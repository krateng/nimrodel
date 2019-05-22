from ._misc import docstring
from ._api import AbstractAPI


class API(AbstractAPI):
	def init(self,parsedoc=docstring):
		self.parsedoc = parsedoc
		self.functions = {} #tuple function, method


	# returns just the import information of this API
	def api_info(self):
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




	def handle(self,nodes,reqmethod,keys):

		func,httpmethod = self.functions[nodes[0]]
		if httpmethod == reqmethod:

			# convert to hinted types
			types = func.__annotations__
			for k in keys:
				if k in types:
					keys[k] = types[k](keys[k])

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
