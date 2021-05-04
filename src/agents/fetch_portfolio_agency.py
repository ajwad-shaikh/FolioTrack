from ..helpers.firebase import db

def fetchPortfolioAgency():
    securities = db.collection('portfolio').stream()
    res = {}
    for securityDoc in securities:
        security = securityDoc.to_dict()
        security.pop('trade_ids', None)
        res[securityDoc.id] = security
    print(res)
    return res
