# Ionos DDNS update script
This is a simple set of scripts that allows the user to obtain the internal ID used by Ionos to identify DNS zones and domain records registered to their account, and then automatically update one or more records using a script set to run with `crontab` or a similar scheduler.

## Setup
The scripts rely on a single .env file in the same directory as the script. This .env file should have the following variables:

```
API_KEY=[your key]
API_KEY_PUBLIC=[your public prefix]
ZONE_ID=[your zone ID]
DOMAIN_ID=[your domain ID]
```

`ZONE_ID` and `DOMAIN_ID` can be obtained using the `get_record_ids.py` script. 

## Automating DNS record updates
The script `ionos_ddns_update.py` updates the DNS record `DOMAIN_ID`, which itself is located within DNS zone `ZONE_ID`. This script can be run at any time - I recommend automating it to run at the desired interval with a tool like `crontab`.