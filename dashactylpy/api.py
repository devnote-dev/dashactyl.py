import requests
from json import dumps
from time import time
from .managers import DashUserManager, DashServerManager, CouponManager


__all__ = ('Dashactyl')

class Dashactyl:
    '''# Dashactyl.py
    ### An interactive API wrapper for Dashactyl in Python.
    '''
    def __init__(self, domain: str, auth: str):
        '''`domain` - The Dashactyl panel domain

        `auth` - The authentication key for the Pterodactyl panel
        
        Creates a new client to interact with Dashactyl.
        '''
        self.domain = domain.removesuffix('/')
        self.auth = 'Bearer '+ auth
        
        self.users = DashUserManager(self)
        self.servers = DashServerManager(self)
        self.coupons = CouponManager(self)
    
    def request(self, method: str, path: str, params: dict={}) -> dict:
        '''### Not for public use.
        
        `method` - The HTTP method for the request
        
        `path` - The path to request
        
        `params` - Optional additional parameters for the request
        
        Performs an API request to the path then returns a dict response.
        '''
        if method not in ('GET', 'POST', 'PATCH', 'DELETE'):
            raise ValueError("method must be 'GET', 'POST', 'PATCH', or 'DELETE'.")
        
        req = requests.get
        if method == 'POST':
            req = requests.post
        elif method == 'PATCH':
            req = requests.patch
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
    
    def ping(self) -> float:
        '''Pings the Dashactyl API.'''
        start = time()
        self.request('GET', '/api')
        return time() - start
