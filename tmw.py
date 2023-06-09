import json
import requests
import base64
import sys

class TmwApi:

    def __init__(self):
        self.BASE_URL = 'https://trc.tmwcloud.com/AMSApp/Integration/System/Unit'
        self.POST_URL = 'https://trc.tmwcloud.com/AMSApp/Integration/Mobile/MeterReading'
        self.username = "apiauth"
        self.password = "%s5znmM9qZRh%*"
        self.headers = {
        'Authorization': 'Basic ' + base64.b64encode((self.username + ':' + self.password).encode()).decode(),
        'Content-Type': 'application/json'
        }

    def get_active_tractors(self):
        res = requests.get(self.BASE_URL, headers=self.headers)

        list = []
        with open('tmw_raw.json', 'w') as f:
            json.dump(res.json()["Units"], f, indent=4)
        for unit in res.json()['Units']:
            if unit['Status'] == "ACTIVE" and unit['Type'] == 'TRACTOR':
                data = {
                    'UnitNumber': unit["UnitNumber"],
                    'SerialNo': unit['SerialNo']
                }
                list.append(data)

        with open('tmw.json', 'w') as f:
            json.dump(list, f, indent=4)
        return list
    
    def get_meter_reading(self, unitnumber, metertype):
        params = {
            "UnitNumber":  unitnumber,
            "MeterType": metertype
        }
        res = requests.get(self.POST_URL, headers=self.headers, params=params)
        return res.json()

    
    def post_new_data(self, id, meterType, Reading, ReadDate):
        self.post_params = {
            "UnitId": "-1",
            "UnitNumber": "1601",
            "MeterType": "ODOMETER",
            "MeterReading": "1000000",
            "MeterDate": "2023-03-24T19:11:28Z"
        }
        res = requests.post(self.POST_URL, headers=self.headers, params=self.post_params)
        return res.status_code, res.json()
    
a = TmwApi()
a.get_meter_reading('1601', 'ODOMETER')

