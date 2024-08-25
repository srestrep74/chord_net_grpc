import hashlib

def sha1_hash(key):
    hash = int(hashlib.sha1(key.encode('utf-8')).hexdigest(), 16) % (2**6)
    print(hash)
    return hash