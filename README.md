# CORA

```
ada:/import/ada2/ywan3191/cora/scripts/cora > python trigger_event.py -h
usage: VOevent [-h] [-d] [-e EMAIL [EMAIL ...]] [-v] sbid [sbid ...]

VO Event trigger

positional arguments:
  sbid

optional arguments:
  -h, --help            show this help message and exit
  -d, --deposited       check DEPOSITED sbid instead of the default RELEASED sbid
  -e EMAIL [EMAIL ...], --email EMAIL [EMAIL ...]
                        send email notification to a list of email addresses
  -r REFRESH_RATE, --refresh-rate REFRESH_RATE
                        Refresh rate for data checking in unit of seconds. Default is every 10min
  -v, --verbose         make it verbose
```

Quick Usage
`python trigger_event.py <sbid_number> -e <email.address>`

