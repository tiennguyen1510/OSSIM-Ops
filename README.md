# OSSIM-Ops

[![JavaScript Style Guide: Good Parts](https://img.shields.io/badge/code%20style-goodparts-brightgreen.svg?style=flat)](https://github.com/dwyl/goodparts "JavaScript The Good Parts")

This tool uses for automation control OSSIM AlienVault. This example for upload asset list servers one way automation.

  - Writing with Python.
  - Interacting with site OSSIM (Because OSSIM not support API).
  - Easy custom and add function.

## Running
1. Setup file list server "serverlist.prod" export from Jenkins
```
SEC-PROD-JP-01	192.168.1.113   172.1.10.97	linode/ubuntu16.04lts	running	14081118	sec-prod-jp-01
```
2. Running file "parse.py" with agrument like command:
```
python parse.py serverlist.prod [more_list]
```
3. Change variables like url for SIEM, Google Hangouts or username, password, base64 for password in file "interact.py".
```
# get url
ossim_url = "https://siem.e-cyber.ee"
url_channel = "https://chat.googleapis.com/v1/spaces/AAAAz9u"
file_path = "serverlist.csv"
...
        payload = {
            'user': 'admin',		# example
            'passu': 'admin',		# example
            'pass': 'YWRtaW4K=='	# base64 for passwd
        }
```

4. Setup crontab.
```
0 5 * * * ssiem	python /home/ssiem/scripts/parse.py serverlist.prod serverlist.dev >> /var/log/siem_uploads.log 2>&1
0 6 * * * ssiem python /home/ssiem/scripts/interact.py >> /var/log/siem_uploads.log 2>&1
```
