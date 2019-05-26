from ._misc import docstring
from ._api import AbstractAPI



class API(AbstractAPI):
	def init(self,parsedoc=docstring):

		self.parsedoc = parsedoc

		self.classes = {}
		self.objects = {}
		self.functions = {} #tuple function, method

		self.all_functions = []


	def api_info(self):
		return {
			"url":self.pathprefix,
			"type":"objectapi",
			"classes":[
				{
					"name":cls,
					"instances":[name for name in self.objects[self.classes[cls]]],
					"methods":[
						{
							"name":name,
							"method":self.functions[self.classes[cls]][name][1],
							"description":self.parsedoc(self.functions[self.classes[cls]][name][0])["desc"],
							"parameters":self.parsedoc(self.functions[self.classes[cls]][name][0])["params"],
							"returns":self.parsedoc(self.functions[self.classes[cls]][name][0])["returns"]
						} for name in self.functions[self.classes[cls]]
					]
				} for cls in self.classes
			]
		}

		# access methods
	#	dec = self.server.get(self.pathprefix + "/<classname>/<objectname>/<functionname>")
	#	self.route_to_function = dec(self.route_to_function)

		# access object itself
	#	dec = self.server.get(self.pathprefix + "/<classname>/<objectname>")
	#	self.route_to_object = dec(self.route_to_object)



	def handle(self,nodes,reqmethod,keys,headers):

		post_allowed = (reqmethod == "POST")

		cls = self.classes[nodes.pop(0)]
		obj = self.objects[cls][nodes.pop(0)]

		current = obj


		while len(nodes) > 0:
			next = nodes.pop(0)
			func,httpmethod = self.functions[current.__class__][next]
			if httpmethod == "GET":
				current = func(current,**keys)
			elif httpmethod == "POST" and post_allowed:
				current = func(current,**keys)
				post_allowed = False
			else:
				return {"error":"HTTP method"}

		if post_allowed:
			# if we made a post request and never used any post step
			return {"error":"HTTP method"}

		# all is done, return last object
		if callable(getattr(current,"__apidict__",None)):
			return current.__apidict__()
		else:
			return current



#	def route_to_function(self,classname,objectname,functionname):
#		keys = FormsDict.decode(request.query)
#		cls = self.classes[classname]
#		obj = self.objects[cls][objectname]
#		func = self.functions[cls][functionname]
#		return func(obj,**keys)
#
#	def route_to_object(self,classname,objectname):
#		keys = FormsDict.decode(request.query)
#		cls = self.classes[classname]
#		obj = self.objects[cls][objectname]
#		return obj.__apidict__(**keys)

	# decorator for the method
	def get(self,path):

		def decorator(func):
			# save reference to this function
			self.all_functions.append((path,func,"GET"))
			# return it unchanged
			return func

		return decorator

	def post(self,path):

		def decorator(func):
			# save reference to this function
			self.all_functions.append((path,func,"POST"))
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
			#self.functions[cls] = self.all_functions
			#self.all_functions = {}

			# unbound functions do not know their class ahead of time,
			# so we save them temporarily and then assign them on class
			# registration

			attrs = [cls.__dict__[k] for k in cls.__dict__]
			# include superclasses
			for superclass in cls.__bases__:
				attrs += [superclass.__dict__[k] for k in superclass.__dict__]
			# check if any decorated functions are methods of this class
			for (pth,func,method) in self.all_functions:
				if func in attrs:
					self.functions[cls][pth] = func,method
					#del self.all_functions[name]



			# return
			return cls

		return decorator

	# manually register an object
##	def register_object(self,obj,name):
#		self.objects[name] = obj
