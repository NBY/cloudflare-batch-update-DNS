# !/usr/bin/python
# coding:utf-8

import csv
import requests
import json

content = '1.1.1.1' # supprot ip / domain
proxied = True  # proxy status True/False
type = 'A' # supprot A/CNAME...etc
cloudflare_auth_key = 'YOUR_CLOUDFLARE_KEY' 
cloudflare_auth_email = 'YOUR_CLOUDFLARE_EMAIL'
csvFile = open("data.csv", "r") 

headers = {
    "X-Auth-Email": cloudflare_auth_email,
    "X-Auth-Key": cloudflare_auth_key,
    "Content-Type": 'application/json'
}

def zoneid(cmd):
    id = os.system('curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=' \
                   + cmd + '&status=active" -H "X-Auth-Email:' + cloudflare_auth_email + \
                   '" -H "X-Auth-Key:' + cloudflare_auth_key + \
                   '" -H "Content-Type: application/json" | jq -r "{"result"}[] | .[0] | .id" > zoneid')
    with open('zoneid') as f:
        for data in f.readlines():
            data = data.strip('\n')
    return data

def dnsid(a, b):
    did = os.system('curl -s -X GET "https://api.cloudflare.com/client/v4/zones/' + \
                    a + '/dns_records?type=A&name=' + b + '" -H "X-Auth-Email:' + \
                    cloudflare_auth_email + '" -H "X-Auth-Key:' + cloudflare_auth_key + \
                    '" -H "Content-Type: application/json" | jq -r "{"result"}[] | .[0] | .id"> dnsid')
    with open('dnsid') as f:
        for data in f.readlines():
            data = data.strip('\n')
    return data

reader = csv.reader(csvFile)
for item in reader:
    zid = zoneid(item[0])
    for domain in item[1:]:
        did = (dnsid(zid, domain))
        url = (
                "https://api.cloudflare.com/client/v4/zones/%(zone_id)s/dns_records/%(record_id)s"
                % {"zone_id": zid, "record_id": did}
        )
        payload = {"type": type, "name": domain, "content": content, "ttl": "1", "proxied": proxied}
        response = requests.put(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Update Completed："+domain)
        else:
            print("Update Fail："+domain)

