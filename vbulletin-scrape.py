#!C:\Python27
# -*- coding: utf-8 -*-

'''
Scrapes vBulletin version up to 4.2.x
Prints posts to terminal on thread can be used to pipe to stdout or text file
for more manipulation

python vbulletin-scrape.py -i http://url.here

TODO: Auto increment until end of thread
'''

import re
import argparse
import requests
from lxml import etree, html

aparser = argparse.ArgumentParser()
aparser.add_argument('-i', '--input', nargs='+', required=True, action='store', 
                    dest="ifile", help="vbulletinscrape.py -i <inputurl>")
args = aparser.parse_args()
urls = args.ifile

find_body_xpath = etree.XPath('.//*[starts-with(@id, "post_message_")]')

sesh = requests.Session()

for url in urls:
    r = sesh.get(url, verify=True)
    if r.status_code == 200:
        htmldata = html.fromstring(r.text)
    else:
        print "could not reach %s page" % (url)
    
    for i in range(len(htmldata)):
        xpath_span = range(len(find_body_xpath(htmldata)))
    
    hitamt = int(str(xpath_span[-1:]).strip("[]")) + 1
    
    for hit in xpath_span:
        all_hits = find_body_xpath(htmldata)[hit].text_content()
        all_hits = re.sub(r"(\s)+", ' ', all_hits)
        #all_hits = all_hits.encode("utf-8")
        if hit == 0:
            print "\n\n%s has %s hits\n-----------------------------------------" \
            "---------------------------------------\n" % (url, str(hitamt))
        print "HIT #%s: %s" % (hit + 1,  all_hits.encode("utf-8").join("\n\n"))
        '''
        with open("results.txt", "w") as fexport:
            for u in all_hits:
                fexport.write("%s" % (u))
        '''
sesh.close()
