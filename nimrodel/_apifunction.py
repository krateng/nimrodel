from bottle import Bottle, FormsDict, request
from bottle import run as bottlerun
import waitress
from threading import Thread
from doreah.pyhp import parse
import pkg_resources
from ._misc import docstring


class API:
	def __init__(self,port=1337,path=None,IPv6=True,server=None,parsedoc=docstring):

		self.path = path
		self.pathprefix = "" if path is None else ("/" + path)

		self.parsedoc = parsedoc

		self.functions = {} #tuple function, method


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
			#server._apis = getattr(server, "_apis", []).append(self)
			self.server = server


		# API explorer
		exploredec = self.server.get("/api_explorer")
		exploredec(self.explorer)

		g_exploredec = self.server.get("/gui_api_explorer")
		g_exploredec(self.gexplorer)

		# unified access
		dec = self.server.get(self.pathprefix + "/<fullpath:path>")
		dec(self.route)
		dec = self.server.post(self.pathprefix + "/<fullpath:path>")
		dec(self.route)



	def explorer(self):
		return {"apis":[
				api.explorer_this() for api in self.server._apis
			]}

	# returns just the import information of this API
	def explorer_this(self):
		return {
			"url":self.pathprefix,
			"type":"functionapi",
			"endpoints":[
				{
					"name":pth,
					"method":self.functions[pth][1],
					"description":self.parsedoc(self.functions[pth][0])["desc"],
					"parameters":self.parsedoc(self.functions[pth][0])["params"],
					"returns":self.parsedoc(self.functions[pth][0])["returns"]
				} for pth in self.functions
			]
		}

	def gexplorer(self):
		pyhpstr = pkg_resources.resource_string(__name__,"res/apiexplorer.pyhp")
		return parse(pyhpstr,self.explorer())


	def route(self,fullpath):
		headers = request.headers
		if request.get_header("Content-Type") is not None and "application/json" in request.get_header("Content-Type"):
			keys = request.json
		else:
			keys = FormsDict.decode(request.params)

		nodes = fullpath.split("/")
		reqmethod = request.method

		func,httpmethod = self.functions[nodes[0]]
		if httpmethod == reqmethod:
			return func(**keys)



	def get(self,path):

		def decorator(func):
			#assign the normal bottle decorator
			#dec = self.server.get(self.pathprefix + path)
			#dec(func)
			self.functions[path] = func,"GET"

			# return function unchanged
			return func

		return decorator

	def post(self,path):

		def decorator(func):
			#assign the normal bottle decorator
			#dec = self.server.post(self.pathprefix + path)
			#dec(func)
			self.functions[path] = func,"POST"

			# return function unchanged
			return func

		return decorator
