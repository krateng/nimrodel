import time
from nimrodel import API

def blue(txt): return "\033[94m" + txt + "\033[0m"
def green(txt): return "\033[92m" + txt + "\033[0m"
def yellow(txt): return "\033[93m" + txt + "\033[0m"

# our api will be accessible under /coolapi
thebestapi = API(path="coolapi")

# we make instances of this class available under the path /coolapi/hero
@thebestapi.apiclass("hero")
class Hero:
	def __init__(self,name,friend,enemy,sibling=None):
		self.name = name
		self.friend = friend
		self.enemy = enemy
		self.sibling = sibling
		# we define how the object's url string is determined - it will be accessible under /coolapi/hero/thisname
		self.__apiname__ = name.lower().replace(" ","")

	# and finally the method calls - this will be accessible under /coolapi/hero/instancename/hello
	@thebestapi.get("hello")
	def hi(self):
		"""Says hello

		:return: Hello
		:rtype: string"""
		return self.name + " bids thee welcome!"

	# if the method takes any arguments, they can be passed with URI arguments or form data / json in the request body:
	@thebestapi.post("victory")
	def victory(self,weapon):
		"""Makes your hero win!

		:param string weapon: The weapon that should be used
		:return: An epic text
		:rtype: string"""
		return self.name + " defeats " + self.enemy + " with a " + weapon + "!"

	# of course this also works with arbitrary argument lists
	@thebestapi.post("party")
	def party(self,**kwargs):
		"""Starts an epic quest

		:param *string *role: All the members of the party
		:return: A party overview
		:rtype: string"""
		return self.name + " leads a party on a great quest. It consists of: "\
			+ ", ".join(kwargs[k] + " as the " + k.capitalize() for k in kwargs)

	# dictionaries are simply returned as json objects
	@thebestapi.get("info")
	def info(self):
		"""Shows some info

		:return: Some info
		:rtype: json"""
		return {"name":self.name,"friend":self.friend,"enemy":self.enemy}

	# if you give your class an __apidict__ method, this will be returned if calling the object without a method
	def __apidict__(self):
		return self.info()


	# if a function returns another API-enabled object, we can simply continue calling its methods
	@thebestapi.get("sibling")
	def get_sibling(self):
		"""Returns this hero's favorite sibling

		:return: The sibling
		:rtype: Hero"""
		return self.sibling




a = Hero("Finrod Felagund","Barahir","Werewolf")
b = Hero("Turin","Beleg","Glaurung")
c = Hero("Galadriel","Melian","Fëanor",sibling=a)

'''
Try out:

HTTP GET /api_explorer
HTTP GET /api_info
HTTP POST /coolapi/hero/turin/victory?weapon=sword
HTTP POST /coolapi/hero/turin/victory BODY weapon=sword
HTTP POST /coolapi/hero/turin/victory HEADER Content-Type: application/json BODY {"weapon":"sword"}
HTTP POST /coolapi/hero/finrodfelagund/party?ranger=Aegnor&archer=Angrod&healer=Galadriel
HTTP GET /coolapi/hero/galadriel
HTTP GET /coolapi/hero/galadriel/sibling/hello
'''

time.sleep(1)
print(yellow("Your first example API is now accessible! Visit ") + blue("http://[::1]:1337/api_explorer") + yellow(" or any other of the paths you can find in the example.py file!"))
input("Press any key to continue")

# now let's add a endpoint-based (non-object-oriented) API

from nimrodel import EAPI

# we use the existing server
simpleapi = EAPI(path="otherapi",server=thebestapi.server)

bestidols = ["Tzuyu","Rosé","Jennie","Seolhyun","Junghwa","Momo","Jimin","IU","Chungha"]


# now we make functions (not methods!) directly accessible

@simpleapi.get("bestidols")
# with type hints we make sure that query arguments are directly converted
def get_bestidols(maxnumber:int=None):
	"""Returns the best k-pop idols in order

	:param int maxnumber: Only return so many idols
	:return: Ordered list of idols
	"""
	return {
		"bestidols":bestidols[:maxnumber]
		# None works by not slicing the list at all, so it does the job of math.inf here
	}

'''
Try out:

HTTP GET /otherapi/bestidols?maxnumber=4
'''


# we can also put variables directly in the path

@simpleapi.get("idol/{rank}")
def get_idol(rank:int):
	"""Returns the idol of the given rank

	:param int rank: Rank
	:return: Name
	"""

	return bestidols[rank-1]


'''
Try out:

HTTP GET /otherapi/idol/2
'''


# if we want to accept a path segment of arbitrary length, simply type-hint it with Multi

from nimrodel import Multi

@simpleapi.get("idols/{ranks}")
def get_idols(ranks:Multi[int]):
	"""Returns the idol of the given ranks

	:param *int *ranks: Ranks
	:return: List of names
	"""

	return {"r":ranks}

	return [bestidols[r] for r in ranks]


'''
Try out:

HTTP GET /otherapi/idols/2/3/5
'''


# and of course lists of arguments also work for query string arguments

@simpleapi.get("ranks")
def get_ranks(idol:Multi[str]):
	"""Returns the ranks of all requested idols

	:param *string *idol: Names of the idols
	:return: JSON object
	"""

	return {i:bestidols.index(i) + 1 for i in idol}



'''
Try out:

HTTP GET /otherapi/ranks?idol=Tzuyu&idol=Junghwa
'''



print(yellow("A second API has been added at runtime to the same server. Refresh the API explorer to see it!"))
input("Press any key to continue")




from nimrodel import RAPI

# and now, a simplified version of the object-based API that allows creating,
# patching, deleting and fetching resources with the usual HTTP methods

api = RAPI(path="restapi",server=thebestapi.server)


@api.apiclass("faction")
class Faction:
	def __init__(self,leader,generals=[],admirals=[]):
		self.leader = leader
		self.__apiname__ = leader.lower().replace(" ","")
		self.generals = generals[:]
		self.admirals = admirals[:]

	# we don't need to define any methods with api access, just the apidict representation

	def __apidict__(self):
		return {
			"leader":self.leader,
			"generals":self.generals,
			"admirals":self.admirals
		}

	# but of course we CAN have additional methods

	@api.get("captains")
	def get_captains(self):
		return {
			"generals":self.generals,
			"admirals":self.admirals
		}


'''
Try out:

HTTP POST /restapi/faction HEADER Content-Type: application/json BODY {"leader":"Cao Cao","admirals":["Cai Mao","Zhang Yun"]}
HTTP POST /restapi/faction HEADER Content-Type: application/json BODY {"leader":"Liu Bei","generals":["Zhuge Liang"]}
HTTP PATCH /restapi/faction/liubei HEADER Content-Type: application/json BODY {"generals":["Guan Yu","Zhang Fei","Zhuge Liang"]}
HTTP DELETE /restapi/faction/caocao
'''


print(yellow("Now we also have a RESTful API. Refresh the API explorer again!"))
input("Press any key to terminate")
