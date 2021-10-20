from bottle import Bottle, FormsDict, request, response, Response
from bottle import run as bottlerun
import waitress
from threading import Thread
from doreah.pyhp import file
from doreah.logging import log
import pkg_resources
from . import versionstr
from collections.abc import Mapping

__logmodulename__ = "nimrodel"

class AbstractAPI:

	def __init__(self,
			server=None,
			port=1337,IPv6=True,
			path="api",
			delay=False,
			auth=None,
			type="json",root_node=None,
			debug=False,
			**kwargs):

		self.path = path
		self.pathprefix = "" if path is None else ("/" + path)

		if auth is not None:
			self.auth = auth

		self.type = type.lower()
		self.rootnode = root_node

		self.debug = debug

		self.init(**kwargs)

		if delay:
			pass
		else:
			self.initserver(port=port,IPv6=IPv6,server=server)
			self.setup_explorer()
			self.setup_routing()

	def auth(self,request):
		return True

	def initserver(self,server,port,IPv6):

		if server is None:
			host = "::" if IPv6 else "0.0.0.0"
			port = port
			self.server = Bottle()
			self.server._apis = [self,]
			t = Thread(target=bottlerun,args=(self.server,),kwargs={"host":host,"port":port,"server":"waitress"})
			t.daemon = True
			t.start()
		else:
			try:
				server._apis.append(self)
			except:
				server._apis = [self]
			self.server = server

	# if delay has been specified on creation, we can now mount this api to a server
	def mount(self,server=None,port=1337,IPv6=True,path=None):

		self.initserver(port=port,IPv6=IPv6,server=server)
		if path is not None:
			self.path = path
			self.pathprefix = "/" + path
		self.setup_explorer()
		self.setup_routing()

	def setup_explorer(self):
		# API explorer
		exploredec = self.server.get("/api_info")
		exploredec(self.explorer)

		g_exploredec = self.server.get("/api_explorer")
		g_exploredec(self.gexplorer)

	def setup_routing(self):

		dec = self.server.get(self.pathprefix + "/<fullpath:path>")
		dec(self.route)
		dec = self.server.post(self.pathprefix + "/<fullpath:path>")
		dec(self.route)
		dec = self.server.route(self.pathprefix + "/<fullpath:path>",method="PATCH")
		dec(self.route)
		dec = self.server.put(self.pathprefix + "/<fullpath:path>")
		dec(self.route)
		dec = self.server.delete(self.pathprefix + "/<fullpath:path>")
		dec(self.route)

		dec = self.server.get(self.pathprefix + "/")
		dec(self.emptyroute)
		dec = self.server.post(self.pathprefix + "/")
		dec(self.emptyroute)
		dec = self.server.route(self.pathprefix + "/")
		dec(self.emptyroute)
		dec = self.server.put(self.pathprefix + "/")
		dec(self.emptyroute)
		dec = self.server.delete(self.pathprefix + "/")
		dec(self.emptyroute)

	def emptyroute(self):
		return self.route("")

	def explorer(self):
		return {
			"information":{
				"nimrodel-version":versionstr
			},
			"apis":[
				api.api_info() for api in self.server._apis
			]
		}

	def gexplorer(self):
		folder = pkg_resources.resource_filename(__name__,"res/")
		#pyhpstr = pkg_resources.resource_string(__name__,"res/apiexplorer.pyhp")
		return file(folder + "/apiexplorer.pyhp",self.explorer())



	def route(self,fullpath):
		# preprocess all requests
		headers = request.headers

		keys = FormsDict.decode(request.query)

		if self.debug:
			log("Request to " + fullpath)
			for k in keys:
				log("\t" + k + " = " + keys.get(k))

		if request.get_header("Content-Type") is not None and "application/json" in request.get_header("Content-Type"):
			json = request.json if request.json is not None else {}
			keys.update(json)

		else:
			formdict = FormsDict.decode(request.forms)
			for k in formdict:
				for v in formdict.getall(k):
					keys[k] = v
			#keys.update(FormsDict.decode(request.forms))

		#print(keys)

		nodes = fullpath.split("/")
		reqmethod = request.method

		if self.auth(request):
			result = self.handle(nodes,reqmethod,keys,headers)
			if isinstance(result,Response):
				return result
			else:
				result = serialize(result)
				result = format_output[self.type](result,root_node=self.rootnode)
				return result
		else:
			response.status = 403
			return "Access denied"


from .output import json, xml

format_output = {
	"json":json.format,
	"xml":xml.format
}


def serialize(obj):

	if isinstance(obj,str) or isinstance(obj,int): return obj
	if obj == [] or obj == {}: return obj

	if isinstance(obj,Mapping):
		try:
			return {k:serialize(obj[k]) for k in obj}
		except Exception as e:
			pass

	try:
		return [serialize(element) for element in obj]
	except Exception as e:
		pass

	for f in ["__apidict__","__json__","__dict__"]:
		try:
			return serialize(getattr(obj,f)())
		except Exception as e:
			pass

	return obj
