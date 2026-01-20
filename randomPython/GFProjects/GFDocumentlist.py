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
      SELECT top(100) CLD.ClaimNumber FROM [dgw_testing].[dbo].[ClaimDetail] CLD
  inner join [dgw_testing].[dbo].ContractDetail COD  on COD.contractnumber = CLD.ContractNumber
    inner join   [dgwods_new].[dbo].[ClaimHeader] b on b.ClaimNumber = CLD.ClaimNumber            
  where TotalPaid > 0 
  and productcode = 'GAP'
                   and NoPrimaryInsurance <>'Yes'
  and CLD.ClaimNumber not in ( Select Claimnumber from dgw_testing.dbo.GF_ClaimDocuments) 
  group by   CLD.ClaimNumber 
""")
    claim_numbers = [row[0] for row in cursor.fetchall()]
    
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

# --- Step 4: Loop through claim numbers and call API ---
headers = {"Authorization": f"Bearer {access_token}"}

for claim_number in claim_numbers:
    params = {"entityNumber": claim_number}

    try:
        api_response = requests.get(api_url, headers=headers, params=params)
        api_response.raise_for_status()
        data = api_response.json()

        documents = data.get("documents", [])
        for doc in documents:
            doc_id = doc.get("id")
            doc_type = doc.get("documentTypeName")
            insert_document_record(doc_id, doc_type, claim_number)

    except requests.HTTPError as e:
        print(f"Error fetching documents for {claim_number}: {e}")
    except Exception as ex:
        print(f"Unexpected error with {claim_number}: {ex}")
