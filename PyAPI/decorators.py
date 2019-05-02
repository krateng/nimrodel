from bottle import Bottle, run, FormsDict, request
import waitress
from threading import Thread



class API:
	def __init__(self,port=1337,path="",IPv6=True):
		self.port = port
		self.path = path
		self.host = "::" if IPv6 else "0.0.0.0"

		self.objects = {}
		self.functions = {}

		self.server = Bottle()

		dec = self.server.get("/" + self.path + "/<objectname>/<functionname>")
		self.route_to_function = dec(self.route_to_function)


		t = Thread(target=self.startserver)
		t.start()

	def startserver(self):
		run(self.server,host=self.host,port=self.port, server="waitress")

	def route_to_function(self,objectname,functionname):
		keys = FormsDict.decode(request.query)
		obj = self.objects[objectname]
		func = self.functions[functionname]
		return func(obj,**keys)

	# decorator for the method
	def get(self,path):

		def decorator(func):
			# save reference to this function
			self.functions[path] = func
			# return in unchanged
			return func

		return decorator

	def register_object(self,obj,name):
		self.objects[name] = obj
