#Collects the most recent post from a source 
#Tracks the comments on the post to see how the ranking changes
#Tracks who likes the top 3 comments 
#Records every 10 minutes
#Outputs all data in a spreadsheet syntax
import csv
import sys
from datetime import datetime
import json
import time
import sched
import urllib2

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

def createFile():
	dateName = time.strftime("%c") + '.txt'
	dateName = dateName.replace(" ", "_")
	print dateName

	try:
		file = open(dateName,'w')   # Trying to create a new file or open one
		file.close();
		return dateName

	except:
		print('Something went wrong! Can\'t tell what?')
		sys.exit(0)

    

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
	s = sched.scheduler(time.time, time.sleep)

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
		#process id
		post_id = post_id.split("_", 1)[1]
		print post_id

		print status_published
		print utc_now

		#post_date = status_published[1]
		#utc_date = utc_now[1]

		#Time difference
		tdelta = utc_now - status_published
		tdelat_min = tdelta.seconds/60
		print tdelta

		#Check first to see if it's on the same day and within 5 mintues of publishing. 
		#We want to get a post as early as possible
		if tdelat_min > 0 and tdelat_min < 5:
			print "Got one!"
			done = False
			# return post_id

		# done = False
		#Waits for 5 minutes, saves some time
		# time.sleep(60*5) UNCOMMENT LATER ON
		return post_id #COMMENT OUT AFTER SAVING

	#returns the whole json object
	return post_id

#Process the whole comment to put some neat data points
def process_comment(comment_id):
	comment_id = comment_id.split("_", 1)[1]
	return comment_id
def get_top_comments(status_id, access_token, num_comments):

    # Construct the URL string
    base = "https://graph.facebook.com"
    node = "/%s/comments" % status_id 
    fields = "?fields=id"
    parameters = "&limit=%s?access_token=%s" % (num_comments, access_token)
    url = base + node + fields + parameters 
    #fields +
    # retrieve data
    data = request_until_succeed(url)
    if data is None:
        return None
    else:   
        return json.loads(data)

#Gets all reactions 
#Returns number of reactions for each type
# def get_reactions(comment_id):
# 	#convert id to something that the graph api can understand
# 	comment_id = comment_id.split("_", 1)[1]

# 	return comment_id
#Gets person's id
def person(reaction_id):
	return
def run_everything():
	#Get's url of Facebook page
	#Set page id manually in line 19
	fileName = createFile()
	print fileName
	post_id = get_most_recent()
	num_comments = 3
	topComments = get_top_comments(post_id, access_token, num_comments)["data"]
	print topComments

	#FIGURE OUT HOW TO GET ID
	#for loop to analyze each comment
	for x in xrange(num_comments):
	 	process_comment(topComments["id"])

	#postJSON = json.dumps(get_most_recent())
	with open(fileName, "a") as myfile:
		myfile.write(topComments)
	return

run_everything();
