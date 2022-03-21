import requests
import hashlib
import sys


def send_request_to_pwnd_api(hashed_password):
    url = 'https://api.pwnedpasswords.com/range/' + hashed_password[:5]
    res = requests.get(url)
    if res.status_code != 200:
        print(f'an error returned, please check the API')
    else:
        return res.text


def hash_function(password):
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    return hashed_password


def check_password_counts(password):
    hashed = hash_function(password).upper()
    result = [key.split(":") for key in send_request_to_pwnd_api(hashed).splitlines()]
    for key in result:
        if key[0] == hashed[5:]:
            return key[1]
    return 0


def main(args):
    for password in args:
        result = check_password_counts(password)
        print(f"Your password {password} is found {result} times")


if __name__ == "__main__":
    main(sys.argv[1:])
