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
api_url = os.getenv("API_URL")

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

# --- Step 2: Get list of claim numbers from your table ---
with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT top(10) ClaimNumber FROM [dgw_testing].[dbo].[ClaimDetail] CLD
  inner join [dgw_testing].[dbo].ContractDetail COD  on COD.contractnumber = CLD.ContractNumber
  where TotalPaid > 0 
  and productcode = 'GAP'
  and ClaimNumber not in ( Select Claimnumber from dgw_testing.dbo.GF_ClaimDocuments) 
  group by   ClaimNumber 
""")
    claim_numbers = [row[0] for row in cursor.fetchall()]
    print(claim_numbers)