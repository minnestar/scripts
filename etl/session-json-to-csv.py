"""
This program will read the JSON data from the sessions system and
turn it into a CSV file that Mediawiki can load using the Data Transfer
extensions.

Jamie Thingelstad
jamie@thingelstad.com

"""

import json
import csv
import urllib2
import commands

req="http://sessions.minnestar.org/events/2.json"
data= urllib2.urlopen(req).read()
x=json.loads(data)

f=csv.writer(open("output.csv","wb+"))

# Write CSV Header, If you dont need that, remove this line
f.writerow(["Title", "Session[Event]", "Session[Presenter]", "Free Text"])
out_event = x["event"]["name"]

for x in x["event"]["sessions"]:
    out_title = x["title"].encode('ascii', 'ignore') 
    out_title = out_title.replace('"','')
    out_title = out_title.replace('/','')
    out_title = out_title.replace('!','')
    out_title = out_title.replace('*','')
    
    # This is ugly, but I couldn't get pandoc to work via pyandoc
    # and since I don't care about speed, we'll do this with files!    
    # Write the markdown to a file
    g = open('temp.md', "w")
    g.write(x["description"].encode('ascii', 'ignore'))
    g.close
    del(g)
    # Use pandoc to convert markdown to mediawiki
    out_description = commands.getoutput('/usr/local/bin/pandoc -f markdown -t mediawiki temp.md')
    
    out_presenter = x["participant"]["name"].encode('ascii', 'ignore') 
    
    print "Writing " + out_title
    f.writerow([out_title, out_event, out_presenter, out_description])

	
