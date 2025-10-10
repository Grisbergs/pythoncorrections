import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv() 

# OAuth2 token endpoint
token_url = "https://aa2-api.pcrsauto.com/token"

# OAuth2 credentials
client_id = os.getenv("Client_id")
client_secret = os.getenv("Client_secret")
username = os.getenv("PCMIUser")
password = os.getenv("PCMIPW")
claimNumber = "CL10457590"

# Step 1: Request access token
token_data = {
    "grant_type": "password",
    "client_id": client_id,
    "client_secret": client_secret,
    "username": username,
    "password": password
}

token_response = requests.post(token_url, data=token_data)
token_response.raise_for_status()
access_token = token_response.json().get("access_token")

# Step 2: Call the document API
api_url = "https://dgws.pcrsauto.com/pcmi.web.services/api/v2/claims/GetDocuments"
params = {"entityNumber": claimNumber}
headers = {"Authorization": f"Bearer {access_token}"}

api_response = requests.get(api_url, headers=headers, params=params)
api_response.raise_for_status()

# ✅ Parse JSON directly (no need for json.loads)
data = api_response.json()

# Access the list of documents
documents = data.get("documents", [])

# Example function that uses the id and documentTypeName
def process_document(doc_id, doc_type):
    print(f"ClaimNumber {claimNumber} Processing document {doc_id} of type {doc_type}")

# Loop through each document and call the function
for doc in documents:
    doc_id = doc.get("id")
    doc_type = doc.get("documentTypeName")
    process_document(doc_id, doc_type)
