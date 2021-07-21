from .api import Dashactyl
from .structures import DashServer, DashUser, Coupon
from typing import Union, Optional, List
from types import FunctionType


__all__ = ['CoinsManager',
            'ResourceManager',
            'DashServerManager',
            'CouponManager',
            'DashUserManager']

MAX_AMOUNT = int('9' * 15)

class DashUserWarning(Exception):
    '''Warning exception for DashUser errors.'''
    pass


class CoinsManager:
    def __init__(self, client: Dashactyl, user: Union[int, DashUser], data: dict):
        '''`client` - The Dashactyl client
        
        `user` - The Dashactyl user the manager is for
        
        Creates a new manager for client coins.
        '''
        self.client = client
        self.user = user
        self.amount = data['coins']
    
    def __call__(self) -> int:
        '''Returns the number of coins the user has or -1 if unavailable.'''
        if isinstance(self.user, DashUser):
            return self.amount
        else:
            return -1
    
    def add(self, amount: int) -> int:
        '''`amount` - The number of coins to add
        
        Adds an amount of coins to the user's account. Returns the added coins on success.
        '''
        if not self.user:
            raise DashUserWarning('user not found')
        
        user = self.user
        if isinstance(self.user, DashUser):
            user = self.user.username
        
        if 0 < amount > MAX_AMOUNT:
            raise ValueError('amount must be between 1 and 9 hundred-trillion')
        
        res = self.client.request('POST', '/api/addcoins', {'id': str(user), 'amount': amount})
        if res['status'] != 'success':
            return res
        
        self.amount += amount
        return self.amount
    
    def remove(self, amount: int) -> int:
        '''`amount` - The number of coins to remove
        
        Removes an amount of coins from the user's account. Returns the removed coins on success.
        '''
        if not self.user:
            raise DashUserWarning('user not found')
        
        user = self.user
        if isinstance(self.user, DashUser):
            user = self.user.username
        else:
            user = self.client.users.get(self.user)
        
        if not user:
            raise DashUserWarning('user not found')
        
        amount = self.amount - amount
        if amount < 0:
            amount = 0
        
        if 0 < amount > MAX_AMOUNT:
            raise ValueError('amount must be between 1 and 9 hundred-trillion')
        
        res = self.client.request('POST', '/api/setcoins', {'id': str(user), 'amount': amount})
        if res['status'] != 'success':
            return res
        
        self.amount = amount
        return self.amount
    
    def set(self, amount: int) -> int:
        '''`amount` - The number of coins to set
        
        Sets the users coins to the specified amount. Returns the set amount of coins on success.
        '''
        if not self.user:
            raise DashUserWarning('user not found')
        
        user = self.user
        if isinstance(self.user, DashUser):
            user = self.user.username
        
        if 0 < amount > MAX_AMOUNT:
            raise ValueError('amount must be between 1 and 9 hundred-trillion')
        
        res = self.client.request('POST', '/api/setcoins', {'id': str(user), 'amount': amount})
        if res['status'] != 'success':
            return res
        
        self.amount = amount
        return self.amount


# TODO: helper methods for resources
class ResourceManager:
    def __init__(self, client: Dashactyl, user: Union[int, DashUser], data: dict):
        '''`client` - The Dashactyl client
        
        `user` - The Dashactyl user the manager is for
        
        `data` - The data to resolve resources from
        
        Creates a new manager for client resources.
        '''
        self.client = client
        self.user = user
        self.__patch(data)
    
    def __call__(self) -> dict:
        '''Returns a dict of the user's resources.'''
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
    
    def setplan(self, package: str):
        return NotImplemented


class DashUserServerManager:
    def __init__(self, client: Dashactyl, *data: Union[dict, DashServer]):
        '''`client` - The Dashactyl client
        
        `data` - The data to resolve servers from
        
        Creates a new manager for client servers.
        '''
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
        '''`data` - The data to resolve servers from
        
        Resolves servers from raw user data.
        '''
        if 'relationships' in data:
            # fallback for invalid or malformed data
            raise KeyError('relationships not present in data')
        
        res = []
        for o in data['relationships']['servers']['data']:
            s = DashServer(self.client, o)
            res.append(s)
        
        return res
    
    def find(self, fn: FunctionType) -> Optional[DashServer]:
        for server in self.cache:
            if fn(server):
                return server
        
        return None
    
    def get(self, id: str) -> Optional[DashServer]:
        '''`id` - The identifier or UUID of the server
        
        Gets a server from the cache, or fetches directly if not available.
        '''
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
        '''`name` - The name of the server
        
        `ram` - The amoout of RAM for the server
        
        `disk` - The amount of disk for the server
        
        `cpu` - The amount of CPU for the server
        
        `egg` - The egg for the server
        
        `location` - The location of the server
        
        Creates a new Pterodactyl server with the specified parameters.
        '''
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
    
    def delete(self, id: str):
        '''`id` - The identifier or UUID of the server
        
        Deletes an existing server. Returns `None` on success.
        '''
        s = self.get(id)
        if isinstance(s, DashServer):
            del self.cache[s.uuid]
            s.delete()
            del s
            return
        
        res = self.client.request('GET', f'/delete?id={id}')
        if res['status'] != 'success':
            return res
        
        return None


class DashServerManager:
    def __init__(self, client: Dashactyl):
        self.client = client
        self.cache = {}
    
    def fetch(self, user: Union[int, Dashactyl], id: str):
        # will be implemented soon
        return NotImplemented
    
    def get(self, id: str) -> Optional[DashServer]:
        for k in self.cache.keys():
            if id in k:
                return self.cache[k]
        
        return None
    
    def get_manager_for(user: DashUser) -> DashUserServerManager:
        return user.servers


class CouponManager:
    def __init__(self, client: Dashactyl):
        '''`client` - The Dashactyl client
        
        Creates a new manager for client coupons.
        '''
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
        '''`code` - The name of the code
        
        `coins` - The number of coins the coupon should grant
        
        `ram` - The amoout of RAM the coupon should grant
        
        `disk` - The amount of disk the coupon should grant
        
        `cpu` - The amount of CPU the coupon should grant
        
        `servers` - The number of servers the coupon should grant
        
        Creates a new coupon with the specified parameters.
        '''
        if (0 < coins > MAX_AMOUNT or
            0 < ram > MAX_AMOUNT or
            0 < disk > MAX_AMOUNT or
            0 < cpu > MAX_AMOUNT or
            0 < servers > 10):
            raise ValueError('amount must be between 1 and 9 hundred-trillion (or servers which is 10)')
        
        if (not code and not (coins or ram or disk or cpu or servers)):
            raise ValueError('no valid parameters provided')
        
        data = self.client.request('POST',
                                    '/createcoupon',
                                    {'code': code, 'coins': coins, 'ram': ram, 'disk': disk, 'cpu': cpu, 'servers': servers})
        if 'status' in data:
            return data
        
        c = Coupon(data)
        self.cache[c.code] = c
        return c
    
    def revoke(self, code: str):
        '''`code` - The code of the coupon to revoke
        
        Revokes a specified coupon. Returns `None` on success.
        '''
        if self.get(code):
            del self.cache[code]
        
        # This should be DELETE...
        res = self.client.request('POST', '/revokecoupon', {'code': code})
        if res['status'] != 'success':
            return res
        
        return None


class DashUserManager:
    def __init__(self, client: Dashactyl):
        '''`client` - The Dashactyl client
        
        Creates a new manager for client users.
        '''
        self.client = client
        self.cache = {}
    
    def fetch(self, id: int) -> Optional[DashUser]:
        '''`id` - The ID of the user
        
        Fetches a user from the API directly.
        '''
        data = self.client.request('GET', f'/api/userinfo?id={str(id)}')
        if data['status'] != 'success':
            return data
        
        u = DashUser(self.client, data)
        self.cache[u.uuid] = u
        return u
    
    def get(self, id: Union[int, str]) -> Optional[DashUser]:
        '''`id` - The ID of the user
        
        Gets a user from the cache, or fetches directly if unavailable.
        '''
        for k in self.cache.keys():
            if id in k:
                return self.cache[k]
        
        if type(id) == str:
            raise DashUserWarning('user not found, try with ID instead')
        
        return self.fetch(id)
    
    def find(self, fn: FunctionType) -> Optional[DashUser]:
        for user in self.cache:
            if fn(user):
                return user
        
        return None
    
    def remove(self, user: Union[int, str, DashUser]):
        '''`id` - The ID of the user
        
        Removes (or deletes) the specified user's account. Returns `None` on success.
        '''
        if isinstance(user, DashUser):
            del self.cache[user.uuid]
            user.remove()
            return
        
        u = self.get(user)
        if u:
            del self.cache[u.uuid]
            u.remove()
            return
        
        raise DashUserWarning('user not found')
