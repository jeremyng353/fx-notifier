from bocfx import bocfx
import requests
import json
import smtplib, ssl

message = ""
benchmarks = {
    'CAD': 6,
    'JPY': 0.0565
}

# BOC
currencies = ['CAD,HKD', 'JPY,HKD']

print("BOC")
for currency in currencies:
  currency_list = currency.split(',')
  output = bocfx(currency, 'SE,ASK')
  output[0] = float(output[0]) / float(output[1])
  if output[0] < benchmarks[currency_list[0]]:
    message += currency_list[0] + " to " + currency_list[1] + ": " + str(output[0]) + "\n" 
  print(currency_list[0] + " to " + currency_list[1] + ": " + str(output[0]))

# HSBC
url = "https://api.hsbc.com.hk/live/open-banking/v1.0/personal-foreign-exchange-rates"
payload={}
headers = {
  'ClientID': '6e111af4-2035-4582-b4a2-07b5b44f43c3',
  'ClientSecret': 'vv_29l8oA-YueIfM56i6PLhC7Xiqj_BmW3fW7n0WTcl38ozGIxPoIOCrZfPkA6baJ3CmirUOxfsmj8N2H4Grew'
}

response = requests.request("GET", url, headers=headers, data=payload)
json_data = json.loads(response.text)

print("\nHSBC")
for e in json_data['data'][0]['Brand'][0]['ExchangeRateType'][1]['ExchangeRate'][0]['ExchangeRateTierBand']: 
  if e['CurrencyCode'] == 'CAD' or e['CurrencyCode'] == 'JPY':
    if float(e['BankSellRate']) < benchmarks[e['CurrencyCode']]:
      message += e['CurrencyName'] + ", bank sell rate: " + e['BankSellRate'] + "\n" 
    print(e['CurrencyName'] + ", bank sell rate: " + e['BankSellRate'])

# Hang Seng
url = "https://api.hangseng.com/live/open-banking/v1.0/personal-foreign-exchange-rates"
payload={}
headers = {
  'ClientID': '4f4c36cb-9e02-484a-9088-6e2058331c6e',
  'ClientSecret': 'atZBq9ou7J1nnnIt_ngDCD-UWyJ4cMz_uceGq-MTNm07bMB7tKXKzgMXjiwUF3DegtbaAtgntVb00LXTim_9Kg'
}

response = requests.request("GET", url, headers=headers, data=payload)
json_data = json.loads(response.text)

print("\nHang Seng")
for e in json_data['data'][0]['Brand'][0]['ExchangeRateType'][1]['ExchangeRate'][0]['ExchangeRateTierBand']: 
  if e['CurrencyCode'] == 'CAD' or e['CurrencyCode'] == 'JPY':
    if float(e['BankSellRate']) < benchmarks[e['CurrencyCode']]:
      message += e['CurrencyName'] + ", bank sell rate: " + e['BankSellRate'] + "\n" 
    print(e['CurrencyName'] + ", bank sell rate: " + e['BankSellRate'])

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "kliong31@gmail.com" 
receiver_email = "bnginhk@gmail.com"  
# check pass for the password
# password = "REPLACE_THIS_VALUE"

if message != "":
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)