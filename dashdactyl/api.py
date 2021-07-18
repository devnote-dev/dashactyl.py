import requests
from json import dumps
from .managers import DashServerManager, CouponManager
from .structures import DashUser


class Dashdactyl:
    '''# Dashdactyl.py
    ### An interactive API wrapper for Dashdactyl in Python.
    '''
    def __init__(self, domain: str, auth: str):
        self.domain = domain
        self.auth = 'Bearer '+ auth
        
        self.users = None # haven't created user manager yet
        self.servers = DashServerManager(self)
        self.coupons = CouponManager(self)
    
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
        
        if res.ok:
            if res.status_code == 204:
                return {'status': 'success'}
            
            return res.json()
        
        return {'status': 'failed',
                'code': res.status_code,
                'message': res.reason}
    
    def ping(self):
        return self.request('GET', '/api')
    
    def get_user(self, id: str) -> DashUser:
        data = self.request('GET', f'/api/userinfo/?id={id}')
        if data['status'] != 'success':
            return 'Invalid User ID'
        
        return DashUser(self, data)
