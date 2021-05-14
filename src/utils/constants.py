# DB Collections
PORTFOLIO = 'portfolio'
TRADES = 'trades'

# Common Document Keys
QUANTITY = 'quantity'
CREATED_AT = 'created_at'
MODIFIED_AT = 'modified_at'

# Portfolio Document Keys
AVG_PRICE = 'average_price'
TRADE_IDS = 'trade_ids'

# Trade Document Keys
ACTION = 'action'
TICKER = 'ticker'
PRICE = 'price'
IS_ACTIVE = 'is_active'

# Actions
BUY = 'BUY'
SELL = 'SELL'

# Response 
MESSAGE_KEY = 'message'
TRADE_ID_KEY = 'trade_id'
SUCCESS = 'Successfully executed.'
INVALID_TRADE_PARAMETERS_ERROR = 'You seem to have passed invalid trade parameters to the request. Required parameters are \'price\', \'quantity\', \'ticker\' and \'action\' in \'application/json\'.'
SHORT_QUANTITY_ERROR = 'You cannot place a sell trade for more quantity of shares than you currently hold.'
INVALID_ACTION_ERROR = 'Trade action can only be \'BUY\' or \'SELL\'.'

# Request
INCLUDE_INACTIVE_TRADES = 'includeInactive'
