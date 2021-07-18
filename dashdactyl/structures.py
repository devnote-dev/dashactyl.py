# Dashdactyl.py Class Structures
from .api import Dashdactyl
from .managers import CoinsManager, ResourceManager, DashServerManager


__all__ = ['DashUser', 'DashServer']

class DashUser:
    '''Represents a Dashdactyl-Pterodactyl User.
    
    TODO: additional helper methods for resources
    '''
    def __init__(self, client: Dashdactyl, data: dict):
        att = data['userinfo']['attributes']
        self.client = client
        self.id = att['id']
        self.uuid = att['uuid']
        self.admin = att['root_admin']
        
        self.email = att['email']
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
    
    def remove(self):
        # This should be changed to DELETE...
        return self.client.request('GET', f'/api/remove_account')


# TODO: helper functions for server class
class DashServer:
    def __init__(self, client: Dashdactyl, data: dict):
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
        self.node = att['node']
        self.allocation = att['allocation']
        self.nest = att['nest']
        self.egg = att['egg']
        self.container = att['container']
        self.created_at = att['created_at']
        self.updated_at = att['updated_at'] or None
    
    def get_owner(self):
        return NotImplemented
    
    def set_state(self, state: str):
        return NotImplemented
    
    def modify(self, data: dict):
        return NotImplemented
    
    def delete(self):
        return self.client.request('GET', f'/delete?id={self.id}')
