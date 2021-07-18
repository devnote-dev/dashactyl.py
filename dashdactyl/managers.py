from .api import Dashdactyl
from .structures import DashServer, DashUser, Coupon
from typing import Union, List


__all__ = ['CoinsManager', 'ResourceManager', 'DashServerManager']

MAX_AMOUNT = int('9' * 15)

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
        
        if 0 < amount > MAX_AMOUNT:
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
        
        if 0 < amount > MAX_AMOUNT:
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
        
        if 0 < amount > MAX_AMOUNT:
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
    
    # Functions below this message WONT be implemented until Dashdactyl
    # updates the API methods for the respective endpoints:
    # - add: POST
    # - remove: PATCH
    # - set: PUT
    
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


class DashServerManager:
    def __init__(self, client: Dashdactyl, *data: Union[dict, DashServer]):
        self.client = client
        self.cache = {}
        self.__patch(*data)
    
    def __patch(self, *data):
        for s in data:
            if isinstance(s, DashServer):
                self.cache[s.uuid] = s
            else:
                s = DashServer(self.client, s)
                self.cache[s.uuid] = s
    
    def resolve(self, data: dict) -> List[DashServer]:
        # only resoles from user data
        if 'relationships' in data:
            # fallback for invalid or malformed data
            raise KeyError('relationships not present in data')
        
        res = []
        for o in data['relationships']['servers']['data']:
            s = DashServer(self.client, o)
            res.append(s)
        
        return res
    
    def get(self, id: str) -> Union[DashServer, None]:
        for k in self.cache.keys():
            if id in k:
                return self.cache[k]
        
        return None
    
    def create(self,
                name: str,
                ram: float,
                disk: float,
                cpu: float,
                egg: str,
                location: str) -> DashServer:
        if (0 < ram > MAX_AMOUNT or
            0 < disk > MAX_AMOUNT or
            0 < cpu > MAX_AMOUNT):
            raise ValueError('server specs params must be between 1 and 9 hundred-trillion')
        
        data = self.client.request('GET',
                                    f'/create?name={name}' \
                                    f'&ram={str(ram)}' \
                                    f'&disk={str(disk)}' \
                                    f'&cpu={str(cpu)}' \
                                    f'&egg={egg}' \
                                    f'&location={location}')
        if data['status'] != 'success':
            return data
        
        s = DashServer(self.client, data)
        self.cache[s.uuid] = s
        return s
    
    def delete(self, id: str) -> dict:
        s = self.get(id)
        if isinstance(s, DashServer):
            del self.cache[s.uuid]
            s.delete()
            del s
            return True
        
        return self.client.request('GET', f'/delete?id={id}')


class CouponManager:
    def __init__(self, client: Dashdactyl):
        self.client = client
        self.cache = {}
    
    def fetch(self, code: str=None):
        # not implemented on Dashdactyl's side
        return NotImplemented
    
    def get(self, code: str):
        # broken because of fetch
        return NotImplemented
    
    def create(self,
                code: str=None,
                coins: int=0,
                ram: float=0,
                disk: float=0,
                cpu: float=0,
                servers: int=0) -> Coupon:
        if (0 < coins > MAX_AMOUNT or
            0 < ram > MAX_AMOUNT or
            0 < disk > MAX_AMOUNT or
            0 < cpu > MAX_AMOUNT or
            0 < servers > 10):
            raise ValueError('amount must be between 1 and 9 hundred-trillion (or servers which is 10)')
        
        if (not code and not (coins or ram or disk or cpu or servers)):
            raise ValueError('no valid parameters provided')
        
        data = self.client.request('POST', '/createcoupon',
                                    {'code': code, 'coins': coins, 'ram': ram, 'disk': disk, 'cpu': cpu, 'servers': servers})
        if 'status' in data:
            return data
        
        c = Coupon(data)
        self.cache[c.code] = c
        return c
    
    def revoke(self, code: str) -> dict:
        if self.get(code):
            del self.cache[code]
        
        return self.client.request('POST', '/revokecoupon', {'code': code})
