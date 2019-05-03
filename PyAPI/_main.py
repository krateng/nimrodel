from bottle import Bottle, run, FormsDict, request
import waitress
from threading import Thread



class API:
	def __init__(self,port=1337,path=None,IPv6=True):
		self.port = port
		self.path = path
		self.pathprefix = "" if self.path is None else ("/" + self.path)
		self.host = "::" if IPv6 else "0.0.0.0"

		self.classes = {}
		self.objects = {}
		self.functions = {}

		self.server = Bottle()

		dec = self.server.get(self.pathprefix + "/<classname>/<objectname>/<functionname>")
		self.route_to_function = dec(self.route_to_function)


		t = Thread(target=self.startserver)
		t.start()

	def startserver(self):
		run(self.server,host=self.host,port=self.port, server="waitress")

	def route_to_function(self,classname,objectname,functionname):
		keys = FormsDict.decode(request.query)
		cls = self.classes[classname]
		obj = self.objects[cls][objectname]
		func = self.functions[functionname]
		return func(obj,**keys)

	# decorator for the method
	def get(self,path):

		def decorator(func):
			# save reference to this function
			self.functions[path] = func
			# return it unchanged
			return func

		return decorator

	# decorator for the class
	def apiclass(self,path):

		def decorator(cls):

			# save reference to this class
			self.classes[path] = cls
			self.objects[cls] = {}

			original_init = cls.__init__

			def new_init(self2,*args,**kwargs):
				print("Signing up")
				# init normally
				original_init(self2,*args,**kwargs)
				# then sign up
				self.objects[cls][self2.__apiname__] = self2
				# self is the api object, self2 the object being initialized here

			cls.__init__ = new_init



			# return
			return cls

		return decorator

	# manually register an object
	def register_object(self,obj,name):
		self.objects[name] = obj
