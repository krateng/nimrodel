from bottle import Bottle, FormsDict, request
from bottle import run as bottlerun
import waitress
from threading import Thread
from doreah.pyhp import parse
import pkg_resources



class AbstractAPI:

	def __init__(self,server=None,port=1337,IPv6=True,path="/api",**kwargs):

		self.path = path
		self.pathprefix = "" if path is None else ("/" + path)

		self.init(**kwargs)

		self.initserver(port=port,path=path,IPv6=IPv6,server=server)
		self.setup_explorer()
		self.setup_routing()

	def initserver(self,server,port,IPv6,path):

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

	def setup_explorer(self):
		# API explorer
		exploredec = self.server.get("/api_explorer")
		exploredec(self.explorer)

		g_exploredec = self.server.get("/gui_api_explorer")
		g_exploredec(self.gexplorer)

	def setup_routing(self):
		# unified access
		dec = self.server.get(self.pathprefix + "/<fullpath:path>")
		dec(self.route)
		dec = self.server.post(self.pathprefix + "/<fullpath:path>")
		dec(self.route)


	def explorer(self):
		return {"apis":[
				api.api_info() for api in self.server._apis
			]}

	def gexplorer(self):
		pyhpstr = pkg_resources.resource_string(__name__,"res/apiexplorer.pyhp")
		return parse(pyhpstr,self.explorer())



	def route(self,fullpath):
		# preprocess all requests
		headers = request.headers
		if request.get_header("Content-Type") is not None and "application/json" in request.get_header("Content-Type"):
			keys = request.json
		else:
			keys = FormsDict.decode(request.params)

		nodes = fullpath.split("/")
		reqmethod = request.method

		return self.handle(nodes,reqmethod,keys)
