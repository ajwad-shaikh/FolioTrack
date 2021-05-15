from flask.json import jsonify
from ..helpers.firebase import db, firestore
from ..utils.constants import *

def fetchTradesAgency(include_inactive=False):
    securities = db.collection(PORTFOLIO).stream()
    res = {}
    for securityDoc in securities:
        security = securityDoc.to_dict()
        res[securityDoc.id] = []
        for trade in security[TRADE_IDS]:
            tradeDoc = db.collection(TRADES).document(trade).get()
            tradeDocDict = tradeDoc.to_dict()
            tradeDocDict.pop(TICKER, None)
            if tradeDocDict[IS_ACTIVE] or include_inactive:
                res[securityDoc.id].append(tradeDocDict)
    print(res)
    return jsonify(res)

def addTradesAgency(trade_request):
    if trade_request is None:
        return jsonify({MESSAGE_KEY: INVALID_TRADE_PARAMETERS_ERROR})
    action = trade_request.get(ACTION)
    price = trade_request.get(PRICE)
    quantity = trade_request.get(QUANTITY)
    ticker = trade_request.get(TICKER)

    # (isTradeValid->bool, Error Message)
    trade_validity_tuple = isTradeValid(price, quantity, action, ticker) 

    if trade_validity_tuple[0] is False:
        return jsonify({ MESSAGE_KEY : trade_validity_tuple[1]})
    
    # add new trade to doc
    trade_doc = db.collection(TRADES).add({
        ACTION: action,
        PRICE: price,
        TICKER: ticker,
        QUANTITY: quantity,
        IS_ACTIVE: True,
        CREATED_AT: firestore.SERVER_TIMESTAMP,
        MODIFIED_AT: firestore.SERVER_TIMESTAMP
    })
    trade_id = trade_doc[1].id

    # get current portfolio doc 
    portfolioDoc = db.collection(PORTFOLIO).document(ticker).get()

    if portfolioDoc.exists:
        # modify current portfolio doc
        portfolioDict = portfolioDoc.to_dict()
        avg_price = portfolioDict[AVG_PRICE]
        qty = portfolioDict[QUANTITY]
        trade_qty = getQuantity(quantity, action)
        portfolioDict[QUANTITY] = trade_qty + qty
        if action == BUY:
            portfolioDict[AVG_PRICE] = ((avg_price * qty) + (price * trade_qty)) / (trade_qty + qty)
        portfolioDict[TRADE_IDS].append(trade_id)
        portfolioDict[MODIFIED_AT] = firestore.SERVER_TIMESTAMP
    else:
        # create portfolio
        portfolioDict = {
            AVG_PRICE: price,
            QUANTITY: quantity,
            TRADE_IDS: [trade_id],
            CREATED_AT: firestore.SERVER_TIMESTAMP,
            MODIFIED_AT: firestore.SERVER_TIMESTAMP,
        }
    
    portfolioDoc = db.collection(PORTFOLIO).document(ticker).set(portfolioDict)

    response_doc = {
        MESSAGE_KEY: SUCCESS,
        TICKER: ticker,
        TRADE_ID: trade_id 
    }
    print(response_doc)
    return jsonify(response_doc)

def removeTradesAgency(remove_request):
    if remove_request is None:
        return jsonify({MESSAGE_KEY: INVALID_REMOVE_REQUEST_PARAMS_ERROR})
    trade_id = remove_request.get(TRADE_ID)

    # (canTradeBeRemoved->bool, Error Message)
    remove_validity_tuple = canTradeBeRemoved(trade_id)
    if remove_validity_tuple[0] is False:
        return jsonify({MESSAGE_KEY: remove_validity_tuple[1]})
    
    # set trade as inactive
    db.collection(TRADES).document(trade_id).set({
        IS_ACTIVE: False,
        MODIFIED_AT: firestore.SERVER_TIMESTAMP
    }, merge=True)

    # get trade document
    trade_dict = db.collection(TRADES).document(trade_id).get().to_dict()
    portfolio_dict = db.collection(PORTFOLIO).document(trade_dict[TICKER]).get().to_dict()

    # modify portfolio document
    if trade_dict[ACTION] == SELL:
        newQty = portfolio_dict[QUANTITY] + trade_dict[QUANTITY]
        newAvg = portfolio_dict[AVG_PRICE]
    elif trade_dict[ACTION] == BUY:
        newCorpus = (portfolio_dict[QUANTITY] * portfolio_dict[AVG_PRICE]) - (trade_dict[QUANTITY] * trade_dict[PRICE])
        newQty = portfolio_dict[QUANTITY] - trade_dict[QUANTITY]
        newAvg = newCorpus / newQty
    
    db.collection(PORTFOLIO).document(trade_dict[TICKER]).set({
        QUANTITY: newQty,
        AVG_PRICE: newAvg,
        MODIFIED_AT: firestore.SERVER_TIMESTAMP
    }, merge=True)

    response_doc = {
        MESSAGE_KEY: SUCCESS,
        TICKER: trade_dict[TICKER],
        TRADE_ID: trade_id 
    }
    print(response_doc)
    return jsonify(response_doc)

def updateTradesAgency(update_request): 
    if update_request is None:
        return jsonify({MESSAGE_KEY: INVALID_UPDATE_REQUEST_PARAMS_ERROR})
    
    tradeId = update_request.get(TRADE_ID)
    fieldToUpdate = update_request.get(FIELD_TO_UPDATE)
    updateValue = update_request.get(UPDATE_VALUE)

    # (canTradeBeUpdated->bool, Error Message)
    update_validity_tuple = canTradeBeUpdated(tradeId, fieldToUpdate, updateValue)
    if update_validity_tuple[0] is False:
        return jsonify({MESSAGE_KEY: update_validity_tuple[1]})
    
    tradeDict = db.collection(TRADES).document(tradeId).get().to_dict()

    # update trade
    db.collection(TRADES).document(tradeId).set({
        fieldToUpdate: updateValue,
        MODIFIED_AT: firestore.SERVER_TIMESTAMP
    }, merge=True)

    # update portfolio
    portfolioDict = db.collection(PORTFOLIO).document(tradeDict[TICKER]).get().to_dict()
    currCorpus = portfolioDict[AVG_PRICE] * portfolioDict[QUANTITY]
    if fieldToUpdate == PRICE:
        newCorpus = currCorpus + ((updateValue-tradeDict[PRICE]) * tradeDict[QUANTITY])
        newAvg = newCorpus / portfolioDict[QUANTITY]
        db.collection(PORTFOLIO).document(tradeDict[TICKER]).set({
            AVG_PRICE: newAvg,
            MODIFIED_AT: firestore.SERVER_TIMESTAMP
        }, merge=True)
    elif fieldToUpdate == QUANTITY:
        if tradeDict[ACTION] == BUY:
            newQty = portfolioDict[QUANTITY] + updateValue - tradeDict[QUANTITY]
            newCorpus = currCorpus + ((updateValue - tradeDict[QUANTITY]) * tradeDict[PRICE])
            newAvg = newCorpus / newQty
        elif tradeDict[ACTION] == SELL:
            newQty = portfolioDict[QUANTITY] - updateValue + tradeDict[QUANTITY]
            newAvg = portfolioDict[AVG_PRICE]
        db.collection(PORTFOLIO).document(tradeDict[TICKER]).set({
            AVG_PRICE: newAvg,
            QUANTITY: newQty,
            MODIFIED_AT: firestore.SERVER_TIMESTAMP
        }, merge=True)
    elif fieldToUpdate == ACTION:
        if tradeDict[ACTION] == BUY and updateValue == SELL:
            newCorpus = currCorpus - (tradeDict[QUANTITY] * tradeDict[PRICE])
            newQty = portfolioDict[QUANTITY] - (2 * tradeDict[QUANTITY])
        elif tradeDict[ACTION] == SELL and updateValue == BUY:
            newCorpus = currCorpus + (tradeDict[QUANTITY] * tradeDict[PRICE])
            newQty = portfolioDict[QUANTITY] + (2 * tradeDict[QUANTITY])
        newAvg = newCorpus / newQty
        db.collection(PORTFOLIO).document(tradeDict[TICKER]).set({
            AVG_PRICE: newAvg,
            QUANTITY: newQty,
            MODIFIED_AT: firestore.SERVER_TIMESTAMP
        }, merge=True)

    response_doc = {
        MESSAGE_KEY: SUCCESS,
        TICKER: tradeDict[TICKER],
        TRADE_ID: tradeId 
    }
    print(response_doc)
    return jsonify(response_doc)

def getQuantity(quantity, action) -> float:
    if action == BUY:
        return quantity
    elif action == SELL:
        return -1 * quantity
    else:
        return 0

def isTradeValid(price, quantity, action, ticker) -> tuple:
    if action is None or price is None or quantity is None or ticker is None or quantity < 0:
        # One of the parameters has not been passed
        return (False, INVALID_TRADE_PARAMETERS_ERROR)
    if action == SELL:
        # Validate Sell Action.
        portfolioDoc = db.collection(PORTFOLIO).document(ticker).get()
        if portfolioDoc.exists:
            # Stock present in portfolio.
            portfolioDict = portfolioDoc.to_dict()
            if portfolioDict.get(QUANTITY) < quantity:
                # Short sell is invalid.
                return (False, SHORT_QUANTITY_ERROR)
            else:
                # Valid sell order.
                return (True, VALID)
        else:
            # Stock not present in portfolio i.e. never bought before - can't sell - invalid.
            return (False, SHORT_QUANTITY_ERROR)
    elif action == BUY:
        # Buy is always valid.
        return (True, VALID)
    else:
        # Invalid action.
        return (False, INVALID_ACTION_ERROR)

def canTradeBeRemoved(trade_id) -> tuple:
    if trade_id is None:
        return (False, INVALID_REMOVE_REQUEST_PARAMS_ERROR)

    # Fetch Trade Doc
    tradeDoc = db.collection(TRADES).document(trade_id).get()
    tradeDict = {}

    # Trade not found
    if tradeDoc.exists:
        tradeDict = tradeDoc.to_dict()
    else:
        return (False, INVALID_TRADE_ID_ERROR)

    # Already deleted Trade
    if tradeDict[IS_ACTIVE] is not True:
        return (False, INVALID_TRADE_ID_ERROR)

    if tradeDict[ACTION] == SELL:
        # Removing SELL orders is safe as total quantity will always increase.
        return (True, VALID)
    
    # Fetch Portfolio document
    portfolioDict = db.collection(PORTFOLIO).document(tradeDict[TICKER]).get().to_dict()

    if tradeDict[ACTION] == BUY:
        # Removing Buy Trade
        post_transact_quantity = portfolioDict[QUANTITY] - tradeDict[QUANTITY]
        if post_transact_quantity >= 0:
            # Non-negative quantity left
            return (True, VALID)
        else:
            # Negative quantity
            return (False, SHORT_ERROR_CANNOT_CANCEL_BUY_ERROR)
    else:
        # Invalid action
        return (False, INVALID_ACTION_ERROR)

def canTradeBeUpdated(tradeId, fieldToUpdate, updateValue) -> bool:
    if tradeId is None or fieldToUpdate is None or updateValue is None:
        return (False, INVALID_UPDATE_REQUEST_PARAMS_ERROR)
    
    trade_fields = [PRICE, ACTION, QUANTITY]
    if fieldToUpdate not in trade_fields:
        return (False, INVALID_UPDATE_REQUEST_PARAMS_ERROR)
    
    tradeDict = db.collection(TRADES).document(tradeId).get().to_dict()

    if fieldToUpdate == PRICE:
        if tradeDict[PRICE] == updateValue:
            return (False, NO_NEED_FOR_UPDATE_ERROR)
        else:
            return (True, SUCCESS)
    elif fieldToUpdate == ACTION:
        if tradeDict[ACTION] == updateValue:
            return (False, NO_NEED_FOR_UPDATE_ERROR)
        else:
            # check if quantity will remain positive post change
            if tradeDict[ACTION] == SELL and updateValue == BUY:
                # additive action
                return (True, SUCCESS)
            elif tradeDict[ACTION] == BUY and updateValue == SELL:
                portfolioDict = db.collection(PORTFOLIO).document(tradeDict[TICKER]).get().to_dict()
                post_quantity = portfolioDict[QUANTITY] - (tradeDict[QUANTITY] * 2)
                if post_quantity >= 0:
                    return (True, SUCCESS)
                else:
                    return (False, SHORT_ERROR_CANNOT_CANCEL_BUY_ERROR)
            else:
                return (False, INVALID_ACTION_ERROR)
    elif fieldToUpdate == QUANTITY:
        if updateValue < 0:
            return (False, INVALID_UPDATE_REQUEST_PARAMS_ERROR)
        elif tradeDict[QUANTITY] == updateValue:
            return (False, NO_NEED_FOR_UPDATE_ERROR)
        else:
            if (updateValue > tradeDict[QUANTITY] and tradeDict[ACTION] == BUY) or (updateValue < tradeDict[QUANTITY] and tradeDict[ACTION] == SELL) :
                # increased net quantity
                return (True, SUCCESS)
            else:
                # decreased net quantity
                portfolioDict = db.collection(PORTFOLIO).document(tradeDict[TICKER]).get().to_dict()
                post_quantity = portfolioDict[QUANTITY] - getQuantity(tradeDict[QUANTITY] - updateValue, tradeDict[ACTION])
                if post_quantity >= 0:
                    return (True, SUCCESS)
                else:
                    return (False, SHORT_ERROR_CANNOT_CANCEL_BUY_ERROR)
