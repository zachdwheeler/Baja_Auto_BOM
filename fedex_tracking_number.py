import requests, base64, json

# --- CONFIG ---
USE_SANDBOX = True
TRACKING_NUMBER = "123456789012"  # FedEx dummy number

if USE_SANDBOX:
    CLIENT_ID = "l74c06830cd9cf432bb8402132b8617bc7"
    CLIENT_SECRET = "0ecda495be784c30a4753872390f4f08"
    OAUTH_URL = "https://apis-sandbox.fedex.com/oauth/token"
    TRACK_URL = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"
else:
    CLIENT_ID = "YOUR_PRODUCTION_CLIENT_ID"
    CLIENT_SECRET = "YOUR_PRODUCTION_CLIENT_SECRET"
    OAUTH_URL = "https://apis.fedex.com/oauth/token"
    TRACK_URL = "https://apis.fedex.com/track/v1/trackingnumbers"

# --- FUNCTIONS ---
def get_oauth_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64_auth}"
    }
    data = "grant_type=client_credentials"

    resp = requests.post(OAUTH_URL, headers=headers, data=data)
    print("Status:", resp.status_code)
    print("Headers:", resp.headers)
    print("Raw body:", resp.content)

    resp.raise_for_status()
    return resp.json()["access_token"]

def track_package(tracking_number, token):
    headers = {
        "Content-Type": "application/json",
        "X-locale": "en_US",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "trackingInfo": [
            {"trackingNumberInfo": {"trackingNumber": tracking_number}}
        ]
    }
    resp = requests.post(TRACK_URL, headers=headers, json=payload)
    print("Track status:", resp.status_code)
    print("Track body:", resp.text)

# --- MAIN ---
token = get_oauth_token()
print("Access token:", token)
track_package(TRACKING_NUMBER, token)
