def format(obj,**kwargs):


	if isinstance(obj,str) or isinstance(obj,int): return obj
	if obj == [] or obj == {}: return obj

	try:
		return {k:jsonify(obj[k]) for k in obj}
	except Exception as e:
		pass

	try:
		return [jsonify(element) for element in obj]
	except Exception as e:
		pass

	try:
		return jsonify(obj.__apidict__())
	except Exception as e:
		pass

	return obj
