import ecdsa

public_keypath = "/home/administrator/v2v-capstone/keys/ecc_public.key"
private_keypath="/home/administrator/v2v-capstone/keys/ecc_private.key"
sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
with open(private_keypath, 'w') as output:
    output.write(sk.to_string())
print(sk.to_string())
vk = sk.get_verifying_key()
with open(public_keypath, 'w') as output:
    output.write(vk.to_string())
print(vk.to_string())
