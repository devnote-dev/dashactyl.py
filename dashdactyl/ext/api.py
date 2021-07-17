import requests
from json import dumps
from .structures import DashUser


class Dashdactyl:
    '''# Dashdactyl.py
    ### An interactive API wrapper for Dashdactyl in Python.
    '''
    def __init__(self, domain: str, auth: str):
        self.domain = domain
        self.auth = 'Bearer '+ auth
    
    def request(self, method: str, path: str, params: dict={}) -> dict:
        if method not in ('GET', 'POST', 'DELETE'):
            raise ValueError("method must be 'GET', 'POST', or 'DELETE'.")
        
        req = requests.get
        if method == 'POST':
            req = requests.post
        elif method == 'DELETE':
            req = requests.delete
        
        path = self.domain + path
        if len(params):
            params = dumps(params)
        else:
            params = None
        
        res = req(path,
                    data=params,
                    headers={'Content-Type': 'application/json',
                            'Authorization': self.auth})
        
        if 200 >= res.status_code < 400:
            return res.json()
        
        return {'status': 'failed', 'code': res.status_code}
    
    def get_user(self, id: str) -> DashUser:
        data = self.request('GET', f'/api/userinfo/?id={id}')
        if data['status'] != 'success':
            return 'Invalid User ID'
        
        return DashUser(self, data)
    
    def get_server(self, id: str):
        # Not implemented on Dashdactyl's side yet, but I will
        # look into interacting with ptero directly for this
        # in the future.
        return NotImplemented
