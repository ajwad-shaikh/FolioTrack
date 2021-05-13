from datetime import datetime
from flask.json import jsonify
from ..helpers.firebase import db

def fetchTradesAgency():
    securities = db.collection('portfolio').stream()
    res = {}
    for securityDoc in securities:
        security = securityDoc.to_dict()
        res[securityDoc.id] = []
        for trade in security['trade_ids']:
            tradeDoc = db.collection('trades').document(trade).get()
            tradeDocDict = tradeDoc.to_dict()
            tradeDocDict.pop('ticker', None)
            res[securityDoc.id].append(tradeDocDict)
    print(res)
    return res

def addTradesAgency(request_json):
    action = request_json.get("action")
    price = request_json.get("price")
    quantity = request_json.get("quantity")
    ticker = request_json.get("ticker")
    if isInvalidTrade(price, quantity, action, ticker):
        return jsonify({ "message" : "Invalid trade parameters passed!"})
    
    # add new trade to doc
    trade_doc = db.collection('trades').add({
        "action": action,
        "price": price,
        "ticker": ticker,
        "quantity": quantity,
        "is_active": True,
        "created_at": datetime.now(),
        "modified_at": datetime.now()
    })
    trade_id = trade_doc[1].id

    # get current portfolio doc 
    portfolioDoc = db.collection('portfolio').document(ticker).get()

    if portfolioDoc.exists:
        # modify current portfolio doc
        portfolioDict = portfolioDoc.to_dict()
        avg_price = portfolioDict["average_price"]
        qty = portfolioDict["quantity"]
        trade_qty = getQuantity(quantity, action)
        portfolioDict["quantity"] = trade_qty + qty
        if action == "BUY":
            portfolioDict["average_price"] = ((avg_price * qty) + (price * trade_qty)) / (trade_qty + qty)
        portfolioDict["trade_ids"].append(trade_id)
        portfolioDict["modified_at"] = datetime.now()
    else:
        # create portfolio
        portfolioDict = {
            "average_price": price,
            "quantity": quantity,
            "trade_ids": [trade_id],
            "created_at": datetime.now(),
            "modified_at": datetime.now()
        }
    
    portfolioDoc = db.collection('portfolio').document(ticker).set(portfolioDict)

    return jsonify(trade_id)

def getQuantity(quantity, action):
    if action == "BUY":
        return quantity
    elif action == "SELL":
        return -1 * quantity
    else:
        return 0

def isInvalidTrade(price, quantity, action, ticker):
    if action is None or price is None or quantity is None or ticker is None:
        # One of the parameters has not been passed
        return False
    if action == "SELL":
        # Validate Sell Action.
        portfolioDoc = db.collection('portfolio').document(ticker).get()
        if portfolioDoc.exists:
            # Stock present in portfolio.
            portfolioDict = portfolioDoc.to_dict()
            if portfolioDict.get("quantity") < quantity:
                # Short sell is invalid.
                return True
            else:
                # Valid sell order.
                return False
        else:
            # Stock not present in portfolio i.e. never bought before - can't sell - invalid.
            return True
    elif action == "BUY":
        # Buy is always valid.
        return False
    else:
        # Invalid action.
        return True
