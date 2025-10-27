# passgen.py
import secrets, string

def generate(length=16, use_upper=True, use_digits=True, use_symbols=True):
    alphabet = string.ascii_lowercase
    if use_upper: alphabet += string.ascii_uppercase
    if use_digits: alphabet += string.digits
    if use_symbols: alphabet += "!@#$%^&*()-_=+[]{};:,.<>/?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__=="__main__":
    print(generate(length=20, use_symbols=True))
