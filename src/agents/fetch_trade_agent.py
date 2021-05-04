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
