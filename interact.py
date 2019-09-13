import sys, re
import json, datetime
import requests

# get url
ossim_url = "https://siem.e-cyber.ee"
url_channel = "https://chat.googleapis.com/v1/spaces/AAAAz9u"

# function login
def interact():
    # login
    url = ossim_url + "/ossim/session/login.php"
    with requests.Session() as s:
        payload = {
            'user': 'admin',
            'passu': 'admin',
            'pass': 'YWRtaW4K'
        }
        req = s.post(url, data=payload, verify=False)
            # condition login
        if "Wrong user or password" in req.text:
            sendLog('Login','Login Fail!')
            return

        headers = s.headers
        print "========================================================================"
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
        print "=======================Token====================" + token
        
        # upload file
        url = ossim_url + "/ossim/av_asset/asset/controllers/import_all_hosts_ajax.php"
        data = {
            'ctx': token,
            'import_type': 'hosts',
            'checkbox': '1',
            'send': 'Import'
        }

        try:
            files = {'file_csv':('serverlist.csv', open('serverlist.csv', 'rb'),'text/csv')}
        except:
            sendLog('File','Not found file !')
            return
        
        req = s.post(url, files=files, data=data, verify=False)
        #print(requests.Request('POST', url, files=files).prepare().body.decode('ascii'))
        if ("parent.import_assets_csv('hosts')" not in req.text):
            sendLog('Upload','Fails upload')
            return

        #print s.headers
        #print req.content
            # response
        url = ossim_url + "/ossim/av_asset/asset/views/import_all_hosts.php"
        payload = {
            'import_assets': '1',
            'ctx': token,
            'import_type': 'hosts'
        }

        req = s.post(url, data=payload, verify=False)
        print "handle"
        handle_sumary_post(req.content)
        print (req.content)
        
def handle_sumary_post(strings):
    print "chay vao"
    str_json = json.loads(strings)
    status = str_json['data']['general']['data']
    print status
    if ('All assets have been successfully imported' in str(status)):
        sendLog('Result','Import OK!')
    elif ('Result','Headers not found' in str(status)):
        sendLog('Headers file Fails')
    elif ('Result','Some assets cannot be imported' in str(status)):
        sendLog('Some assets cannot be imported')

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

def sendLog(cate, status):
    dt = datetime.datetime.now()
    d = str(dt).split(" ")
    #message = "status"
	print message
    #sendGG(message, message)



interact()
