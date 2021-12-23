# Dashdactyl.py Class Structures
from . import MAX_AMOUNT, CoinsManager, ResourceManager, DashUserServerManager
from typing import Optional


__all__ = ('DashUser', 'DashServer', 'Coupon')

class DashUser:
    '''Represents a Dashactyl-Pterodactyl User.'''
    def __init__(self, client, data: dict):
        att = data['userinfo']['attributes']
        self.client = client
        self.id: int = att['id']
        self.uuid: str = att['uuid']
        self.is_admin: bool = att['root_admin']
        
        self.email: str = att['email']
        self.username: int = att['username']
        self.firstname: str = att['first_name']
        self.lastname: str = att['last_name']
        
        self.language: str = att['language']
        self.tfa: bool = att['2fa'] or False
        
        self.created_at: str = att['created_at']
        self.updated_at: str = att['updated_at'] or None
        
        self.coins = CoinsManager(client, self, data)
        self.servers = DashUserServerManager(client, self, att)
        self.resources = ResourceManager(self, data)
    
    @property
    def tag(self) -> str:
        return self.firstname + self.lastname
    
    def remove(self):
        '''Removes (or deletes) the user's account. Returns `None` on success.'''
        res = self.client.request('DELETE', f'/api/removeaccount/{str(self.id)}')
        if res['status'] != 'success':
            raise Exception('failed deleting user account')
        
        del self.client.users.cache[self.uuid]
        return None


# TODO: helper functions for server class
# TODO: DashServerResourceManager class
class DashServer:
    def __init__(self, client, data: dict):
        att = data['attributes']
        self.client = client
        self.id: int = att['id']
        self.uuid: str = att['uuid']
        self.identifier: str = att['identifier']
        self.name: str = att['name']
        self.description: str = att['description']
        self.status: str = att['status'] or None
        self.is_suspended: bool = att['suspended']
        self.limits: dict = att['limits']
        self.feature_limits: dict = att['feature_limits']
        self.user: int = att['user']
        self.owner: DashUser = None
        self.node: int = att['node']
        self.allocation: int = att['allocation']
        self.nest: int = att['nest']
        self.egg: int = att['egg']
        self.container: dict = att['container']
        self.created_at: str = att['created_at']
        self.updated_at: str = att['updated_at'] or None
    
    def get_owner(self) -> Optional[DashUser]:
        '''Gets the owner of the server. May return `None` if not available.'''
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
                cpu: float=None):
        '''`ram` - The amount of RAM to set
        
        `disk` - The amount of disk to set
        
        `cpu` - The amount of CPU to set
        
        Modifies the RAM, disk, or CPU of the server. Returns the modified server on success.
        '''
        if (0 < ram > MAX_AMOUNT or
            0 < disk > MAX_AMOUNT or
            0 < cpu > MAX_AMOUNT):
            raise ValueError('server specs params must be between 1 and 9 hundred-trillion')
        
        res = self.client.request('GET', f'/modify?id={self.id}&ram={ram}&disk={disk}&cpu={cpu}')
        if res['status'] != 'success':
            return res
        
        return self
    
    def delete(self):
        '''Deletes the server. Returns `None` on success.'''
        if not self.owner:
            self.get_owner()
        
        res = self.client.request('DELETE', f'/api/deleteserver/{str(self.owner.id)}/{str(self.id)}')
        if res['status'] != 'success':
            return res
        
        return None


class Coupon:
    def __init__(self, data: dict):
        self.code: str = data['code']
        self.coins: int = data['coins'] or 0
        self.ram: float = data['ram'] or 0
        self.disk: float = data['disk'] or 0
        self.cpu: float = data['cpu'] or 0
        self.servers: int = data['servers'] or 0
