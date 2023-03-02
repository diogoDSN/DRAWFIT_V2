from typing import Optional
from enum import Enum

class Permissions(Enum):

    OWNER = 'Owner'
    MODERATOR = 'Moderator'
    NORMAL = 'Normal'

def nextPermission(perm: Optional[Permissions]) -> Optional[Permissions]:
    if perm == None:
        return Permissions.NORMAL
    elif perm == Permissions.NORMAL:
        return Permissions.MODERATOR
    elif perm == Permissions.MODERATOR:
        return Permissions.OWNER
    elif perm == Permissions.OWNER:
        return Permissions().OWNER

def previousPermission(perm: Optional[Permissions]) -> Optional[Permissions]:
    if perm == Permissions.OWNER:
        return Permissions.MODERATOR
    elif perm == Permissions.MODERATOR:
        return Permissions.NORMAL
    else:
        None
    