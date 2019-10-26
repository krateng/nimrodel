def format(obj,**kwargs):

	if isinstance(obj,str) or isinstance(obj,int): return obj
	if obj == [] or obj == {}: return obj

	try:
		return {k:format(obj[k]) for k in obj}
	except Exception as e:
		pass

	try:
		return [format(element) for element in obj]
	except Exception as e:
		pass

	try:
		return format(obj.__apidict__())
	except Exception as e:
		pass

	return obj
