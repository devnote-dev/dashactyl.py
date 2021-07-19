# Dashdactyl.py Class Structures
from .api import Dashactyl
from .managers import MAX_AMOUNT, CoinsManager, ResourceManager, DashServerManager


__all__ = ['DashUser', 'DashServer', 'Coupon']

class DashUser:
    '''Represents a Dashactyl-Pterodactyl User.
    
    TODO: additional helper methods for resources
    '''
    def __init__(self, client: Dashactyl, data: dict):
        att = data['userinfo']['attributes']
        self.client = client
        self.id = att['id']
        self.uuid = att['uuid']
        self.admin = att['root_admin']
        
        self.email = att['email']
        self.password = None # Fetch on funcion call
        self.ip = None # Fetch on function call
        self.username = att['username']
        self.firstname = att['first_name']
        self.lastname = att['last_name']
        
        self.language = att['language']
        self.tfa = att['2fa'] or False
        
        self.created_at = att['created_at']
        self.updated_at = att['updated_at'] or None
        
        self.coins = CoinsManager(client, self)
        self.servers = DashServerManager(client, att)
        self.resources = ResourceManager(self, data)
    
    @property
    def tag(self) -> str:
        return self.firstname + self.lastname
    
    def get_ip(self) -> str:
        if self.ip is None:
            res = self.client.request('GET', f'/getip?id=${self.id}')
            if 'status' in res:
                return res
            
            self.ip = res['ip']
            return res['ip']
        
        return self.ip
    
    def get_password(self):
        # I dont know the endpoint for this...
        return NotImplemented
    
    def regen(self):
        # Not implemented on Dashactyl
        return NotImplemented
    
    def remove(self):
        # This should be changed to DELETE...
        return self.client.request('GET', f'/api/remove_account')


# TODO: helper functions for server class
class DashServer:
    def __init__(self, client: Dashactyl, data: dict):
        att = data['attributes']
        self.client = client
        self.id = att['id']
        self.uuid = att['uuid']
        self.identifier = att['identifier']
        self.name = att['name']
        self.description = att['description']
        self.status = att['status'] or None
        self.suspended = att['suspended']
        self.limits = att['limits']
        self.feature_limits = att['feature_limits']
        self.user = att['user']
        self.owner = None # Fetch on function call
        self.node = att['node']
        self.allocation = att['allocation']
        self.nest = att['nest']
        self.egg = att['egg']
        self.container = att['container']
        self.created_at = att['created_at']
        self.updated_at = att['updated_at'] or None
    
    def get_owner(self):
        if not self.owner:
            for user in self.client.users.cache:
                if user.id == self.user:
                    self.owner = user
                    break
        
        return self.owner
    
    def set_state(self, state: str):
        # Not implemented on Dashactyl
        return NotImplemented
    
    def modify(self,
                ram: float=None,
                disk: float=None,
                cpu: float=None) -> bool:
        if (0 < ram > MAX_AMOUNT or
            0 < disk > MAX_AMOUNT or
            0 < cpu > MAX_AMOUNT):
            raise ValueError('server specs params must be between 1 and 9 hundred-trillion')
        
        res = self.client.request('GET', f'/modify?id={self.id}&ram={ram}&disk={disk}&cpu={cpu}')
        if res['status'] != 'success':
            return res
        
        return True
    
    def delete(self) -> bool:
        res = self.client.request('GET', f'/delete?id={self.id}')
        if res['status']:
            return False
        
        return True


class Coupon:
    def __init__(self, data: dict):
        self.code = data['code']
        self.coins = data['coins'] or 0
        self.ram = data['ram'] or 0
        self.disk = data['disk'] or 0
        self.cpu = data['cpu'] or 0
        self.servers = data['servers'] or 0
