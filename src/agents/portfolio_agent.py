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
