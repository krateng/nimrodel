# Nimrodel

A simple Bottle.py-wrapper to provide HTTP API access to any python object.

# Requirements

* [python3](https://www.python.org/) - [GitHub](https://github.com/python/cpython)
* [bottle.py](https://bottlepy.org/) - [GitHub](https://github.com/bottlepy/bottle)
* [waitress](https://docs.pylonsproject.org/projects/waitress/) - [GitHub](https://github.com/Pylons/waitress)
* [doreah](https://pypi.org/project/doreah/) - [GitHub](https://github.com/krateng/doreah) (at least Version 0.9.1)
* [parse](https://pypi.org/project/parse/) - [GitHub](https://github.com/r1chardj0n3s/parse)

# Quick Start

Install with

```
pip install nimrodel
```

Create your API with

```python

from nimrodel import API

myapi = API()
```

You may optionally pass a port number with `port=42`, a path with `path="api"` and whether you want to serve on IPv4 (`IPv6=False`).
You can also give the API object an existing bottle server (`server=bottleobject`), in which case your API will be served on the existing server. It is heavily recommended to also pass a path variable to separate API from regular routing of your server.
You may also pass a custom function with `parsedoc=yourfunction` that takes your method as input and returns a dictionary with the values `desc` for the function description, `params` for a dictionary of parameter names mapped to a dictionary and `returns` for a dictionary of the return value. Both return and param dictionaries can have the keys `type` and `desc` for data type and description respectively. By default nimrodel will attempt to parse your docstring according to the reST standard (Sphinx).


Then make any class accessible with a decorator.

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

Then you can access its methods with simple HTTP calls like `/group/exid/songs?member=Junghwa`.

There is also an integrated graphical API explorer under `/api_explorer`.

Nimrodel also allows you to create a simple function-based API with the class `EAPI`.


For more in-depth exploration of the possibilities, refer to the file `example.py` included in the repository.
