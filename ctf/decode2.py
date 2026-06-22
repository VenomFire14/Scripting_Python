import hashlib,base64,json,gmpy2,requests


n=int("143378114148022884893321207029708996420518533102791717000410551262205106637624116731830080548032422781470472272225429382462610116519069783686354941290007709713339222408870112264534002668331516130054674275879899440010889368868525224695038243273840041453425671560986589421529424277199564859135277516307128566803")

msg=json.dumps({
"callsign":"pilot",
"clearance":"admin",
"dock":"annulus-gate",
"manifest":"civilian",
"role":"admin",
"sector":"outer-rim"
},separators=(",",":")).encode()


sha=hashlib.sha256(msg).digest()

asn1=bytes.fromhex(
"3031300d060960864801650304020105000420"
)


# 128 byte RSA block
block = b"\x00\x01" + b"\xff"*74 + b"\x00" + asn1 + sha

x=int.from_bytes(block,"big")

sig=int(gmpy2.iroot(x,3)[0])

token=(
base64.urlsafe_b64encode(msg).decode().rstrip("=")
+"."
+base64.urlsafe_b64encode(
sig.to_bytes(128,"big")
).decode().rstrip("=")
)

print(token)

print(
requests.post(
"http://162.243.197.117:5000/dock",
json={"token":token}
).text
)