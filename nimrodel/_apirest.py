from ._misc import docstring, MultiType
from ._api import AbstractAPI
import parse
from bottle import FormsDict


class API(AbstractAPI):
	def init(self,parsedoc=docstring):
		self.parsedoc = parsedoc

		self.classes = {}
		self.objects = {}
		self.methods = {} #not referring to object methods, but to http methods
		self.functions = {} #now these are the object methods .__.
		self.all_functions = [] #unbound


	# returns just the import information of this API
	def api_info(self):
		return {
			"url":self.pathprefix,
			"type":"restapi",
			"classes":[
				{
					"name":cls,
					"allowed":self.methods[self.classes[cls]],
					"instances":[name for name in self.objects[self.classes[cls]]],
					"methods":[],
					"attributes":{}
				} for cls in self.classes
			]
		}




	def handle(self,nodes,reqmethod,querykeys,headers):


		cls = self.classes[nodes.pop(0)]

		# REST access to resource
		if (reqmethod in ["POST"] and len(nodes) == 0) or (len(nodes) == 1):

			if reqmethod in ["POST"]:
				newobj = cls(**querykeys)
				# new object will sign up by itself thanks to class decorator
				return newobj.__apidict__()

			if reqmethod in ["GET","PATCH","DELETE"]:
				objkey = nodes.pop(0)
				obj = self.objects[cls][objkey]

			if reqmethod == "PATCH":
				try:
					return obj.__patch__(**querykeys)
				except:
					pass

				# if no __patch__ method is provided, we try everythin we can
				# to somehow patch this object
				for key in querykeys:
					for assignattempt in (
						# oh boy here we go again
						"getattr(obj,'set_' + key)(querykeys[key])",
						"getattr(obj,'set' + key)(querykeys[key])",
						"obj[key] = querykeys[key]",
						"setattr(obj,key,querykeys[key])"
					):
						try:
							exec(assignattempt)
							break
						except:
							pass

				return obj.__apidict__()

			if reqmethod == "GET":
				return obj.__apidict__()

			if reqmethod == "DELETE":
				del self.objects[cls][objkey]
				return {"status":"success"}

		# access to object methods
		elif len(nodes) > 1:
			objkey = nodes.pop(0)
			obj = self.objects[cls][objkey]

			for f in self.functions[cls]:

				if f["method"] != reqmethod: continue

				pathkeys = FormsDict()

				# match against paths
				r = parse.parse(f["path"],"/".join(nodes))
				if r is not None:
					func = f["func"]
					for k in r.named:
						# set vars according to path match
						pathkeys[k] = r[k]

					types = func.__annotations__
					for k in pathkeys:
						if k in types:
							if isinstance(types[k],MultiType):
								subtype = types[k].elementtype
								pk = pathkeys[k].split("/")
								pathkeys[k] = [subtype(e) for e in pk]
							else:
								pathkeys[k] = types[k](pathkeys[k])

					for k in querykeys:
						if k in types:
							if isinstance(types[k],MultiType):
								subtype = types[k].elementtype
								qk = querykeys.getall(k)
								querykeys[k] = [subtype(e) for e in qk]
							else:
								querykeys[k] = types[k](querykeys[k])

					if f["headers"]:
						return func(obj,**querykeys,**pathkeys,**headers)
					else:
						return func(obj,**querykeys,**pathkeys)


		return {"status":"failure"}


	# decorators for object methods
	def get(self,path,pass_headers=False):
		def decorator(func):
			# save reference to this function
			self.all_functions.append(
				{
					"path":path,
					"method":"GET",
					"func":func,
					"headers":pass_headers
				}
			)
			# return it unchanged
			return func
		return decorator

	def post(self,path,pass_headers=False):
		def decorator(func):
			# save reference to this function
			self.all_functions.append(
				{
					"path":path,
					"method":"POST",
					"func":func,
					"headers":pass_headers
				}
			)
			# return it unchanged
			return func
		return decorator


	# decorator for the class
	def apiclass(self,path,get=True,post=True,patch=True,delete=True):

		def decorator(cls):

			# save reference to this class
			self.classes[path] = cls
			self.objects[cls] = {}
			self.methods[cls] = {"GET":get,"POST":post,"PATCH":patch,"DELETE":delete}
			self.functions[cls] = []

			original_init = cls.__init__

			def new_init(self2,*args,**kwargs):
				# init normally
				original_init(self2,*args,**kwargs)
				# then sign up
				self.objects[cls][self2.__apiname__] = self2
				# self is the api object, self2 the object being initialized here

			cls.__init__ = new_init

			# unbound functions do not know their class ahead of time,
			# so we save them temporarily and then assign them on class
			# registration

			attrs = [cls.__dict__[k] for k in cls.__dict__]
			# include superclasses
			for superclass in cls.__bases__:
				attrs += [superclass.__dict__[k] for k in superclass.__dict__]
			# check if any decorated functions are methods of this class
			for f in self.all_functions:
				if f["func"] in attrs:
					self.functions[cls].append(f)
					#del self.all_functions[name]

			# return
			return cls

		return decorator
