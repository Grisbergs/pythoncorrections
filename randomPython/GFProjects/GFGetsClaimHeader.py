import os
import requests
import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Read environment variables ---
driver = os.getenv("DB_DRIVER")
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

client_id = os.getenv("Client_id")
client_secret = os.getenv("Client_secret")
username = os.getenv("PCMIUser")
pw = os.getenv("PCMIPW")
token_url = os.getenv("TOKEN_URL")
api_base_url = os.getenv("API_BASEURL")
print(f" the base URL {api_base_url}")

# --- Build the connection string dynamically ---
conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={user};"
    f"PWD={password};"
)

# --- Step 1: Request access token ---
token_data = {
    "grant_type": "password",
    "client_id": client_id,
    "client_secret": client_secret,
    "username": username,
    "password": pw
}

token_response = requests.post(token_url, data=token_data)
token_response.raise_for_status()
access_token = token_response.json().get("access_token")

# --- Step 2: Get list of claim numbers ---
with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 300
         ClaimNumber
        FROM [dgw_testing].[dbo].[GF_AuxClaimHeader]
        WHERE insertedDate > '1/1/2026' 
    """)
    claim_numbers = [row[0] for row in cursor.fetchall()]

# --- Step 3: Update Claim Header Function ---
def update_claim_header(ins_comp, veh_state, claim_number):
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE [dgw_testing].[dbo].[GF_AuxClaimHeader]
                SET VehInsCompanyName = ?, VehicleLocationState = ?
                WHERE ClaimNumber = ?
                """,
                (ins_comp, veh_state, claim_number)
            )
            conn.commit()
            print(f"Updated: {claim_number} | InsComp={ins_comp} | State={veh_state}")

    except Exception as e:
        print(f"Database update error for claim {claim_number}: {e}")

# --- Step 4: Loop through claims and call API ---
headers = {"Authorization": f"Bearer {access_token}"}

for claim_number in claim_numbers:
    # Build correct URL without overwriting the variable itself
    url = f"{api_base_url}claims/{claim_number}/header/vehInsCompanyName,vehicleLocationState"
    try:
        api_response = requests.get(url, headers=headers)
        api_response.raise_for_status()
        data = api_response.json()
        ins_comp = data.get("vehInsCompanyName")
        veh_state = data.get("vehicleLocationState")

        update_claim_header(ins_comp, veh_state, claim_number)
        
    except requests.HTTPError as e:
        print(f"API error fetching claim {claim_number}: {e}")
    except Exception as ex:
        print(f"Unexpected error with claim {claim_number}: {ex}")
