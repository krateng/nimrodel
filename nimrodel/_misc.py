import re

def docstring(func):
	docstr = func.__doc__

	docstr = docstr.replace("\t","")

	params = {}
	returns = {}

	lines = docstr.split("\n")
	desc = []
	for l in lines:
		if l.startswith(":"):
			match = re.match(r":param (.*)? (.*)?: (.*)",l)
			if match is not None:
				type, name, d = match.groups()
				params[name] = {"type":type,"desc":d}
				continue
			match = re.match(r":return: (.*)",l)
			if match is not None:
				returns["desc"], = match.groups()
				continue
			match = re.match(r":rtype: (.*)",l)
			if match is not None:
				returns["type"], = match.groups()
				continue

		else:
			desc.append(l)

	desc
	desc = "\n".join(desc).strip("\n")

	return {"desc":desc,"params":params,"returns":returns}
