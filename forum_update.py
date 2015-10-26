import mechanize
from lxml import html
import os.path
import re
import post as login
import gen_comment as g
class post():
        def __init__(self, date, link):
            self.link = link
            self.date = date
        def p(self):
            return str(self.date + " : " +self.link)

def crawl():
	comparing = False
	old_posts = []
	links = []
	dates = []
	new_posts = []
	if os.path.isfile('update'): # if file exists
		comparing = True
		old_file = open('update','r')   
		lines = old_file.readlines()
		line = 0
		while line < len(lines):
			old_posts.append(post(lines[line].rstrip(),lines[line+1].rstrip()))
			line = line + 2

	browser = mechanize.Browser()
	browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13"),("Referer","https://hackthissite.org")]

	page = browser.open('https://www.hackthissite.org/forums/search.php?search_id=active_topics')

	page = html.fromstring(page.read())
	posts = page.xpath("//li/dl[@class='icon']")
	popos =[]
	for post_index in range(len(posts)):
		if post_index == 0:
			continue
		href = posts[post_index].xpath("dd[@class='lastpost']/span/a/@href")[1]
		poster = posts[post_index].xpath("dd[@class='lastpost']/span/a/text()")[0]
		date = posts[post_index].xpath("dd[@class='lastpost']/span/text()")[3]
		print href + "\n" + poster + "\n" + date
		if poster != 'Goatbot':
			popo = post(date[3:], href[1: href.index("&sid")])
			popos.append(popo)
	if comparing:
		new_file = open('new','w')
		i = 0
		for n in popos:
			found = False
			for o in old_posts:
				if o.p() == n.p():
					found = True
					break;
			if found == False:
				print "new post!\n", n.p(),"\n"
				new_file.write(n.link);
				new_file.write("\n")

		new_file.close()

                
	update = open('update','w')
	for p in popos:
		update.write(p.date);
		update.write("\n");
		update.write(p.link);
		update.write("\n");
	update.close()

def goat_check():
	key_words = ['goat',
'bloat', 'blote', 'boat', 'coat', 'cote', 'dote', 'float', 'frote', 'gloat', 'groat', 'grote', 'moat', 'mote', 'note', 'oat', 'quote', 'roat', 'rote', 'scoat', 'shoat', 'shote', 'sloat', 'sloate', 'smote', 'sproat', 'stoat', 'stote', 'throat', 'tote', 'troat', 'vogt', 'vote', 'wrote','afloat', 'coat', 'promote', 'remote', 'boat'
,'quote', 'oat']

	off_limits = ['8','79','14','50','51','52','84','53','54','55','56','57','58','65',
'64','63','62','61','60','59','16','19','22','21','20','23','22','21','20','23',
'147','157']

	pages_file = open('new','r')
	array = pages_file.readlines()
	urls = []
	for i in array:
		urls.append("https://www.hackthissite.org/forums"+i.rstrip())
    
	for i in urls:
		if i[i.index('php?f')+6: i.index('&t=')] in off_limits:
			print i, ' is off limits'
			continue
		browser = mechanize.Browser()
		browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13"),("Referer","https://hackthissite.org")]
		print "trying '"+i + '"\n'
		page = browser.open(i)
		page = html.fromstring(page.read())

        # look for an instance of goat in the last post
		post_list = page.xpath('//div[@class="content"]/text()')
		if len(post_list) > 0:
			last_post = post_list[len(post_list)-1]
		else:
			continue		
		print "'"+last_post,"'\n"
		for test in key_words:
			if re.search(test, last_post, re.IGNORECASE):
				print 'found "', test + '"'
				# I'm attempting to lower the amount of stuff going on. I'll do a login while i'm on the thread and have the comment
				login.login(i.rstrip(), g.generate_comment(last_post))
				print "\nposted\n"
				#c = open('confirmed','a')
				#c.write(i.rstrip());
				#c.write("\n");
				#c.close()
				break
