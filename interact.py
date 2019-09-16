import sys, re
import json, datetime
from httplib2 import Http
from json import dumps
import requests

# get url
ossim_url = "https://siem.e-cyber.ee"
url_channel = "https://chat.googleapis.com/v1/spaces/AAAAz9u"
file_path = "serverlist.csv"

# function for send message Google Hangouts
def sendGG(text, url_input):
	url = url_input
	bot_message = {'text' : text}
	message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}
	
	http_obj = Http()
	
	response = http_obj.request(
		uri=url,
		method='POST',
		headers=message_headers,
		body=dumps(bot_message),
	)

# function for sendLog 
def sendLog(cate, status):
    dt = datetime.datetime.now()
    d = str(dt).split(" ")
    message = "```" + d[0] + " | " + d[1] + "  | " + cate + " | [SIEM] File CSV: " + status + "!```"
    sendGG(message, url_channel)

# function login
def interact():
    # login
    url = ossim_url + "/ossim/session/login.php"
    with requests.Session() as s:
        payload = {
            'user': 'admin',		# example
            'passu': 'admin',		# example
            'pass': 'YWRtaW4K=='	# base64 for passwd
        }
        req = s.post(url, data=payload, verify=False)
            # condition login
        if "Wrong user or password" in req.text:
            sendLog('Login','Login Fail!')
            return

        headers = s.headers
            # get TOKEN
        req = s.get(ossim_url + '/ossim/av_asset/asset/views/import_all_hosts.php')
        token = req.text
        if ("ctx" not in token):
            sendLog('Login','Not get TOKEN')
            return

        for line in token.split("\n"):
            if "ctx" in line:
                token = re.findall('(([0-9A-F]){16,32})',line)[0][0]
                break
        
            # upload file
        url = ossim_url + "/ossim/av_asset/asset/controllers/import_all_hosts_ajax.php"
        data = {
            'ctx': token,
            'import_type': 'hosts',
            'checkbox': '1',
            'send': 'Import'
        }

        try:
            files = {'file_csv':(file_path, open(file_path, 'rb'),'text/csv')}
        except:
            sendLog('File','Not found file !')
            return
        
        req = s.post(url, files=files, data=data, verify=False)
        if ("parent.import_assets_csv('hosts')" not in req.text):
            sendLog('Upload','Fails upload')
            return

            # response
        url = ossim_url + "/ossim/av_asset/asset/views/import_all_hosts.php"
        payload = {
            'import_assets': '1',
            'ctx': token,
            'import_type': 'hosts'
        }

        req = s.post(url, data=payload, verify=False)
        handle_sumary_post(req.content)

# function for get line error from file csv
def getLineInFile(arr_id):
    f=open(file_path)
    lines=f.readlines()
    result = "This is line: \n"
    for i in arr_id:
        result = result + "```" +lines[i] + "```\n"
    return result

# function handle status for implement upload file asset
def handle_sumary_post(strings):
    str_json = json.loads(strings)
    print "[x] " + str(str_json)
    status = str_json['data']['general']['data']

    if ('All assets have been successfully imported' in str(status)):
        sendLog('Result','Import OK!')
    elif ('Headers not found' in str(status)):
        sendLog('Result','Headers file Fails')
    elif ('Some assets cannot be imported' in str(status)):
        sendLog('Result','Some assets cannot be imported')
        total = str_json['data']['general']['statistics']['total']
        arr_id = []
        for i in range (1, total + 1):
            status = str_json['data']['by_hosts'][str(i)]['status']
            if ("error" in status):
                arr_id.append(i)
        result = getLineInFile(arr_id)
        sendGG(result, url_channel)


interact()
