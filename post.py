import mechanize
import markov
import os

def login(link, comment):
	browser = mechanize.Browser()
	browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13"),("Referer","https://hackthissite.org")]
	browser.open("https://hackthissite.org") 
	browser.select_form(nr = 0)
	browser.form['username'] = 'Goatbot'
	browser.form['password'] = 'nooap'
	#print 'logging onto HTS'
	logged_in_object = browser.submit()
	#print 'logged on\n redirecting to forums'
	forum_ready = browser.open("https://www.hackthissite.org/forums/ucp.php?mode=login")
	#print 'ok'
	formed_uri = str(link.replace("viewtopic","posting").rstrip()+"&mode=reply")
	print "'",formed_uri,"'"
	browser.open(formed_uri)
	for form in browser.forms():
		if form.attrs['id'] == 'postform':
			browser.form = form
			break
	browser.form['message'] = "did someone say goat?\n" + comment
	a = browser.submit(name='post', label='Submit')

