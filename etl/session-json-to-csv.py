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
import time
from datetime import datetime
from datetime import timedelta
from pytz import timezone

def bool2str(v):
    if v:
        return "Yes"
    else:
        return "No"

req="http://sessions.minnestar.org/events/3.json"
data= urllib2.urlopen(req).read()
x=json.loads(data)

f=csv.writer(open("output.csv","wb+"))

# Write CSV Header, If you dont need that, remove this line
f.writerow(["Title",
	"Session[Event]",
        "Session[Summary]"
	"Session[Presenter]",
	"Session[Projector]",
	"Session[Panel]",
        "Session[Room]",
	"Session[Start hour]",
	"Session[Start minute]",
	"Session[End hour]",
	"Session[End minute]",
	"Free Text"])

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
    
    out_presenter = ', '.join(x["presenter_names"]).encode('ascii', 'ignore') 
    out_summary = x["summary"].encode('ascii', 'ignore')
    out_panel = bool2str(x["panel"])
    out_projector = bool2str(x["projector"])
    out_room = x["room_name"]

    out_time = x["starts_at"]
    start_time = datetime.strptime(out_time, "%Y-%m-%dT%H:%M:%S-05:00")
    start_time = start_time.replace(tzinfo=timezone('US/Central'))
    out_start_hour = start_time.strftime("%I")
    out_start_minute = start_time.strftime("%M")
    end_time = start_time + timedelta(minutes=45)
    out_end_hour = end_time.strftime("%I")
    out_end_minute = end_time.strftime("%M")
 
    print "Writing " + out_title
    f.writerow([out_title, out_event, out_summary, out_presenter, out_projector, out_panel, 
        out_room, out_start_hour, out_start_minute, out_end_hour, out_end_minute, out_description])

	
