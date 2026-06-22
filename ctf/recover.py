import hashlib
from ecdsa.curves import SECP256k1

n = SECP256k1.order

r = int(
"2cbda85fc21f5e62f94d8378d2dad1a05bc5d5522d5a717f2bdf1df13d558ec7",
16
)

s1 = int(
"4b2f38c18c2a933f81112350ae048f0162feaaed599f827180944ea3203570de",
16
)

s2 = int(
"7db2d815212aab6b986d0a403b724ad5fd57d2d9e826bf2893e29d9d179d59f3",
16
)


def sha256_int(sender, recipient, amount):
    msg = f"{sender}:{recipient}:{amount}"
    return int(hashlib.sha256(msg.encode()).hexdigest(),16)


z1 = sha256_int(
    "Suspect",
    "FranklinGothic",
    "21.68"
)

z2 = sha256_int(
    "Suspect",
    "ForeverFlames",
    "45.46"
)


# k = (z1-z2)/(s1-s2)
k = ((z1-z2) * pow(s1-s2, -1, n)) % n


# d = (s1*k-z1)/r
d = ((s1*k - z1) * pow(r,-1,n)) % n


print("k =",hex(k))
print("private key =",hex(d)[2:])
print("flag:")
print("boroCTF{" + hex(d)[2:] + "}")