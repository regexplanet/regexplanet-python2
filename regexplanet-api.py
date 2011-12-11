#!/usr/bin/python
#
#
#

import cgi
import json
import re
import webapp2

class TestPage(webapp2.RequestHandler):
	def get(self):

		retVal = self.doTest()

		self.response.headers['Content-Type'] = 'text/plain'

		callback = self.request.get('callback')
		if len(callback) == 0 or re.match("[a-zA-Z][-a-zA-Z0-9_]*$", callback) is None:
			self.response.out.write(retVal)
		else:
			self.response.out.write(callback)
			self.response.out.write("(")
			self.response.out.write(retVal)
			self.response.out.write(");")



	def doTest(self):

		regex = self.request.get('regex')
		if len(regex) == 0:
			return json.dumps({"success": False, "message": "no regular expression to test"})

		replacement = self.request.get('replacement')
		inputs = self.request.get_all('input')

		options = set(self.request.get_all('option'))
		flags = 0
		flagList = []
		if "ignorecase" in options:
			flags |= re.IGNORECASE
			flagList.append("IGNORECASE")
		if "locale" in options:
			flags |= re.LOCALE
			flagList.append("LOCALE")
		if "multiline" in options:
			flags |= re.MULTILINE
			flagList.append("MULTILINE")
		if "dotall" in options:
			flags |= re.DOTALL
			flagList.append("DOTALL")
		if "unicode" in options:
			flags |= re.UNICODE
			flagList.append("UNICODE")
		if "verbose" in options:
			flags |= re.VERBOSE
			flagList.append("VERBOSE")


		html = []
		html.append('<table class="bordered-table zebra-striped">\n')
		html.append('\t<tbody>\n')

		html.append('\t\t<tr>\n')
		html.append('\t\t\t<td>')
		html.append('Regular Expression')
		html.append('</td>\n')
		html.append('\t\t\t<td>')
		html.append(cgi.escape(regex))
		html.append('</td>\n')
		html.append('\t\t</tr>\n')

		html.append('\t\t<tr>\n')
		html.append('\t\t\t<td>')
		html.append('as a raw Python string')
		html.append('</td>\n')
		html.append('\t\t\t<td>')
		html.append(cgi.escape("r'" + regex + "'"))
		html.append('</td>\n')
		html.append('\t\t</tr>\n')

		html.append('\t\t<tr>\n')
		html.append('\t\t\t<td>')
		html.append('as a regular Python string (with re.escape())')
		html.append('</td>\n')
		html.append('\t\t\t<td>')
		html.append(cgi.escape("'" + re.escape(regex)) + "'")
		html.append('</td>\n')
		html.append('\t\t</tr>\n')

		html.append('\t\t<tr>\n')
		html.append('\t\t\t<td>')
		html.append('replacement')
		html.append('</td>\n')
		html.append('\t\t\t<td>')
		html.append(cgi.escape(replacement))
		html.append('</td>\n')
		html.append('\t\t</tr>\n')

		pattern = re.compile(regex, flags)

		html.append('\t\t<tr>\n')
		html.append('\t\t\t<td>')
		html.append('flags')
		html.append('</td>\n')
		html.append('\t\t\t<td>')
		html.append(str(pattern.flags))
		html.append('</td>\n')
		html.append('\t\t</tr>\n')

		html.append('\t\t<tr>\n')
		html.append('\t\t\t<td>')
		html.append('flags (as constants)')
		html.append('</td>\n')
		html.append('\t\t\t<td>')
		html.append(cgi.escape("|".join(flagList)))
		html.append('</td>\n')
		html.append('\t\t</tr>\n')

		html.append('\t\t<tr>\n')
		html.append('\t\t\t<td>')
		html.append('# of groups (.group)')
		html.append('</td>\n')
		html.append('\t\t\t<td>')
		html.append(str(pattern.groups))
		html.append('</td>\n')
		html.append('\t\t</tr>\n')

		html.append('\t\t<tr>\n')
		html.append('\t\t\t<td>')
		html.append('Group name mapping (.groupindex)')
		html.append('</td>\n')
		html.append('\t\t\t<td>')
		html.append(str(pattern.groupindex))
		html.append('</td>\n')
		html.append('\t\t</tr>\n')

		html.append('\t</tbody>\n')
		html.append('</table>\n')

		html.append('<table class="bordered-table zebra-striped">\n')
		html.append('\t<thead>\n')
		html.append('\t\t<tr>\n')
		html.append('\t\t\t<th>Test</th>\n')
		html.append('\t\t\t<th>Target String</th>\n')
		html.append('\t\t\t<th>findall()</th>\n')
		html.append('\t\t\t<th>match()</th>\n')
		html.append('\t\t\t<th>search()</th>\n')
		html.append('\t\t\t<th>split()</th>\n')
		html.append('\t\t\t<th>sub()</th>\n')
		for loop in range(0, pattern.groups - 1):
			html.append('\t\t\t<th>group(')
			html.append(str(loop))
			html.append(')</th>\n');

		html.append('\t\t</tr>');
		html.append('\t</thead>');
		html.append('\t<tbody>');

		for loop in range(0, len(inputs)):

			test = inputs[loop]

			if len(test) == 0:
				continue

			html.append('\t\t<tr>\n')
			html.append('\t\t\t<td>')
			html.append(str(loop+1))
			html.append('</td>\n')

			html.append('\t\t\t<td>')
			html.append(cgi.escape(test))
			html.append('</td>\n')

			html.append('\t\t\t<td>')
			html.append(cgi.escape(str(pattern.findall(test))))
			html.append('</td>\n')

			html.append('\t\t\t<td>')
			html.append(cgi.escape(str(pattern.match(test))))
			html.append('</td>\n')

			html.append('\t\t\t<td>')
			html.append(cgi.escape(str(pattern.search(test))))
			html.append('</td>\n')

			html.append('\t\t\t<td>')
			html.append(cgi.escape(str(pattern.split(test))))
			html.append('</td>\n')

			html.append('\t\t\t<td>')
			html.append(cgi.escape(str(pattern.sub(replacement, test))))
			html.append('</td>\n')

			html.append('\t\t</tr>\n')

		html.append('\t</tbody>\n')
		html.append('</table>\n')

		return json.dumps({"success": True, "html": "".join(html)})



class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Hello, World!')

app = webapp2.WSGIApplication([('/', MainPage), ('/test.json', TestPage) ],
							  debug=True)


