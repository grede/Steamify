# api id, hash
API_ID = 0
API_HASH = 'insert your api hash here'

DELAYS = {
    'ACCOUNT': [5, 15],  # delay between connections to accounts (the more accounts, the longer the delay)
    'CLAIM': [60, 180]   # delay in seconds before claim points every 8 hours
}

TASKS = {
    'PERFORM_TASKS': True, # whether soft should perform tasks / claim task rewards or not
    'DELAY': [5, 15], # delay in seconds in between any task actions
    'BLACKLIST_TASK': ["Invite 1 friend", "Invite 5 friends", "Invite 15 friends"] # names of tasks that soft should not attempt to perform
}

SPARKS = {
    'COLLECT_SPARKS': True, # whether soft should collect sparks
}

CASE_OPEN_GAME = {
    'PLAY': True,  # whether soft should open cases or not
    'CASES_TO_BE_OPENED': [0, 1],  # number of cases soft should open at one go (min, max)
    'DELAY_BETWEEN_OPENINGS': [15, 60],  # delay in seconds (min, max) between each case opening attempt
    'CASE_PRICE': [0, 300],  # price range (min, max) in which soft would randomly pick next case to be opened
    'MIN_BALANCE_CONTROL': 1000  # min account balance at which soft will stop any attempt to buy new cases
}

PROXY_TYPES = {
    "TG": "http",  # proxy type for tg client. "socks4", "socks5" and "http" are supported
    "REQUESTS": "http"  # proxy type for requests. "http" for https and http proxys, "socks5" for socks5 proxy.
}

# session folder (do not change)
WORKDIR = "sessions/"

# timeout in seconds for checking accounts on valid
TIMEOUT = 30
REQUEST_TIMEOUT = 120
