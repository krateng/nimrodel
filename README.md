# PyAPI

A simple Bottle.py-wrapper to provide API access to any python object.

# Requirements

* [python3](https://www.python.org/) - [GitHub](https://github.com/python/cpython)
* [bottle.py](https://bottlepy.org/) - [GitHub](https://github.com/bottlepy/bottle)
* [waitress](https://docs.pylonsproject.org/projects/waitress/) - [GitHub](https://github.com/Pylons/waitress)

# Quick Start

Create your API with

`
	from PyAPI import API

	myapi = API()
`

Then make any method accessible a decorator. All arguments of the function can be passed via URI query arguments.

`
	class Group:

		@myapi.get("songs")
		def get_songs(self,member):
			return {"songs":[s["title"] for s in self.songs if member in s["performers"]]}
`

Finally, register your objects like this:

`
	e = Group("Exid")
	myapi.register_object(e,"exid")
`

Then you can access their functions with simple HTTP calls:

`
	HTTP GET http://localhost:1337/myapi/exid/songs?member=Junghwa
`
