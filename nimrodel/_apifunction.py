from ._misc import docstring, FunctionHolder
from ._api import AbstractAPI


class API(AbstractAPI):
	def init(self,parsedoc=docstring):
		self.parsedoc = parsedoc

		# nested dicts that lead to the right function
		# None points to the function at that position if no further path is given
		# 0 points to functions that accept a variable at this point, its dict includes the 1 key for the var name
		self.functions = FunctionHolder()

	# returns just the import information of this API
	def api_info(self):
		return {
			"url":self.pathprefix,
			"type":"functionapi",
			"endpoints":[
				{
					"name":"/".join(func["route"]),
					"method":func["method"].name,
					"description":self.parsedoc(func["function"])["desc"],
					"parameters":self.parsedoc(func["function"])["params"],
					#"parameters":{
					#	param:{
					#		"type":str(self.functions[pth][0].__annotations__.get(param)),
					#		"desc":"tbd"
					#	}
					#for param in self.functions[pth][0].__code__.co_varnames},
					"returns":self.parsedoc(func["function"])["returns"]
				} for func in self.functions
			]
		}




	def handle(self,nodes,reqmethod,keys):

		return self.functions.call(reqmethod,nodes,keys)



	def get(self,path):

		def decorator(func):
			self.functions.add(func,"GET",path)
			#self.functions[path] = func,"GET"

			# return function unchanged
			return func

		return decorator

	def post(self,path):

		def decorator(func):
			self.functions.add(func,"POST",path)

			# return function unchanged
			return func

		return decorator
