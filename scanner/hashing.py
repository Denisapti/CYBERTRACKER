import hashlib

def sha256_file(path): # Computes the SHA-256 hash of a file.
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
