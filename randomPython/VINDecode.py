import requests

def decode_vin(vin: str):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    response = requests.get(url)
    response.raise_for_status()  # raises an error if request failed
    data = response.json()

    make = None
    model = None
    trim  = None

    for item in data.get("Results", []):
        if item["Variable"] == "Make":
            make = item["Value"]
        elif item["Variable"] == "Model":
            model = item["Value"]
        elif item["Variable"] == "Trim":
            trim = item["Value"]

    return make, model, trim

# Example usage
vin_number = "JF2SKADC8RH456826"
make, model, trim = decode_vin(vin_number)

print(f"Make: {make}")
print(f"Model: {model}")
print(f"Trim: {trim}")