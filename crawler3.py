import urllib2
from bs4 import BeautifulSoup
import time
import json
import csv
start_time=time.time()

def make_trie(trie, word):
	if type(word) != str:
		print "Trie only works on strings\n"
	temp_trie=trie
	for letter in word:
		temp_trie= temp_trie.setdefault(letter, {})
	temp_trie=temp_trie.setdefault('_end_','_end_')
	return trie

def in_trie(trie, word):
	if type(word) != str:
		print "Trie only works on strings\n"
	temp_trie=trie
	for letter in word:
		if letter not in temp_trie:
			return False
		temp_trie=temp_trie[letter]
	return True
def make_trie2(trie, word):
	if type(word) != str:
		print "Trie only works on strings\n"
	temp_trie=trie
	for letter in word:
		temp_trie= temp_trie.setdefault(letter, {})
	temp_trie=temp_trie.setdefault('_end_','_end_')
	return trie

def in_trie2(trie, word):
	if type(word) != str:
		print "Trie only works on strings\n"
	temp_trie=trie
	for letter in word:
		if letter not in temp_trie:
			return False
		temp_trie=temp_trie[letter]
	return True

def remove_from_trie(trie, word,depth):
	if word and word[depth] not in trie:
		return False
	if len(word) == depth +1:
		del trie[word[depth]]
		if not trie:
			return True
		return False
	else:
		temp_trie=trie
		if remove_from_trie(temp_trie[word[depth]], word, depth+1):
			if temp_trie:
				del temp_trie[word[depth]]
			return not temp_trie
		return False

def crawl(seeds,mainlink):
	frontier=seeds
	visited_urls=[]
	nooflink=1
	i=0
	trie={}
	trie2={}
	a=1	
	for crawl_url in frontier:
		if in_trie(trie,crawl_url)== False:
			print "Crawling :",crawl_url
			make_trie(trie,crawl_url)
			make_trie2(trie2,crawl_url)
			try:
				c=urllib2.urlopen(crawl_url)
				print "Crawled",a
			except:
				print "Could not access:",crawl_url
				continue
	
			content_type = c.info().get('Content-Type')
			if not content_type.startswith('text/html'):
				continue
			
			nooflink=nooflink-1
			soup=BeautifulSoup(c.read())
			links=soup('a')
			for link in links:
				if 'http://' in link.get('href'):
					url=link.get('href')
					list=[link.string,url]
				elif 'https://' in link.get('href'):
					url=link.get('href')
					list=[link.string,url]
				elif ';' in link.get('href'):
					url=mainlink
					list=[link.string,url]
				elif '?' in link.get('href'):
					url=mainlink
					list=[link.string,url]
				elif '%' in link.get('href'):
					url=mainlink
					list=[link.string,url]
				elif link.get('href')=='/':
					url=mainlink
					list=[link.string,url]
				elif '#' in link.get('href'):
					url=mainlink
					list=[link.string,url]
				else:
					url=mainlink + link.get('href')
					list=[link.string,url]
					
					if in_trie2(trie2,url)==False:
						f=open("linkslist2.txt","a+") 
						f.write(url+'\n')
						f.close()
						frontier.append(url)
						make_trie2(trie2,url)
						with open("%s.csv" %crawl_url.replace('/','.'),"a") as csv_file:
							writer=csv.writer(csv_file,delimiter=',')
							writer.writerow(list)
			yo= soup.prettify()
			f=open("%s.txt" %crawl_url.replace('/','.'),"a+") 
			f.write(yo.encode('utf8'))
			f.close()
			i=i+1
			if a>99:
				break
			a=a+1
			
		else:
			continue
	print(json.dumps(trie, indent=1))
	print("---%s---"%(time.time()-start_time))		
			
if __name__ == '__main__':		
	f=open("starturl.txt","r")
	x=[]
	for line in f:
		y=line.rstrip('\n')
		x.append(line.rstrip('\n'))
	f.close()
	crawl(x,y)


