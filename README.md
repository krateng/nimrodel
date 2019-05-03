# PyAPI

A simple Bottle.py-wrapper to provide API access to any python object.

# Requirements

* [python3](https://www.python.org/) - [GitHub](https://github.com/python/cpython)
* [bottle.py](https://bottlepy.org/) - [GitHub](https://github.com/bottlepy/bottle)
* [waitress](https://docs.pylonsproject.org/projects/waitress/) - [GitHub](https://github.com/Pylons/waitress)

# Quick Start

Create your API with

```python

from PyAPI import API

myapi = API()
```



Then make any class  accessible with a decorator.

```python

@myapi.apiclass("group")
class Group:

	def __init__(self,name,apipath,songs):
		# some stuff
		self.__apiname__ = apipath
```

Any instance of that class is now accessible via the combination of class path and its individual path. Now just decorate the methods. All its arguments can be passed via URI query arguments.

```python
	@myapi.get("songs")
	def get_songs(self,member):
		return {"songs":[s["title"] for s in self.songs if member in s["performers"]]}
```

Now create an object and make sure it has an `__apiname__` attribute:

```python
e = Group("Exid","exid",exidsongs)
```

Then you can access its methods with simple HTTP calls:


	HTTP GET http://localhost:1337/myapi/group/exid/songs?member=Junghwa
