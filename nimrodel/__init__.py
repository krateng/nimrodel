name = "nimrodel"
version = 0,4,1
versionstr = ".".join(str(n) for n in version)
author = {
	"name": "Johannes Krattenmacher",
	"email": "python@krateng.dev",
	"github": "krateng"
}
requires = [
	"bottle",
	"waitress",
	"doreah"
]


from ._apiobject import API as ObjectAPI
from ._apifunction import API as EndpointAPI

# short names
OAPI = ObjectAPI
EAPI = EndpointAPI

# default
API = OAPI
