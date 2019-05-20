from nimrodel import API

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
HTTP GET /gui_api_explorer
HTTP POST /coolapi/hero/turin/victory?weapon=sword
HTTP POST /coolapi/hero/turin/victory BODY weapon=sword
HTTP POST /coolapi/hero/turin/victory HEADER Content-Type: application/json BODY {"weapon":"sword"}
HTTP POST /coolapi/hero/finrodfelagund/party?ranger=Aegnor&archer=Angrod&healer=Galadriel
HTTP GET /coolapi/hero/galadriel
HTTP GET /coolapi/hero/galadriel/sibling/hello
'''
