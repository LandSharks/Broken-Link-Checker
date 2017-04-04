from lxml import html
import requests
from requests_ntlm import HttpNtlmAuth
import getpass

domain = ""
password = ""
user = ""
checked = list()

def getUrl(url):
	if(url in checked or "mailto:" in url or "#" in url):
		#print("Url already checked")
		checked.append(url)
		return list()
	elif("/" == url[0] or "." not in url or ".." in url):
		checked.append(url)
		url = "http://{}{}".format(domain, url)
	elif("javascript" in url or ";" in url or ".js" in url):
		checked.append(url)
		return list()
	page = requests.get(url, auth=HttpNtlmAuth(user, password), timeout=30)
	if(not page.status_code == 200):
		print("Broken link found!")
		f = open('BrokenLinksBFS.txt', 'a')
		f.write("Link: {} returned error code: {}.\n\n".format(url, page.status_code))
		f.close();
		checked.append(url)
		return list();
	elif(domain not in url):
		#print("Url not in domain")
		checked.append(url)
		return list()
	tree = html.fromstring(page.content)
	hyper = tree.xpath("//a/@href")
	hyper[:] = [x for x in hyper if("javascript" not in x and "#" not in x or "_layouts" not in x)]
	checked.append(url)
	return hyper;

def check(data):
	if(not data):
		return
	else:
		stack = list()
		for i in data:
			try:
				if("javascript" not in i and "#" not in i and "_layouts" not in i):
					print("Fetching: {}".format(i))
					temp = getUrl(i)
					stack.append(temp)
			except Exception as e:
				f = open('ConnectionFailuresBFS.txt', 'a')
				f.write("URL: {} caused the script to crash\n\tException {}\n\n".format(i,e))
				f.close();
				checked.append(i)
				print("A failure occured while making a GET request")
		for i in stack:
			check(stack.pop())


org = [".net", ".gov", ".com", ".org", ".edu"]
url = input("Starting page (w/o the http://): ")

index = None

try:
	for i in org:
		if(i in url):
			index = url.index(i)
except Exception:
	index = None

if(index is not None):
	domain = url[0:index+4]
else: 
	print("Could not determine domain")
	domain = input("Please manually input the domain (include .com, .net, etc): ")
user = input("Domain\\User Name: ")
password = getpass.getpass("Password: ")
check(getUrl("http://{}".format(url)))
print("Done")
