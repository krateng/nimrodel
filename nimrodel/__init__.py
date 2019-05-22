from ._apiobject import API as ObjectAPI
from ._apifunction import API as EndpointAPI

# short names
OAPI = ObjectAPI
EAPI = EndpointAPI

# default
API = OAPI

name = "nimrodel"
version = 0,4,0
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
