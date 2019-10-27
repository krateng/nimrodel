# Credit to https://gist.github.com/reimund/5435343/


def format(d, root_node="root"):
	return '<?xml version="1.0" encoding="UTF-8"?>' + formatelement(d,root_node)

def formatelement(d, root_node="root"):
	wrap          =     False if None == root_node or isinstance(d, list) else True
	root          = 'objects' if None == root_node else root_node
	root_singular = root[:-1] if 's' == root[-1] and None == root_node else root
	xml           = ''
	children      = []

	if isinstance(d, dict):
		for key, value in dict.items(d):
			if isinstance(value, dict):
				children.append(formatelement(value, key))
			elif isinstance(value, list):
				children.append(formatelement(value, key))
			else:
				xml = xml + ' ' + key + '="' + str(value) + '"'
	else:
		for value in d:
			children.append(formatelement(value, root_singular))

	end_tag = '>' if 0 < len(children) else '/>'

	if wrap or isinstance(d, dict):
		xml = '<' + root + xml + end_tag

	if 0 < len(children):
		for child in children:
			xml = xml + child

		if wrap or isinstance(d, dict):
			xml = xml + '</' + root + '>'

	return xml
