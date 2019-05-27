from ._misc import docstring, MultiType
from ._api import AbstractAPI
import parse
from bottle import FormsDict


class API(AbstractAPI):
	def init(self,parsedoc=docstring):
		self.parsedoc = parsedoc

		self.classes = {}
		self.objects = {}


	# returns just the import information of this API
	def api_info(self):
		return {
			"url":self.pathprefix,
			"type":"restapi",
			"classes":[
				{
					"name":cls,
					"instances":[name for name in self.objects[self.classes[cls]]],
					"attributes":{

					}
				} for cls in self.classes
			]
		}




	def handle(self,nodes,reqmethod,querykeys,headers):


		cls = self.classes[nodes.pop(0)]

		if reqmethod in ["POST"]:
			newobj = cls(**querykeys)
			# new object will sign up by itself thanks to class decorator
			return newobj.__apidict__()

		if reqmethod in ["GET","PATCH","DELETE"]:
			objkey = nodes.pop(0)
			obj = self.objects[cls][objkey]

		if reqmethod == "PATCH":
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
			return "OK"


	# decorator for the class
	def apiclass(self,path):

		def decorator(cls):

			# save reference to this class
			self.classes[path] = cls
			self.objects[cls] = {}

			original_init = cls.__init__

			def new_init(self2,*args,**kwargs):
				# init normally
				original_init(self2,*args,**kwargs)
				# then sign up
				self.objects[cls][self2.__apiname__] = self2
				# self is the api object, self2 the object being initialized here

			cls.__init__ = new_init

			# return
			return cls

		return decorator
