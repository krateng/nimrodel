name = "nimrodel"
version = 0,7,0
desc = "Bottle-wrapper to make python objects accessible via HTTP API"
versionstr = ".".join(str(n) for n in version)
author = {
	"name": "Johannes Krattenmacher",
	"email": "python@krateng.dev",
	"github": "krateng"
}
requires = [
	"bottle",
	"waitress",
	"doreah>=1.2.1",
	"parse"
]
resources = [
	"res/*"
]



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
