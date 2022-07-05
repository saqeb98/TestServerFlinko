import time
from aifc import Error

import requests
import json

class Execution_Failure(Error):
    pass

def login(mail, password):
    s = requests.Session()
    payload = {
        'emailId': mail,
        'password': password,
    }
    logurl = 'https://app.flinko.com:8101/optimize/v1/public/user/signin'
    head = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    resp = requests.post(logurl, json=payload)
    tk = json.loads(resp.content)
    token = tk['responseObject']['access_token']
    head["Authorization"] = "Bearer " + token

    suiteid = 'SUITE1015'
    pes = s.post('http://10.10.10.172:8109/optimize/v1/dashboard/execution/suite/' + suiteid, headers=head)
    out = json.loads(pes.content)
    exid = out['responseObject']['id']

    time.sleep(2)
    sc = 0
    fr1 = 0
    while (sc < 1):
        r1 = s.get('http://10.10.10.172:8109/optimize/v1/dashboard/execution/' + exid, headers=head)
        c1 = json.loads(r1.content)
        fr1 = c1['responseObject']['executionStatus']
        print('status : ' + fr1 + '......')
        if (fr1 == "Completed" or fr1 == "Terminated" or fr1 == "Warning"):
            if fr1 == 'Completed':
                r2 = s.get('http://10.10.10.172:8110/optimize/v1/executionResponse/result/' + exid, headers=head)
                c2 = json.loads(r2.content)
                fr2 = c2['responseObject']['suiteStatus']
                if fr2 == 'FAIL':
                    raise Test_Failed
                else:
                    print("End Result : " + "Test Passed")
                sc = 1
            elif (fr1 == "Terminated" or fr1 == 'Warning'):
                print("End Result : " + fr1)
                sc = 1
        time.sleep(10)
login('mohammed.saqeb@testyantra.com', 'Password@123')
