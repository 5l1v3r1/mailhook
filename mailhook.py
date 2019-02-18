import argparse
from pathlib import Path
from requests import post
from re import escape,compile,search
from sys import exit
from time import sleep

VALID_STRING    = 'E-mail address is valid'
INVALID_STRING  = 'E-mail address does not exist on this server'
BLOCKED_STRING  = 'Too many invalid recipients'
URL             = 'http://mailtester.com/testmail.php'

valid_reg       = compile(escape(VALID_STRING)) 
blocked_reg     = compile(escape(BLOCKED_STRING))
invalid_reg     = compile(escape(INVALID_STRING))

DEFAULT_SLEEP_TIME          = 45
DEFAULT_BLOCKED_SLEEP_TIME  = 60*20

def check_email(email,verbose=True):
    '''
    Use mailtester.com to check if a given email address is valid. Will
    perform an extended sleep should a block detection occur.
    '''

    # ====================================
    # MAKE REQUEST AND HANDLE SERVER BLOCK
    # ====================================

    resp = make_request(email)
    if search(blocked_reg, resp.text):
        resp = blocked_loop(email)

    # ==============
    # VALIDATE EMAIL
    # ==============

    if resp and search(valid_reg, resp.text):
        known_valid = email
        outcome = True
    else:
        outcome = False

def blocked_loop(email):
    '''
    Loop until the server has been unblocked.
    '''

    # ================================================
    # USE VALID EMAIL IF KNOWN, USE ORIGINAL OTHERWISE
    # ================================================

    if known_valid: test_email = known_valid
    else: test_email = email

    while True:
        
        print('[+] Blocked by server! Sleeping for '\
              f'{args.blocked_sleep_time} seconds')

        # ==============
        # EXTENDED SLEEP
        # ==============

        sleep(args.blocked_sleep_time)

        print('[+] Awake!')

        # ==================================
        # REQUEST AN EMAIL KNOWN TO BE VALID
        # ==================================

        kresp = make_request(test_email)
        if search(blocked_reg, kresp.text):
            continue
        else:
            return make_request(email)

    return resp

def make_request(email):

    return post(
        URL,data={'lang':'en','email':email}
    )

if __name__ == '__main__':

    print('\nStarting the script...\n')

    # ========================
    # BUILD THE DAMN INTERFACE
    # ========================

    parser = argparse.ArgumentParser(
        description='Test some emails against mailtester.com'
    )
    mexc = parser.add_mutually_exclusive_group(required=True)
    mexc.add_argument('--email-address','-e',
        help='Single email to check.')
    mexc.add_argument('--input-file','-i',
        help='File containing newline delimited email addresses',)
    parser.add_argument('--output-file','-o',
        help='Output file to receive records')
    parser.add_argument('--print-invalid','-pi',action='store_true',
        help='Determine if invalid emails should be printed to stdout')
    parser.add_argument('--sleep-time','-s',default=45,
        help='Length of time to sleep between requests '\
            f'in seconds. (Default: {DEFAULT_SLEEP_TIME})')
    parser.add_argument('--blocked-sleep-time','-b',default=60*20,
        help='Length of time to sleep after being blocked by the server '\
            f'in seconds. (Default: {DEFAULT_BLOCKED_SLEEP_TIME})')
    parser.add_argument('--resume-log','-r',
        help='Output file of interrupted execution. Avoids duplicate requests.')

    args = parser.parse_args()

    print(f'[+] Sleep time is currently set to: {args.sleep_time}')
    print(f'[+] Blacklist sleep time is set to: {args.blocked_sleep_time}')

    known_valid = None
    last_email = None
    logs = []

    # ================================
    # READ LOGS AND FIND A VALID EMAIL
    # ================================
    # - slurps up a log file
    # - reads each record to the logs list
    # - final email is captured in last_email
    # - all previous logs are rewritten to the target log file

    if args.resume_log:

        # TEST EXISTANCE OF LOG FILE
        if not Path(args.resume_log).exists():
            raise Exception(
                'Resume log doesn\'t exist!'
            )
        
        # OPEN LOG FILE
        with open(args.resume_log) as log:
            for r in log:
                r = r.strip()               # STRIP WHITESPACE
                logs.append(r)              # CAPTURE RECORD
                esplit = r.split(':')       # SPLIT THE EMAIL
                last_email = esplit[1]      # CAPTURE LAST EMAIL

                # Capture at least one known valid from the log file
                if not known_valid and esplit[0] == 'valid':
                    known_valid = esplit[1]
                    print(f'[+] A valid email was found: {known_valid}')


        if last_email:
            print(f'[+] Last email tested: {last_email}')
    
    # =======================================
    # OPEN OUTPUT FILE & HANDLE ATTACK RESUME
    # =======================================
    
    # PREPARE OUTPUT FILE
    if args.output_file:
        outfile = open(args.output_file,'w')
    else:
        outfile = None

    # WRITING PREVIOUS LOGS TO DISK
    if logs:
        [outfile.write(l+'\n') for l in logs]

    # =========
    # MAIN LOOP
    # =========

    if args.email_address: check_email(args.email_address)
    elif args.input_file:

        if not Path(args.input_file).exists():

            raise BaseException(
                'Input file doesn\'t exist'
            )

        # =======================
        # PREPARE RESUMPTION FLAG
        # =======================
        #
        # True indicates that any additional emails should be checked
        #

        if last_email: resumed = False
        else: resumed = True

        # ===========================================
        # BEGIN ITERATING OVER TARGET EMAIL ADDRESSES
        # ===========================================

        with open(args.input_file) as infile:

            for email in infile:

                email = email.strip()

                # =======================================
                # CONTINUE LOOPING UNTIL RESUMPTION EMAIL
                # =======================================

                if not resumed and (last_email == email):
                    resumed = True
                    continue        # AVOID RECHECK OF EMAIL
                elif not resumed:   # CONTINUE UNTIL RESUME FLAG
                    continue
                
                # =======================
                # CHECK THE EMAIL ADDRESS
                # =======================

                outcome = check_email(email)

                if outcome:
                    print(f'valid: {email}')
                elif args.print_invalid:
                    print(f'invalid: {email}')

                # ===========
                # OUTPUT LOGS
                # ===========

                if outfile:

                    if outcome: outfile.write('valid:'+email+'\n')
                    else: outfile.write('invalid:'+email+'\n')

                    outfile.flush()

                # =============================
                # SLEEP FOR SOME PERIOD OF TIME
                # =============================

                sleep(args.sleep_time)

    # =====================
    # CLOSE THE OUTPUT FILE
    # =====================

    if outfile:
        outfile.close()

    print('\nExiting\n')
