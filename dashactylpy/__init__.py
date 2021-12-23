'''# Dashactyl.py
### An interactive API Wrapper for Dashactyl in Python

Author: Devonte <https://github.com/devnote-dev>
© 2021 devnote-dev
License: MIT
'''

__title__ = 'dashactylpy'
__author__ = 'Devonte'
__copyright__ = 'MIT'
__version__ = '0.0.5a'

from .api import Dashactyl
from .managers import CoinsManager, DashUserManager, ResourceManager, \
    CouponManager, DashUserServerManager
from .structures import DashUser, DashServer, Coupon
