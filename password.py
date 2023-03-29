import secrets
import string

def num_there(s):
    return any(i.isdigit() for i in s)

def create_password(length=12, uppercase=True, lowercase=True,
                    punctuation=False, digits=True, dashes=True, constraints = True):
    """ Create a password """
    chars = ''
    dash_chars = '_-'
    password = ''

    if digits: chars += string.digits
    if uppercase: chars += string.ascii_lowercase
    if lowercase: chars += string.ascii_uppercase
    if punctuation: chars += string.punctuation
    if dashes: chars += dash_chars
    chars = "".join(set(chars))

    password_ok =  False

    while not password_ok:
        password = ''.join(secrets.choice(chars) for i in range(length))
        if not constraints: break
        password_ok = True

        # password not OK if should contain both upper and lower case letters & does not
        if length > 1 and (lowercase and uppercase) and (password.lower() == password):
            password_ok = False

        # password not ok if should contain at least one dash & does not
        if dashes:
            dash_found = False
            for c in dash_chars:
                if c in password:
                    dash_found = True
                    break
            if not dash_found:
                password_ok = False

        # password not OK if should contain a number and does not.
        if digits and not num_there(password):
            password_ok = False

    return password

def main():
    print(create_password())

if __name__ == '__main__':
    main()
