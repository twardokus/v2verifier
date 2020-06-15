from fastecdsa.curve import P256
from fastecdsa.keys import export_key, gen_keypair

public_keypath = "/home/user/fastecc_public.key"
private_keypath="/home/user/fastecc_private.key"

priv, pub = gen_keypair(P256)
export_key(priv, curve=P256, filepath=private_keypath)
export_key(pub, curve=P256, filepath=public_keypath)
