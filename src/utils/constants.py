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

# Response / Request
MESSAGE_KEY = 'message'
TRADE_ID = 'tradeId'
INCLUDE_INACTIVE_TRADES = 'includeInactive'
FIELD_TO_UPDATE = 'fieldToUpdate'
UPDATE_VALUE = 'updateValue'
CUMULATIVE_RETURS = 'cumulativeReturns'
SECURITIES = 'securities'
LIVE_PRICE = 'livePrice'
RETURNS = 'returns'

# Messages
VALID = 'Valid request.'
SUCCESS = 'Successfully executed.'
INVALID_TRADE_PARAMETERS_ERROR = 'You seem to have passed invalid trade parameters to the request. Required parameters are \'price\', \'quantity\', \'ticker\' and \'action\' in \'application/json\'.'
SHORT_QUANTITY_ERROR = 'You cannot place a sell trade for more quantity of shares than you currently hold.'
INVALID_ACTION_ERROR = 'Trade action can only be \'BUY\' or \'SELL\'.'
INVALID_REMOVE_REQUEST_PARAMS_ERROR = 'You seem to have passed invalid parameters to the remove request. Required parameter is \'tradeId\' in \'application/json\'.'
SHORT_ERROR_CANNOT_CANCEL_BUY_ERROR = 'We cannot cancel the BUY trade as the net quantity in your portfolio is less than the trade quantity. Consider modifying the order instead.'
INVALID_TRADE_ID_ERROR = 'We could not find an active trade matching this trade id'
INVALID_UPDATE_REQUEST_PARAMS_ERROR = 'You seem to have passed invalid parameters to the update request. Required parameters are \'tradeId\', \'fieldToUpdate\' and \'updateValue\' in \'application/json\'.'
NO_NEED_FOR_UPDATE_ERROR = 'No need to update as value to be updated matches the current value.'

# Live Price Constant
LIVE_PRICE_CONSTANT = 100

# Env variables

SERVICE_ACCOUNT_KEY = 'SERVICE_ACCOUNT_KEY'
