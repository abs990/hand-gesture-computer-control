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
        resp = requests.get(url,headers=headers)
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
        requests.post(url,headers=headers)

    """
    call executor to close app
    """
    def closeApp(self, app_id):
        url = self.base_endpoint+"/app/"+str(app_id)+"/close"
        requests.post(url,headers=headers)

    """
    call executor to move mouse
    """
    def moveMouse(self, pos_x, pos_y):
        url = self.base_endpoint+"/mouse/move"
        payload = {
            'pos_x': pos_x,
            'pos_y': pos_y
        }
        requests.post(url,json=payload,headers=headers)

    """
    call executor to left click mouse
    """
    def leftClickMouse(self, pos_x, pos_y):
        url = self.base_endpoint+"/mouse/left-click"
        payload = {
            'pos_x': pos_x,
            'pos_y': pos_y
        }
        requests.post(url,json=payload,headers=headers)

    """
    call executor to right click mouse
    """
    def rightClickMouse(self, pos_x, pos_y):
        url = self.base_endpoint+"/mouse/right-click"
        payload = {
            'pos_x': pos_x,
            'pos_y': pos_y
        }
        requests.post(url,json=payload,headers=headers)