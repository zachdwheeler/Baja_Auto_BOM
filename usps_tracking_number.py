import requests, json, base64

#TODO: get a tracking number from liam
TRACKING_NUMBER = "9200190356641437092197"

TESTING = True

# USPS API URLs
if TESTING:
    # Sandbox/test environment URLs
    TRACKING_URL = f'https://apis-tem.usps.com/tracking/v3/tracking/{TRACKING_NUMBER}'
    TOKEN_URL = "https://apis-tem.usps.com/oauth2/v3/token"
else:
    # Production URLs
    TRACKING_URL = f'https://apis.usps.com/tracking/v3/tracking/{TRACKING_NUMBER}'
    TOKEN_URL = "https://apis.usps.com/oauth2/v3/token"

CLIENT_ID = "amLO5l0oAA86X3VAFzaECp1LMzeuRC6USkMxIsnhugVONbEX".strip()
CLIENT_SECRET = "5bE1R8qRnB69jhPzGK7avr30zDvzwAdM6h24TfrZKmvRpW0IfRq3blpfRFmZoTLc".strip()

def set(number):
    global TRACKING_NUMBER
    TRACKING_NUMBER = number
    return TRACKING_URL

def get_oauth():
    """Get OAuth token from USPS API"""
    #TODO: contact the USPS dev team for help with my credentials
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    # USPS expects credentials in the form data, not as Basic auth
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    resp = requests.post(TOKEN_URL, headers=headers, data=data)
    print("Status:", resp.status_code)
    # print("Headers:", resp.headers)
    print("Raw body:", resp.content)

    resp.raise_for_status()
    return resp.json()["access_token"]



if __name__ == "__main__":
    try:
        token = get_oauth()
        print("Access token received (truncated):", token[:20] + '...' if token else '<missing>')
    except Exception as e:
        # Print error with useful details but do not print secrets
        print("Error obtaining token:", e)
