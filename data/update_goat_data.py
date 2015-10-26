import mechanize
from lxml import html
import time
def pull_post_history(from_page, to_page): # pull hts pages into local folder named as 0..pages/10
	browser = mechanize.Browser()
	browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13"),("Referer","https://hackthissite.org")]
	for number in range(int(from_page), int(to_page)):
		page = browser.open("https://www.hackthissite.org/forums/search.php?st=0&sk=t&sd=d&author=goatboy&start="+str(number*10))
		output_file = open(str(number),'w')
		output_file.write(page.read())
		print number
		time.sleep(15)

def loop_through_pages(pages): # add pages arg coz i can't be fucked figuring it out
	post_links = []
	for number in range(pages):
		page = open(str(number),'r')
		
		page = html.fromstring(page.read())# page definition changes to the xml object
		post_obj2 = page.xpath('//div[@class="search post bg2"]/div[@class="inner"]/div[@class="postbody"]/h3/a/@href')
		post_obj1 = page.xpath('//div[@class="search post bg1"]/div[@class="inner"]/div[@class="postbody"]/h3/a/@href')
		links = post_obj2 + post_obj1 # we need to add them together now
		post_links = post_links + links
	output_file = open('links','w')
	for l in post_links:
		output_file.write("https://www.hackthissite.org/forums"+l[1:]+"\n")
		


def data_mine():
	browser = mechanize.Browser()
	browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13"),("Referer","https://hackthissite.org")]
	links = open('links','r')
	done = open('done','r')
	links_followed = done.readlines()
	done.close()
	count = 0
	
	for link in links.readlines():
		if link in links_followed:
			pass
		else:
			link = link.rstrip()
			page = browser.open(link)
			page = html.fromstring(page.read())
			posts = page.xpath("//div[@class='postbody']")
			for post in posts:
				ptag = post.xpath('h3/a/@href')
				text = post.xpath("div[@class='content']/text()")
				if link[link.rfind('#p'):] == ptag[0]:
					done = open('done','a')
					data = open('data.txt','a')
					done.write(link+"\n")
					for line in text:
						try:
							data.write(line+"\n")
						except:
							print 'failed to write ' + line
					print text
			count = count + 1
			time.sleep(15)
		if count > 50:
			break
			
