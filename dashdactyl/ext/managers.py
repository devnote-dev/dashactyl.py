from .api import Dashdactyl
from .structures import DashUser
from typing import Union


class CoinsManager:
    def __init__(self, client: Dashdactyl, user: Union[int, DashUser]):
        self.client = client
        self.user = user
    
    def __call__(self) -> int:
        if isinstance(self.user, DashUser):
            return self.user.coins
        else:
            return -1
    
    def add(self, amount: int) -> bool:
        if not self.user:
            raise Exception('no user specified')
        
        user = self.user
        if isinstance(self.user, DashUser):
            user = self.user.username
        
        if 0 < amount > int('9' * 15):
            raise ValueError('amount must be between 1 and 9 hundred-trillion')
        
        res = self.client.request('POST', '/api/addcoins', {'id': str(user), 'amount': amount})
        if res['status'] != 'success':
            return False
        else:
            return True
    
    def remove(self, amount: int) -> bool:
        if not self.user:
            raise Exception('no user specified')
        
        user = self.user
        if isinstance(self.user, DashUser):
            user = self.user.username
        else:
            user = self.client.get_user(self.user)
        
        if not user:
            raise Exception()
        
        amount = user.coins - amount
        if amount < 0:
            amount = 0
        
        if 0 < amount > int('9' * 15):
            raise ValueError('amount must be between 1 and 9 hundred-trillion')
        
        res = self.client.request('POST', '/api/setcoins', {'id': str(user), 'amount': amount})
        if res['status'] != 'success':
            return False
        else:
            return True
    
    def set(self, amount: int) -> bool:
        if not self.user:
            raise Exception('no user specified')
        
        user = self.user
        if isinstance(self.user, DashUser):
            user = self.user.username
        
        if 0 < amount > int('9' * 15):
            raise ValueError('amount must be between 1 and 9 hundred-trillion')
        
        res = self.client.request('POST', '/api/setcoins', {'id': str(user), 'amount': amount})
        if res['status'] != 'success':
            return False
        else:
            return True


# TODO: helper methods for resources
class ResourceManager:
    def __init__(self, user: Union[int, DashUser], data: dict):
        self.user = user
        self.__patch(data)
    
    def __call__(self) -> dict:
        return {'ram': self.ram,
                'disk': self.disk,
                'cpu': self.cpu,
                'servers': self.servers}
    
    def __patch(self, data):
        self.ram = data['package']['ram']
        self.disk = data['package']['disk']
        self.cpu = data['package']['cpu']
        self.servers = data['package']['servers']
        
        if data['extra']:
            self.ram += data['extra']['ram']
            self.disk += data['extra']['disk']
            self.cpu += data['extra']['cpu']
            self.servers += data['extra']['servers']
    
    # Functions below this method WONT be implemented until Dashdactyl
    # updates the API methods for the respective endpoints:
    # -> add = POST
    # -> remove = PATCH
    # -> set = PUT
    
    def add(self,
            ram: float=None,
            disk: float=None,
            cpu: float=None,
            servers: int=None):
        return NotImplemented
    
    def remove(self,
                ram: float=None,
                disk: float=None,
                cpu: float=None,
                servers: int=None):
        return NotImplemented
    
    def set(self,
            ram: float=None,
            disk: float=None,
            cpu: float=None,
            servers: int=None,
            package: str=None):
        return NotImplemented
