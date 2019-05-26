from ._misc import docstring, MultiType
from ._api import AbstractAPI
import parse
from bottle import FormsDict


class API(AbstractAPI):
	def init(self,parsedoc=docstring):
		self.parsedoc = parsedoc

		#self.functions = FunctionHolder()
		self.functions = []
		# dict: route, method, func

	# returns just the import information of this API
	def api_info(self):
		return {
			"url":self.pathprefix,
			"type":"functionapi",
			"endpoints":[
				{
					"name":f["path"],
					"method":f["method"],
					"description":self.parsedoc(f["func"])["desc"],
					"parameters":self.parsedoc(f["func"])["params"],
					#"parameters":{
					#	param:{
					#		"type":str(self.functions[pth][0].__annotations__.get(param)),
					#		"desc":"tbd"
					#	}
					#for param in self.functions[pth][0].__code__.co_varnames},
					"returns":self.parsedoc(f["func"])["returns"]
				} for f in self.functions
			]
		}




	def handle(self,nodes,reqmethod,querykeys,headers):


		for f in self.functions:

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
					return func(**querykeys,**pathkeys,**headers)
				else:
					return func(**querykeys,**pathkeys)

		return {"error":"Not found"}


	def get(self,path,pass_headers=False):

		def decorator(func):
			self.functions.append(
				{
					"path":path,
					"method":"GET",
					"func":func,
					"headers":pass_headers
				}
			)

			# return function unchanged
			return func
		return decorator

	def post(self,path,pass_headers=False):

		def decorator(func):
			self.functions.append(
				{
					"path":path,
					"method":"POST",
					"func":func,
					"headers":pass_headers
				}
			)

			# return function unchanged
			return func
		return decorator
