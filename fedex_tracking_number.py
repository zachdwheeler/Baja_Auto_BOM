import requests, json

# --- CONFIG ---
USE_SANDBOX = False
TRACKING_NUMBER = "123456789012"  # FedEx dummy number

if USE_SANDBOX:
    CLIENT_ID = "l74c06830cd9cf432bb8402132b8617bc7"
    CLIENT_SECRET = "0ecda495be784c30a4753872390f4f08"
    OAUTH_URL = "https://apis-sandbox.fedex.com/oauth/token"
    TRACK_URL = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"
else:
    CLIENT_ID = "l779e5e08d00cc4443a08d164f7fe426e1"
    CLIENT_SECRET = "e890c61d07aa4c27b5a68f6e9ea2cb90"
    OAUTH_URL = "https://apis.fedex.com/oauth/token"
    TRACK_URL = "https://apis.fedex.com/track/v1/trackingnumbers"

# --- FUNCTIONS ---
def set(number):
    #call me maybe
    TRACKING_NUMBER = number

def get_OAUTH():

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    

    resp = requests.post(OAUTH_URL, headers=headers, data=data)

    resp.raise_for_status()
    return resp.json()["access_token"]

def get_payload():
    payload = {
    "trackingInfo": 
    [
    {
        "trackingNumberInfo": 
            {
                "trackingNumber": TRACKING_NUMBER
            }
        }
    ],
        "includeDetailedScans": True
    }
    return payload

def get_json_file():
    # Get OAuth token first
    token = get_OAUTH()
    
    # Use the correct URL based on sandbox setting
    url = TRACK_URL

    payload = get_payload()
    headers = {
        'Content-Type': "application/json",
        'X-locale': "en_US",
        'Authorization': f"Bearer {token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def get_list_of_keys(package_data):
    track_results = package_data["output"]["completeTrackResults"][0]["trackResults"][0]
    return list(track_results.keys())

def check_if_key_is_valid(key):
    if key in get_list_of_keys(get_json_file()):
        print("sea cucumber")
    else:
        print("key is not here")

def get_key_value(key):
    package_data = get_json_file()
    track_results = package_data["output"]["completeTrackResults"][0]["trackResults"][0]
    try:
        return track_results[key]
    except:
        return f'{key} is an invalid key'

#pretty sure the reason this doesnt work rn is since the dummy number has multiple packages attached ot it
print(get_list_of_keys(get_json_file()))
#could put shipment details through get_list_of_keys and check if "contents" is a key, if so then get part numbers 
print(f'package details go bang: {get_key_value("estimatedDeliveryTimeWindow")}')
