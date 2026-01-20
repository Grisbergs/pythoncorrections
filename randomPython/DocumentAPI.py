import requests
import base64
from dotenv import load_dotenv
import os
import pyodbc



load_dotenv() 
# OAuth2 token endpoint
token_url = "https://aa2-api.pcrsauto.com/token"

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
api_url = os.getenv("DocFileAPI_URL")

# Step 1: Request access token
token_data = {
    "grant_type": "password",
    "client_id": client_id,
    "client_secret": client_secret,
    "username": username,
    "password": password
}

# --- Build the connection string dynamically ---
conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={user};"
    f"PWD={password};"
)

token_response = requests.post(token_url, data=token_data)
token_response.raise_for_status()
access_token = token_response.json().get("access_token")



with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT top(100) ClaimNumber FROM [dgw_testing].[dbo].[ClaimDetail] CLD
  inner join [dgw_testing].[dbo].ContractDetail COD  on COD.contractnumber = CLD.ContractNumber
  where TotalPaid > 0 
  and productcode = 'GAP'
  and ClaimNumber not in ( Select Claimnumber from dgw_testing.dbo.GF_ClaimDocuments) 
  group by   ClaimNumber 
""")
    doc_ids = [row[0] for row in cursor.fetchall()]
 
# --- Step 3: Define document insert function ---
def insert_document_record(doc_id, doc_type, claim_number):
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO [dgw_testing].[dbo].GF_ClaimDocuments (ClaimNumber, DocumentID, DocumentTypeName)
                VALUES (?, ?, ?)
                """,
                (claim_number, doc_id, doc_type)
            )
            conn.commit()
            print(f"Inserted document {doc_id} ({doc_type}) for claim {claim_number}")
    except Exception as e:
        print(f"Database insert error for claim {claim_number}, doc {doc_id}: {e}")


for document in doc_ids:
    params = {"id": document}

headers = {
    "Authorization": f"Bearer {access_token}"
}

api_response = requests.get(api_url, headers=headers, params=params)
api_response.raise_for_status()
doc_data = api_response.json()

# Step 3: Save document
file_name = doc_data["fileName"]
document_data = doc_data["documentData"]  # base64 string

# Decode and save file
file_bytes = base64.b64decode(document_data)
with open(file_name, "wb") as f:
    f.write(file_bytes)

print(f"✅ File saved as {file_name}")
