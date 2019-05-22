import re

regex_param = re.compile(r":param (.*)? (.*)?: (.*)")
regex_return = re.compile(r":return: (.*)")
regex_rtype = re.compile(r":rtype: (.*)")

# default function to extract information from functions
def docstring(func):
	try:
		docstr = func.__doc__
		docstr = docstr.replace("\t","")

		params = {}
		returns = {}

		lines = docstr.split("\n")
		desc = []
		for l in lines:
			if l.startswith(":"):
				match = regex_param.match(l)
				if match is not None:
					type, name, d = match.groups()
					params[name] = {"type":type,"desc":d}
					continue
				match = regex_return.match(l)
				if match is not None:
					returns["desc"], = match.groups()
					continue
				match = regex_rtype.match(l)
				if match is not None:
					returns["type"], = match.groups()
					continue

			else:
				desc.append(l)

		desc
		desc = "\n".join(desc).strip("\n")

		return {"desc":desc,"params":params,"returns":returns}
	except:
		return {"desc":"","params":{},"returns":{}}





# class for routing

import enum

class Http(enum.Enum):
	GET = 1
	POST = 2

	def __str__(self):
		return self.name

class FunctionHolder:

	def __init__(self):
		self.functions = {}
		# this dict:
		# 	name				-> subdict				fixed paths
		#	None				-> (varname, subdict)	for variable
		#	GET					-> func					get function at this path
		#	POST				-> func					post function at this path

		self.functionlist = []

	def add(self,func,method,path):
		route = path.split("/")
		method = {"get":Http.GET,"post":Http.POST}[method.lower()]
		pointer = self.functions
		for node in route:
			if node.startswith("<") and node.endswith(">"):
				pointer[None] = pointer.setdefault(None,(node[1:-1],{}))
				pointer = pointer[None][1]
			else:
				pointer[node] = pointer.setdefault(node,{})
				pointer = pointer[node]
		pointer[method] = func
		self.functionlist.append(
			{
				"function":func,
				"method":method,
				"route":["{" + node[1:-1] + "}" if node.startswith("<") and node.endswith(">") else node for node in route],
			}
		)

	def call(self,method,route,keys):
		method = {"get":Http.GET,"post":Http.POST}[method.lower()]
		pointer = self.functions
		for node in route:
			# explicit name
			if node in pointer:
				pointer = pointer[node]
			else:
				keys[pointer[None][0]] = node # set argument to uri part
				pointer = pointer[None][1]

		func = pointer[method]

		# convert to hinted types
		types = func.__annotations__
		for k in keys:
			if k in types:
				keys[k] = types[k](keys[k])

		return func(**keys)


	# enable iteration over all functions
	def __getitem__(self,pos):
		return self.functionlist[pos]
	def __len__(self):
		return len(self.functionlist)
