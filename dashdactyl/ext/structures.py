# Dashdactyl.py Class Structures
from .managers import CoinsManager, ResourceManager


class DashUser:
    '''Represents a Dashdactyl-Pterodactyl User.
    
    TODO: additional helper methods for resources
    '''
    def __init__(self, client, data):
        att = data['userinfo']['attributes']
        self.id = att['id']
        self.uuid = att['uuid']
        self.admin = att['root_admin']
        
        self.username = att['username']
        self.email = att['email']
        self.firstname = att['first_name']
        self.lastname = att['last_name']
        
        self.language = att['language']
        self.tfa = att['2fa'] or False
        
        self.created_at = att['created_at']
        self.updated_at = att['updated_at'] or None
        
        self.coins = CoinsManager(client, self)
        self.servers = [DashServer(s) for s in att['relationships']['servers']['data']]
        self.resources = ResourceManager(self, data)


# TODO: helper functions for server class
class DashServer:
    def __init__(self, data):
        att = data['attributes']
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
        return NotImplemented
