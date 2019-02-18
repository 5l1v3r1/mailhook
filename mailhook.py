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
        
    print(f'[+] Checking Email ({email}): ', end='')

    if check_email(email):
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
    parser.add_argument('--output-file','-o',
        help='Output file to receive records'
    )
    parser.add_argument('--sleep-time','-s',default=30,
        help='Length of time to sleep between requests (seconds)')

    args = parser.parse_args()

    if args.output_file:
        outfile = open(args.output_file,'w')
    else:
        outfile = None

    if args.email_address: check_and_print(args.email_address)
    elif args.input_file:

        if not Path(args.input_file).exists():

            raise BaseException(
                'Input file doesn\'t exist'
            )

        with open(args.input_file) as infile:

            email = email.strip()
            for email in infile:
                outcome = check_and_print(email.strip())

                if outfile:
                    if outcome: outfile.write('valid:'+email)
                    else: outfile.write('invalid:'+email)

                sleep(args.sleep_time)
    else:
        print('[+] Something screwy happened.')

    if outfile:
        outfile.close()

    print('\nExiting\n')
