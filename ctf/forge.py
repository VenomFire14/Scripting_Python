from ecdsa.curves import SECP256k1
import hashlib

n = SECP256k1.order


# put your recovered private key here
d = int(
    "1b7ba9dafeb7c7a30fd8043a656c3ab89509db070dbd48b593d8e266b56ca22d",#YOUR_PRIVATE_KEY_HEX
    16
)


# reuse nonce from previous challenge
k = int(
    "0x842d22462a557c342a77a28c521ed84948cdd80167511542ecd88810431625a6",#YOUR_RECOVERED_K_HEX
    16
)


# Need this transaction
sender = "Suspect"
recipient = "Boro_Confiscation_Committee"
amount = "51.42"


msg = f"{sender}:{recipient}:{amount}"

z = int(
    hashlib.sha256(msg.encode()).hexdigest(),
    16
)


# r = x coordinate of kG
G = SECP256k1.generator

r = (k * G).x() % n


s = (pow(k,-1,n) * (z + r*d)) % n


print("r =",hex(r))
print("s =",hex(s))


def der_encode(r,s):

    rb = r.to_bytes(32,'big')
    sb = s.to_bytes(32,'big')

    rb = rb.lstrip(b'\x00')
    sb = sb.lstrip(b'\x00')

    if rb[0] & 0x80:
        rb = b'\x00'+rb

    if sb[0] & 0x80:
        sb = b'\x00'+sb


    body = (
        b'\x02' + bytes([len(rb)]) + rb +
        b'\x02' + bytes([len(sb)]) + sb
    )

    return b'\x30' + bytes([len(body)]) + body


sig = der_encode(r,s)

print(sig.hex())
print("\nFLAG:")
print("boroCTF{" + sig.hex() + "}")