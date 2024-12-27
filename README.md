# Ionos DDNS update script
This is a simple set of scripts that allows the user to obtain the internal ID used by Ionos to identify DNS zones and domain records registered to their account, and then automatically update one or more records using a script set to run with `crontab` or a similar scheduler.

## Setup
The scripts rely on a single .env file in the same directory as the script. This .env file should have the following variables:

```env
API_KEY=[your key]
API_KEY_PUBLIC=[your public prefix]
ZONE_ID=[your zone ID]
DOMAIN_ID=[your domain ID]
LOGGING=[true or false]
```

`ZONE_ID` and `DOMAIN_ID` can be obtained using the `get_record_ids.py` script. You can obtain an API key from the Ionos developer portal.

## Automating DNS record updates
The script `ionos_ddns_update.py` updates the DNS record `DOMAIN_ID`, which itself is located within DNS zone `ZONE_ID`. This script can be run at any time - I recommend automating it to run at the desired interval with a tool like `crontab`.

The `LOGGING` variable in the environment file enables or disables logging in the `ionos_ddns_update.py` script. Set to `TRUE` or `FALSE`.

An example crontab entry looks like this:
```
0 * * * * cd /home/jacob/ionos_ddns_script && /usr/bin/python3 /home/jacob/ionos_ddns_script/ionos_ddns_update.py
```

Note that I `cd` into the working directory where I want the log file to be located before running the script.