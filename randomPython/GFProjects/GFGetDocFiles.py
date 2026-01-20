import requests
import base64
from dotenv import load_dotenv
import os
import pyodbc
from datetime import datetime

# ------------------------
# Load environment variables
# ------------------------
load_dotenv()

token_url = os.getenv("TOKEN_URL")
api_url = os.getenv("DocFileAPI_URL")

driver = os.getenv("DB_DRIVER")
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

client_id = os.getenv("Client_id")
client_secret = os.getenv("Client_secret")
username = os.getenv("PCMIUser")
pw = os.getenv("PCMIPW")

# ------------------------
# Logging setup
# ------------------------
log_file = os.path.join(os.getcwd(), "GF_DocLog.txt")

def log_message(message: str):
    """Append a timestamped message to the log file and print it."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(full_message)
    print(full_message.strip())

# ------------------------
# Get API Access Token
# ------------------------
token_data = {
    "grant_type": "password",
    "client_id": client_id,
    "client_secret": client_secret,
    "username": username,
    "password": pw
}

try:
    token_response = requests.post(token_url, data=token_data)
    token_response.raise_for_status()
    access_token = token_response.json().get("access_token")
    log_message("✅ Successfully obtained access token.")
except Exception as e:
    log_message(f"❌ Failed to get access token: {e}")
    raise SystemExit(e)

headers = {"Authorization": f"Bearer {access_token}"}

# ------------------------
# Database connection string
# ------------------------
conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={user};"
    f"PWD={password};"
)

# ------------------------
# Query for pending documents
# ------------------------
with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT  top(400)
            [DocumentID],
            [ClaimNumber]
        FROM [dgw_testing].[dbo].[GF_ClaimDocuments]
        WHERE  
          SentToGf is Null        
    """)
    documents = cursor.fetchall()

log_message(f"📄 Retrieved {len(documents)} documents pending for upload.\n")

# ------------------------
# Create GFdocuments root folder
# ------------------------
gf_root = os.path.join(os.getcwd(), "GFdocuments")
os.makedirs(gf_root, exist_ok=True)

# ------------------------
# Process each document
# ------------------------
for doc_id, claim_number in documents:
    try:
        log_message(f"Processing DocumentID: {doc_id} for Claim: {claim_number}")

        # --- Step 1: Call API for document data ---
        params = {"id": doc_id}
        api_response = requests.get(api_url, headers=headers, params=params)
        api_response.raise_for_status()
        doc_data = api_response.json()

        file_name = doc_data.get("fileName", f"{doc_id}.pdf")
        document_data = doc_data.get("documentData")

        if not document_data:
            log_message(f"⚠️ No document data returned for {doc_id}")
            continue

        # --- Step 2: Create claim folder under GFdocuments ---
        claim_folder = os.path.join(gf_root, str(claim_number))
        os.makedirs(claim_folder, exist_ok=True)

        # --- Step 3: Decode and save file ---
        file_path = os.path.join(claim_folder, file_name)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(document_data))

        log_message(f"✅ File saved to {file_path}")

        # --- Step 4: Update record in database ---
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE [dgw_testing].[dbo].[GF_ClaimDocuments]
                SET SentToGF = 1
                WHERE DocumentID = ?
            """, (doc_id,))
            conn.commit()

        log_message(f"🟢 Updated SentToGF = 1 for DocumentID {doc_id}\n")

    except Exception as e:
        log_message(f"❌ Error processing DocumentID {doc_id}: {e}\n")
