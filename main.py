# Why do you need cookies?
# We need your account cookie so the bot can login and purchase things on your account
# Is it safe?
# Yes, this is completley safe we do not send your cookie anywhere else but the official roblox webpage. Don't Believe us? Well you can look through the code yourself.
# PLEASE NOTE: When sharing these files always insure that your account cookie is still not in the config.json file 
import time
import httpx
import threading
import json
fetch_config = open("config.json")
config = json.load(fetch_config)
acct_cookie = config["cookie"]
set_items = config["set_items"]
snipe_new_lims = config["snipe_new_limiteds"]
budget = input("Enter your rubux budget: ")
budget = int(budget)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.15 Safari/537.36"
items_sniped = []
def get_userid():
  url = "https://www.roblox.com/catalog/3248850486/yotube" # You can change this to any catalog item if you want
  headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "cookie": acct_cookie,
    "referer": "https://www.roblox.com",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": user_agent
  }
  id = httpx.get(url, headers=headers)
  id = str(id.text)
  file = open("content.txt", "a+")
  file.truncate(0)
  file.write(id)
  file.close()
  f = open("content.txt", "r+")
  content = f.readlines()
  f.close()
  for line in content:
    line = line.replace(" ", "")
    if "data-userid=" in line:
      line = line.replace('data-userid="', "")
      line = line.replace('"', "")
      id = line
      break
  id = id.replace("\n", "")
  return id
id = get_userid()
get_rubux_bal = f"https://economy.roblox.com/v1/users/{id}/currency"
headers = {
  "cookie": acct_cookie
}
rubux_bal = httpx.get(get_rubux_bal, headers=headers)
rubux_bal = rubux_bal.json()["robux"]
rubux_bal = int(rubux_bal)
if rubux_bal < budget:
  print("You do not have enough robux for your budget!")
  time.sleep(6)
  exit(0)

def get_csrf(item_url):
  global t1 
  t1 = time.time()
  headers = {

    "cookie": acct_cookie,
  }
  csrf = httpx.get(item_url, headers=headers)
  csrf = str(csrf.text)
  file = open("content.txt", "a+")
  file.truncate(0)
  file.write(csrf)
  file.close()
  f = open("content.txt", "r+")
  content = f.readlines()
  f.close()
  for line in content:
    line = line.replace(" ", "")
    if 'name="csrf-token"' in line:
      line = line.replace('<metaname="csrf-token"', "")
      line = line.replace('data-token="', "")
      line = line.replace("/>", "")
      line = line.replace('"', "")
      csrf = line
      break
  for line in content:
    line = line.replace(" ", "")
    if 'data-product-id' in line:
      line = line.replace('data-product-id="', "")
      line = line.replace('"', "")
      offical_item_id = line
      break
  for line in content:
    line = line.replace(" ", "")
    if 'data-expected-price=' in line:
      line = line.replace('data-expected-price="', "")
      line = line.replace('"', "")
      item_price = line
      break
  for line in content:
    line = line.replace(" ", "")
    if 'data-expected-seller-id="' in line:
      line = line.replace('data-expected-seller-id="', "")
      line = line.replace('"', "")
      seller_id = line
      break
  
    
  try:
    if int(item_price) > budget:
      print("Item is to expensive for set budget!")
      return main()
    return csrf, offical_item_id, item_price, seller_id
  except UnboundLocalError:
    print("It looks like the item trying to be sniped doesn't exsist!")
    return main()
      
def buy_item(item):
  global t1
  global t2
  global budget
  csrf, item_id, item_price, vendor_id = get_csrf(item)
  csrf = csrf.replace("\n", "")
  item_price = item_price.replace("\n", "")
  vendor_id = vendor_id.replace("\n", "")
  item_id = item_id.replace("\n", "")
  purchase_url = f"https://economy.roblox.com/v1/purchases/products/{item_id}"
  payload = {
    "expectedCurrency": "1",
    "expectedPrice": item_price,
    "expectedSellerId": vendor_id,
  }
  headers = {
    "cookie": acct_cookie,
    "x-csrf-token": csrf
  }
  purchase_response = httpx.post(purchase_url, headers=headers, json=payload)
  if purchase_response.status_code == 200:
    t2 = time.time()
    if item in items_sniped:
      return main()
    print(f"Successfully Sniped Item\nBought at Item Price: {item_price} Robux\nItem Link: {item}\nSniped Item in: {t2-t1} Sec")
    items_sniped.append(item)
    budget -= int(item_price)
  elif purchase_response.status_code == 429:
    print("it looks like you already sniped this item! (Item found in inventory)")
    return main()
  else:
    print(f"Something went wrong trying to snipe item!\nError code: {purchase_response.status_code}")
    time.sleep(6)
    exit(0)
  
file = open("custom.txt", "r+")
data = file.readlines()
file.close()  
def main():
  global custom_items_bought
  if set_items == "true":
    for line in data:
      line = line.replace("\n", "")
      buy_item(line)
    print("Bought all items linked in custom.txt!")
    time.sleep(10)
    exit(0)
    
  

if __name__ == "__main__":
  threads = input("Enter amount of threads: ")
  input("Click enter to start sniping")
  for i in range(int(threads)):
    threading.Thread(target=main).start()
