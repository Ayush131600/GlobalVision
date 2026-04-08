import requests
import json

def check_esewa():
    url = "https://rc-epay.esewa.com.np/api/epay/main/v2/form/verification"
    print(f"Checking eSewa Endpoint: {url}")
    try:
        # We use OPTIONS or a dummy GET/POST to check availability
        r = requests.options(url, timeout=10)
        print(f"Status Code: {r.status_code}")
        if r.status_code < 500:
            print("SUCCESS: eSewa Sandbox Server is Reachable and Online.")
        else:
            print(f"WARNING: eSewa Server returned status {r.status_code}")
            
    except Exception as e:
        print(f"FAILURE: Could not connect to eSewa. Error: {str(e)}")

if __name__ == "__main__":
    check_esewa()
