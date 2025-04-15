
from fyers_apiv3 import fyersModel
from fyers_apiv3 import accessToken

# === User Config ===
client_id = "WTOTXZNDYL-100"        # Format: APP_ID-100
secret_key = "8HAJFLQYC7"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
state = "custom_state"

# === Step 1: Generate Auth URL ===
session = accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type="code",
    state=state
)

auth_url = session.generate_authcode()
print("\n🔗 Visit this URL to log in and authorize:")
print(auth_url)

# === Step 2: Paste auth_code after logging in ===
auth_code = input("\nPaste the auth_code from URL after login: ").strip()

# === Step 3: Exchange auth_code for access_token ===
session.set_token(auth_code)
token_response = session.generate_token()

if "access_token" not in token_response:
    print("❌ Error getting token:", token_response)
    exit()

access_token = token_response["access_token"]
print("\n✅ Access Token received.")

# === Step 4: Initialize Fyers and Fetch Profile ===
fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token,
    log_path="."
)

profile = fyers.get_profile()
print("\n👤 Profile Info:")
print(profile)

# === Step 5: Place a Sample Market Order (SBIN) ===
order = {
    "symbol": "NSE:SBIN-EQ",
    "qty": 1,
    "type": 2,
    "side": 1,
    "productType": "INTRADAY",
    "limitPrice": 0,
    "stopPrice": 0,
    "disclosedQty": 0,
    "validity": "DAY",
    "offlineOrder": False,
    "stopLoss": 0,
    "takeProfit": 0
}

response = fyers.place_order(order)
print("\n📦 Order Response:")
print(response)
