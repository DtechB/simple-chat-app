import hashlib

message = '12345678'.encode()
print(hashlib.sha256(message).hexdigest())
print(hashlib.sha256(message).hexdigest())
