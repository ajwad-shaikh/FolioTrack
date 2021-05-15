from ..helpers.exchange import getLiveTicker
from flask.json import jsonify
from ..helpers.firebase import db
from ..utils.constants import *

def fetchPortfolioAgency():
    securities = db.collection(PORTFOLIO).stream()
    res = {}
    for securityDoc in securities:
        security = securityDoc.to_dict()
        security.pop(TRADE_IDS, None)
        res[securityDoc.id] = security
    print(res)
    return jsonify(res)

def fetchReturnsAgency():
    securities = db.collection(PORTFOLIO).stream()
    returns = 0
    returnsMap = {}
    for securityDoc in securities:
        security = securityDoc.to_dict()
        live_price = getLiveTicker(securityDoc.id)
        secReturn = security[QUANTITY] * (live_price - security[AVG_PRICE])
        returnsMap[securityDoc.id] = {
            LIVE_PRICE: live_price,
            AVG_PRICE: security[AVG_PRICE],
            QUANTITY: security[QUANTITY],
            RETURNS: secReturn,
        }
        returns = returns + secReturn
    res = {
        MESSAGE_KEY: SUCCESS,
        CUMULATIVE_RETURS: returns,
        SECURITIES: returnsMap,
    }
    print(res)
    return jsonify(res)
