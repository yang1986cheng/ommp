import base64
import hashlib

def get_check_code(instr):
    hash = hashlib.md5()
    hash.update(instr.strip())
    return base64.encodestring(hash.digest())

print get_check_code('1231')