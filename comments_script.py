#Collects the most recent post from a source 
#Tracks the comments on the post to see how the ranking changes
#Tracks who likes the top 3 comments 
#Records every 10 minutes
#Outputs all data in a spreadsheet syntax

import urllib2
import json
import datetime
import csv
import time
from datetime import datetime

app_id = "1603715373026421"

app_secret = "37707056385dd5a3633855283030ae61"

access_token = app_id + "|" + app_secret

page_id = 'Vox'

#Return Time in UTC
def UtcNow():
    now = datetime.datetime.utcnow()
    return now

def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)
            
            print "Error for URL %s: %s" % (url, datetime.datetime.now())

    return response.read()

#Gets time of the post
def get_time_of_post_recent(page_id, access_token, num_statuses):
	 # construct the URL string
    base = "https://graph.facebook.com"
    node = "/" + page_id + "/feed" 
    parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, access_token) # changed
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    return data

#Gets most recent post on a politcal page
def get_most_recent():
	print "Waiting till a new post occurs"

	done = True
	post_id = None

	while done:
		#Post object (most recent post)
		post = get_time_of_post_recent(page_id, access_token, 1)["data"][0]
		#print json.dumps(post, indent=4, sort_keys=True)
		post_json = json.dumps(post)
		#print post_json
		post_json = json.loads(post_json)

		#Get current Date object to compare to Facebook post (in UTC)
		utc_now = datetime.utcnow()
		utc_now.strftime('%Y-%m-%dT%H:%M:%S+0000')

		#Time in UTC
		post_time = post_json['created_time']
		status_published = datetime.strptime(post_time,'%Y-%m-%dT%H:%M:%S+0000')
		#status_published.split(" ")

		#ID for post to be used for analyzing
		post_id = post_json['id']
		print post_id

		print status_published
		print utc_now

		#post_date = status_published[1]
		#utc_date = utc_now[1]

		#Time difference
		tdelta = utc_now - status_published
		tdelat_min = tdelta.seconds/60
		print tdelta

		#Check first to see if it's on the same day
		
		if tdelat_min > 0 and tdelat_min < 5:
			print "Got one!"
			done = False
			return post_id

		done = False

	
	

	return

#Gets top 3 comments
def get_top_comments(post_id):
	return
#Gets all reactions
def get_reactions(comment_id):
	return
#Gets person's id
def person(reaction_id):
	return
def run_everything():
	#Get's url of Facebook page
	page_id = raw_input("Enter a page_id: ")
	get_most_recent(page_id)
	return

get_most_recent();
