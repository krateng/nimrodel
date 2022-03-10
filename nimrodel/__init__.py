__version__ = '0.8.0'

from ._apiobject import API as ObjectAPI
from ._apifunction import API as EndpointAPI
from ._apirest import API as RestAPI
from ._misc import Multi

# short names
OAPI = ObjectAPI
EAPI = EndpointAPI
RAPI = RestAPI

# default
API = OAPI
