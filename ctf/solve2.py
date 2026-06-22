import requests
from ecdsa import ellipticcurve, curves


TARGET = "http://192.241.175.41:5000"


curve = curves.SECP256k1
G = curve.generator
n = curve.order


def get_pubkey():
    return requests.get(
        TARGET + "/pubkey"
    ).json()


def get_signature():
    return requests.post(
        TARGET + "/sign",
        json={"message":"A"}
    ).json()


def recover(sig, pub):

    h = int(sig["h"])
    r = int(sig["r"])
    s = int(sig["s"])

    nonce_msb = int(sig["nonce_msb"])

    unknown = int(pub["unknown_bits"])

    pub_x = int(pub["pub_x"])
    pub_y = int(pub["pub_y"])


    print("[+] unknown bits:", unknown)

    rinv = pow(r, -1, n)


    # k = leaked_part || unknown_part
    for low in range(1 << unknown):

        k = (nonce_msb << unknown) | low


        # d = (s*k-h)/r mod n
        d = ((s*k - h) * rinv) % n


        Q = d * G


        if Q.x() == pub_x and Q.y() == pub_y:

            print("\n[+] PRIVATE KEY FOUND")
            print(hex(d))

            print("\n[+] nonce")
            print(k)

            return d


    print("[-] failed")
    return None



def main():

    pub = get_pubkey()

    print("[+] curve:", pub["curve"])

    sig = get_signature()

    print("[+] signature")
    print(sig)


    d = recover(sig, pub)


    if d:
        print("\nNow forge signature with private key")


if __name__ == "__main__":
    main()