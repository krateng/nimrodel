def page(apidict):

	html = """

	<html>
		<head>
			{head}
		</head>
		<body>
			{body}
		</body>
	</html>

	""".format(head=head(),body=body(apidict))

	return html

def head():
	return """

	<title>API Explorer</title>
	<style>{style}</style>
	<script>{script}</script>

	""".format(style=style(),script=script())

def body(apidict):

	html = ""

	i = 0
	for api in apidict["apis"]:
		html += """

			<div onclick=triggerCollapse(this) class="api_header" id="api_header_{id}">
				{apiurl}
			</div>
			<div class="api_desc" id="api_desc_{id}">
				"""

		for cls in api["classes"]:
			classhtml = ""
			classhtml += """
				<div onclick=triggerCollapse(this) class="class_header" id="class_header_{clsid}">
					{classname}
				</div>
				<div class="class_desc" id="class_desc_{clsid}">
					"""

			for method in cls["methods"]:
				methodhtml = ""
				methodhtml += """
					<div onclick=triggerCollapse(this) class="method_header" id="method_header_{methid}">
						<span class="method_{httpmethod}">{httpmethod}</span>
						{methodname}
					</div>
					<div class="method_desc" id="method_desc_{methid}">
						Awesome method
					</div>


				"""

				methodhtml = methodhtml.format(methodname=method["name"],httpmethod=method["method"],methid=str(i))
				classhtml += methodhtml
				i += 1


			classhtml += """
				</div>


			"""

			classhtml = classhtml.format(classname=cls["name"],clsid=str(i))
			html += classhtml
			i += 1

		html += """

			</div>


		"""

		html = html.format(apiurl=api["url"],id=str(i))
		i += 1

	return html

def style():
	return """

	.api_header {{
		padding:10px;
		font-weight:bold;
		cursor:pointer;
	}}
	.api_desc {{

	}}

	.class_header {{
		padding:10px;
		background-color:grey;
		cursor:pointer;
	}}
	.method_GET {{
		padding:5px;
		background-color:blue;
	}}
	.method_POST {{
		padding:5px;
		background-color:green;
	}}
	.class_desc {{

	}}


	""".format()

def script():
	return """

	function triggerCollapse(e) {
		id = e.id;
		otherid = id.replace("_header_","_desc_")
		descbody = document.getElementById(otherid)
		if (descbody.style.display == "none") { descbody.style.display = ""; }
		else { descbody.style.display = "none"; }
	}


	"""
