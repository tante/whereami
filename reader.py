#!/usr/bin/env python        

import oauth2, time, urllib, urllib2, json, datetime

ACCESS = "ACCESS_KEY"
SECRET = "SECRET KEY"
URL = "https://openpaths.cc/api/1" 

def build_auth_header(url, method):
    params = {                                            
        'oauth_version': "1.0",
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': int(time.time()),
    }
    consumer = oauth2.Consumer(key=ACCESS, secret=SECRET)
    params['oauth_consumer_key'] = consumer.key 
    request = oauth2.Request(method=method, url=url, parameters=params) 
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    request.sign_request(signature_method, consumer, None)
    return request.to_header()

params = {"num_points": 1}    # get the last entry
query = "%s?%s" % (URL, urllib.urlencode(params))
try:
    request = urllib2.Request(query)
    request.headers = build_auth_header(URL, 'GET')
    connection = urllib2.urlopen(request)
    data = json.loads(''.join(connection.readlines()))[0]
    with open("template.html") as f:
        template = f.read()

    with open("where.html","w") as f:
        output = template.replace('$lat',str(data['lat']))
        output = output.replace("$lng",str(data['lon']))
        output = output.replace("$time",datetime.datetime.fromtimestamp(data['t']).strftime("%H:%M, %a %b %d"))
        f.write(output)

except urllib2.HTTPError as e:
    print(e.read())
