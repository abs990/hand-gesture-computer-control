import requests

headers = {
    'Content-Type': 'application/json'
}

class Executor:
    def __init__(self, base_endpoint):
        self.base_endpoint = base_endpoint

    """
    call executor to get app name
    """
    def getAppDetails(self, gesture_id):
        url = self.base_endpoint+"/gesture/"+str(gesture_id)+"/app-info"
        resp = requests.get(url,headers)
        if resp.status_code == 404:
            return -1, ""
        else:
            value = resp.json()
            return value['app_id'], value['app_name']

    """
    call executor to open app
    """     
    def openApp(self, app_id):
        url = self.base_endpoint+"/app/"+str(app_id)+"/open"
        requests.post(url,headers)

    """
    call executor to close app
    """
    def closeApp(self, app_id):
        url = self.base_endpoint+"/app/"+str(app_id)+"/close"
        requests.post(url,headers)     