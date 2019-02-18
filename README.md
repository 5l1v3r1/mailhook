# mailhook

Check email addresses against mailtester.com. Unlike other utilities supporting the same functionality, MailHook will detect when a blacklist occurs and will proceed to sleep for a user-specified period of time.

# Reuirements

MailHook requires python3.6 or greater and Python Requests.

# Install

```python3.6
python3.6 -m pip install -r requirements.txt
```

# Description of Functionality

- Supports logging
- Scans are resumable by ingesting a log file and run time
- To avoid blacklisting, sleeps for a given period of time between checks (provided in seconds)
- Detects blacklisting, sleeps for a given period of time to allow blacklist to expire (provided in seconds)

# Sample of Interface

```
root@supercoolhostname:mailhook~> python3.6 mailhook.py --help

Starting the script...

usage: mailhook.py [-h]
                   (--email-address EMAIL_ADDRESS | --input-file INPUT_FILE)
                   [--output-file OUTPUT_FILE] [--print-invalid]
                   [--sleep-time SLEEP_TIME]
                   [--blocked-sleep-time BLOCKED_SLEEP_TIME]
                   [--resume-log RESUME_LOG]

Test some emails against mailtester.com

optional arguments:
  -h, --help            show this help message and exit
  --email-address EMAIL_ADDRESS, -e EMAIL_ADDRESS
                        Single email to check.
  --input-file INPUT_FILE, -i INPUT_FILE
                        File containing newline delimited email addresses
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Output file to receive records
  --print-invalid, -pi  Determine if invalid emails should be printed to
                        stdout
  --sleep-time SLEEP_TIME, -s SLEEP_TIME
                        Length of time to sleep between requests in seconds.
                        (Default: 40)
  --blocked-sleep-time BLOCKED_SLEEP_TIME, -b BLOCKED_SLEEP_TIME
                        Length of time to sleep after being blocked by the
                        server in seconds. (Default: 1800)
  --resume-log RESUME_LOG, -r RESUME_LOG
                        Output file of interrupted execution. Avoids duplicate
                        requests.
```
