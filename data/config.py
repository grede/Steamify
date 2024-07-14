# api id, hash
API_ID = 0
API_HASH = 'insert your api hash here'

DELAYS = {
    'ACCOUNT': [5, 15],  # delay between connections to accounts (the more accounts, the longer the delay)
    'CLAIM': [60, 180]   # delay in seconds before claim points every 8 hours
}

PROXY_TYPES = {
    "TG": "http",  # proxy type for tg client. "socks4", "socks5" and "http" are supported
    "REQUESTS": "http"  # proxy type for requests. "http" for https and http proxys, "socks5" for socks5 proxy.
}

# session folder (do not change)
WORKDIR = "sessions/"

# timeout in seconds for checking accounts on valid
TIMEOUT = 30
