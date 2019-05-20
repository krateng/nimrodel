import re

regex_param = re.compile(r":param (.*)? (.*)?: (.*)")
regex_return = re.compile(r":return: (.*)")
regex_rtype = re.compile(r":rtype: (.*)")

# default function to extract information from functions
def docstring(func):
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
