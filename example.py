from PyAPI import *

thebestapi = API(path="coolapi")

class Hero:
	def __init__(self,name,friend,enemy):
		self.name = name
		self.friend = friend
		self.enemy = enemy

	@thebestapi.get("victory")
	def victory(self,weapon):
		return self.name + " defeats " + self.enemy + " with a " + weapon + "!"

	@thebestapi.get("party")
	def party(self,**kwargs):
		return self.name + " leads a party on a great quest. It consists of: "\
			+ ", ".join(kwargs[k] + " as the " + k.capitalize() for k in kwargs)

	@thebestapi.get("info")
	def info(self):
		return {"name":self.name,"friend":self.friend,"enemy":self.enemy}




a = Hero("Finrod Felagund","Barahir","Werewolf")
b = Hero("Turin","Beleg","Glaurung")
c = Hero("Galadriel","Melian","Fëanor")
thebestapi.register_object(a,"finrod")
thebestapi.register_object(b,"turambar")
thebestapi.register_object(c,"galadriel")

'''
Try out:

HTTP GET /coolapi/turambar/victory?weapon=sword
HTTP GET /coolapi/finrod/party?ranger=Aegnor&archer=Angrod&healer=Galadriel
HTTP GET /coolapi/galadriel/info
'''
