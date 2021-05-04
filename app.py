from flask import Flask

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/api/trade", methods=["GET"])
def fetchTrades():
    # Fetch Trades
    return "Fetch Trades"

@app.route("/api/trade", methods=["POST"])
def addTrade():
    # Add Trade
    return "Add Trade"

@app.route("/api/trade", methods=["PATCH"])
def updateTrade():
    # Update Trade
    return "Update Trade"

@app.route("/api/trade", methods=["DELETE"])
def removeTrade():
    # Remove Trade
    return "Remove Trade"

@app.route("/api/portfolio", methods=["GET"])
def fetchPortfolio():
    # Fetch Portfolio
    return "Portfolio"

@app.route("/api/returns", methods=["GET"])
def fetchReturns():
    # Fetch Returns
    return "Returns"
