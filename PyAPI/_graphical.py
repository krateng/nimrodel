from doreah.pyhp import parse
import pkg_resources

def page(apidict):

	pyhpstr = pkg_resources.resource_string(__name__,"res/apiexplorer.pyhp")
	return parse(pyhpstr,apidict)
