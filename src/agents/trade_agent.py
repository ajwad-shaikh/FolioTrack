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
        return jsonify({MESSAGE_KEY: INVALID_TRADE_PARAMETERS_ERROR})
    trade_id = remove_request.get(TRADE_ID)

    # (canTradeBeRemoved->bool, Error Message)
    remove_validity_tuple = canTradeBeRemoved(trade_id)
    if remove_validity_tuple[0] is False:
        return jsonify({MESSAGE_KEY: remove_validity_tuple[1]})
    
    # set trade as inactive
    db.collection(TRADES).document(trade_id).set({
        IS_ACTIVE: False
    }, merge=True)

    # get trade document
    trade_dict = db.collection(TRADES).document(trade_id).get().to_dict()

    # modify portfolio quantity
    qty_change = -1 * getQuantity(trade_dict[QUANTITY], trade_dict[ACTION])
    db.collection(PORTFOLIO).document(trade_dict[TICKER]).update({
        QUANTITY: firestore.Increment(qty_change)
    })

    response_doc = {
        MESSAGE_KEY: SUCCESS,
        TICKER: trade_dict[TICKER],
        TRADE_ID: trade_id 
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
    if action is None or price is None or quantity is None or ticker is None:
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

