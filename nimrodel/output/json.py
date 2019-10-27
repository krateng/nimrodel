def format(obj,**kwargs):

	# dicts are already jsonified by bottle, just make sure we don't have a top level list

	if isinstance(obj,list):
		return {"result":obj}
	else:
		return obj
