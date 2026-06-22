import requests

url="http://192.241.175.41:5000/"

a=requests.post(url+"/sign",
json={"message":"AAA"}).json()

b=requests.post(url+"/sign",
json={"message":"BBB"}).json()

print(a)
print(b)

x = 90407791030827140832888634182624650101514785441950035367149030527983647

print(x.bit_length())