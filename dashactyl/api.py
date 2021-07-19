import requests
from json import dumps
from .managers import DashServerManager, DashUserManager, CouponManager


class Dashactyl:
    '''# Dashactyl.py
    ### An interactive API wrapper for Dashactyl in Python.
    '''
    def __init__(self, domain: str, auth: str):
        self.domain = domain
        self.auth = 'Bearer '+ auth
        
        self.users = DashUserManager(self)
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
