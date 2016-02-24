# In this script I am looking at the "states" in the "us" where 
# people are using meetup.com to organize an event. The script is looking at the incoming json to keep track of the 
# places where an event is organized.
# The key here is that, the script records the state of an event as a key to the dictionary and
# uses the time of the event as the value for the corresponding key.
# The interesting part is that it keeps track of the state where a meeting has been organized, if there is an existing key,
# the script calculates the difference in the time of event of the two JSON messages and then, it removes the previous existing 
# event, deletes it from the dictionary and put the new event as a replacement for the previous
import requests
import json
import time
import codecs
from datetime import datetime
from sys import stdout
import sys
reload(sys)  
sys.setdefaultencoding('utf-8') 

# this script polls the meetup API, 



b = {}
#print ("Loading the json")
# get the meetup response from the API and setting stream to true
meetUp = requests.get("http://stream.meetup.com/2/rsvps", stream=True)
#creating an iterator for json request response 
for meetUp_next in meetUp.iter_lines():
    
    try:
        # loading and decoding to avoide getting a utf-error
        m = json.loads(meetUp_next.decode('utf-8'))
        # to check if the corresponding tuple of m has the key we are looking for the group
        if "group" in m:
            # To check if the group_country of the event is us. I am only taking note of the events in US
            if m["group"]["group_country"] == "us" or m["group"]["group_country"] == "US":
                # recording the group_state of the event
                group_state = m["group"]["group_state"]
                # if the group_state is not in the dictionary
                if group_state not in b:
                    # add it to the dictionary
                    b[group_state]=m["event"]["time"]
                else:
                    # if there is an existing record, calculate the absolute diff in the time of the two events and convert them into hours
                    diff = (abs(m["event"]["time"] - b[group_state]))/(24*60*60*1000)
                    # delete from the dictionary the value corresponding to the previous key
                    del b[group_state]
                    # Add the value of the time to previous key
                    b[group_state]=m["event"]["time"]
                    # Print JSON to stdout, to be processed by diff.py.
                    print(json.dumps({"t": diff}))
                    # As always, flush stdout to get it to print without getting put in a buffer!
                    stdout.flush()
    except:
        continue