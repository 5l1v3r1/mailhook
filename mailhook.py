import argparse
from pathlib import Path
from requests import post
from re import escape,compile,search
from sys import exit


VALID_STRING    = 'E-mail address is valid'
INVALID_STRING  = 'E-mail address does not exist on this server'
URL             = 'http://mailtester.com/testmail.php'

valid_reg       = compile(escape(VALID_STRING)) 

def check_email(email):
    
    resp = post(
        URL,data={'lang':'en','email':email}
    )

    if resp and search(valid_reg, resp.text):
        return True
    else:
        return False

def check_and_print(email):
        
    print(f'[+] Checking Email ({args.email_address}): ', end='')

    if check_email(args.email_address):
        print('Valid')
        return 1
    else:
        print('Invalid')
        return 0

if __name__ == '__main__':

    print('\nStarting the script...\n')

    parser = argparse.ArgumentParser(
        description='Test some emails against mailtester.com'
    )
    mexc = parser.add_mutually_exclusive_group(required=True)
    mexc.add_argument('--email-address','-e',
        help='Single email to check.')
    mexc.add_argument('--input-file','-i',
        help='File containing newline delimited email addresses',
    )

    args = parser.parse_args()

    if args.email_address: check_and_print(args.email_address)
    elif args.input_file:

        if not Path(args.input_file).exists():

            raise BaseException(
                'Input file doesn\'t exist'
            )

        with open(args.input_file) as infile:

            for email in infile:

                outcome = check_and_print(email)
    else:
        print('[+] Something screwy happened.')

    print('\nExiting\n')
