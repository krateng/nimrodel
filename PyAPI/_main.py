from bottle import Bottle, FormsDict, request
from bottle import run as bottlerun
import waitress
from threading import Thread



class API:
	def __init__(self,port=1337,path=None,IPv6=True,server=None):

		self.path = path
		self.pathprefix = "" if path is None else ("/" + path)

		self.classes = {}
		self.objects = {}
		self.functions = {}

		self.unassigned_functions = {}

		if server is None:
			host = "::" if IPv6 else "0.0.0.0"
			port = port
			self.server = Bottle()
			self.server._apis = [self,]
			t = Thread(target=bottlerun,args=(self.server,),kwargs={"host":host,"port":port,"server":"waitress"})
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

		# unified access
		dec = self.server.get(self.pathprefix + "/<fullpath:path>")
		self.route = dec(self.route)

	def explorer(self):
		return {"apis":[
				{
					"url":api.pathprefix,
					"classes":[
						{
							"name":cls,
							"instances":[obj for obj in api.objects[api.classes[cls]]],
							"methods":[obj for obj in api.functions[api.classes[cls]]]
						} for cls in api.classes
					]
				} for api in self.server._apis
			]}

		# access methods
	#	dec = self.server.get(self.pathprefix + "/<classname>/<objectname>/<functionname>")
	#	self.route_to_function = dec(self.route_to_function)

		# access object itself
	#	dec = self.server.get(self.pathprefix + "/<classname>/<objectname>")
	#	self.route_to_object = dec(self.route_to_object)



	def route(self,fullpath):
		keys = FormsDict.decode(request.query)
		nodes = fullpath.split("/")

		cls = self.classes[nodes.pop(0)]
		obj = self.objects[cls][nodes.pop(0)]

		current = obj

		while len(nodes) > 0:
			next = nodes.pop(0)
			func = self.functions[current.__class__][next]
			current = func(current,**keys)

		# all is done, return last object
		if callable(getattr(current,"__apidict__",None)):
			return current.__apidict__()
		else:
			return current



	def route_to_function(self,classname,objectname,functionname):
		keys = FormsDict.decode(request.query)
		cls = self.classes[classname]
		obj = self.objects[cls][objectname]
		func = self.functions[cls][functionname]
		return func(obj,**keys)

	def route_to_object(self,classname,objectname):
		keys = FormsDict.decode(request.query)
		cls = self.classes[classname]
		obj = self.objects[cls][objectname]
		return obj.__apidict__(**keys)

	# decorator for the method
	def get(self,path):

		def decorator(func):
			# save reference to this function
			self.unassigned_functions[path] = func
			# return it unchanged
			return func

		return decorator

	# decorator for the class
	def apiclass(self,path):

		def decorator(cls):

			# save reference to this class
			self.classes[path] = cls
			self.objects[cls] = {}
			self.functions[cls] = {}

			original_init = cls.__init__

			def new_init(self2,*args,**kwargs):
				# init normally
				original_init(self2,*args,**kwargs)
				# then sign up
				self.objects[cls][self2.__apiname__] = self2
				# self is the api object, self2 the object being initialized here

			cls.__init__ = new_init

			# assign functions
			#self.functions[cls] = self.unassigned_functions
			#self.unassigned_functions = {}

			# unbound functions do not know their class ahead of time,
			# so we save them temporarily and then assign them on class
			# registration

			attrs = [cls.__dict__[k] for k in cls.__dict__]
			# check if any decorated functions are methods of this class
			for name in list(self.unassigned_functions.keys()):
				if self.unassigned_functions[name] in attrs:
					self.functions[cls][name] = self.unassigned_functions[name]
					del self.unassigned_functions[name]



			# return
			return cls

		return decorator

	# manually register an object
	def register_object(self,obj,name):
		self.objects[name] = obj
