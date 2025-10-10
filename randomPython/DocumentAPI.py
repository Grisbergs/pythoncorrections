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
password =os.getenv("PCMIPW") 

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


api_url = "https://dgws.pcrsauto.com/pcmi.web.services/api/v2/claims/getdocument"
params = {"id": 6562599}  

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
