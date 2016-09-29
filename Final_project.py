tho## Final Project
## Robert Farb

## import statements
import test
import json
import urllib
import urllib2
import requests_oauthlib
import webbrowser
import operator


## Pretty function
def pretty(obj):
	return json.dumps(obj, sort_keys=True, indent=2)
	
## Positive word list
pos_ws = []
f = open('positive-words.txt', 'r')

for l in f.readlines()[35:]:
    pos_ws.append(unicode(l.strip()))
f.close()

## Negative word list
neg_ws = []
f = open('negative-words.txt', 'r')
for l in f.readlines()[35:]:
    neg_ws.append(unicode(l.strip()))

## Twitter Oauth
client_key = 'ksbx3TufNo0FiZFkZCrw5LIDz'
client_secret = 'tUn9VW5PX1qltEIuwdUrDcuSGArBleZE7s1ETnJbU5AWH0082G'

## Twitter Class
class Tweet():
	def __init__(self, tweet_dict):
		if 'text' in tweet_dict:
			self.text = tweet_dict['text']
		else:
			self.text = ""
		
		if 'retweet_count' in tweet_dict:
			self.retweet_count = tweet_dict['retweet_count']
		else:
			self.retweet_count = 0
		
		if 'favourites_count' in tweet_dict:
			self.favourites_count = tweet_dict['favourites_count']
		else:
			self.favourites_count = 0



	def positive(self):
		pos = [word for word in pos_ws if word in self.text]		
		return len(pos)
                   
	def negative(self):
		negs = []
		for word in neg_ws:
			if word in self.text.split() and word not in negs:
				negs.append(word)
		return len(negs)

	def emo_score(self):
		return p.positive() - p.negative()

		

## Getting the Twitter token
def get_tokens():
	oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)
	request_token_url = 'https://api.twitter.com/oauth/request_token'
	fetch_response = oauth.fetch_request_token(request_token_url)
	
	resource_owner_key = fetch_response.get('oauth_token')
	resource_owner_secret = fetch_response.get('oauth_token_secret')
	
	base_authorization_url = 'https://api.twitter.com/oauth/authorize'
	authorization_url = oauth.authorization_url(base_authorization_url)
	
	webbrowser.open(authorization_url)
	verifier = raw_input('Please input the verifier')
	
	oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)  
                                                       
	access_token_url = 'https://api.twitter.com/oauth/access_token'
	oauth_tokens = oauth.fetch_access_token(access_token_url)
	resource_owner_key = oauth_tokens.get('oauth_token')
	resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    
	return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)

## Putting the Information in the file "Creds.txt"
try:
    f = open("creds.txt", 'r')
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = json.loads(f.read())
    f.close()
except:
    tokens = get_tokens()
    f = open("creds.txt", 'w')
    f.write(json.dumps(tokens))
    f.close()
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = tokens
  

protected_url = 'https://api.twitter.com/1.1/account/settings.json'
oauth = requests_oauthlib.OAuth1Session(client_key,
                        client_secret=client_secret,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret)
r = oauth.get(protected_url)

## The user inputs a topic to get feedback about 
search_parameter = raw_input("Please input a topic you would like to see Twitter and USA Today statistics for")


## Two functions to encode the user input to work for the urls
def usa_encode_search(input):
	usa_correct_search = input
	for x in input:
		if x == ' ':
			usa_correct_search = input.replace(' ', '+') 
	return usa_correct_search

def twitter_encode_search(input):
	twitter_correct_search = input
	for x in input:
		if x == ' ':
			twitter_correct_search = input.replace(" ", "%20")
	return twitter_correct_search
	
usa_encoded_search = usa_encode_search(search_parameter)
twitter_encoded_search = twitter_encode_search(search_parameter)

## I am getting a list of tweets about Michael Brown with no specific location parameter.
tweets = []
max_id = None
my_params = {'count' : 20}
for i in range(5):
	if len(tweets) > 0:
		my_params['max_id'] = min(ids) - 1
	t = oauth.get("https://api.twitter.com/1.1/search/tweets.json?q="+twitter_encoded_search+"&count=50",
                params = my_params)
tweet_dict = t.json()
for x in tweet_dict['statuses']:
	text = x['text']
	tweets.append(text)

## Encoding the list so it is no longer unicode.	
tweet_list = [x.encode('UTF8') for x in tweets]
## Now I have a list of tweets Relating to "Michael Brown"


## Now I am going to get a list of Tweets related to "Michael Brown" Within 20 miles of Ferguson, MO
Ferg_tweets = []
max_id = None
my_params = {'count' : 20}
for i in range(5):
	if len(Ferg_tweets) > 0:
		my_params['max_id'] = min(ids) - 1
	t2 = oauth.get('https://api.twitter.com/1.1/search/tweets.json?q='+twitter_encoded_search+'&geocode=38.7442%2C-90.3053%2C30mi&count=60',
					params = my_params)
Ferg_tweet_dict = t2.json()
for thing in tweet_dict['statuses']:
	text = thing['text']
	Ferg_tweets.append(text)

## Encoding the list so it's no longer unicode	
Ferg_tweet_list = [x.encode('UTF8') for x in Ferg_tweets]
##print Ferg_tweet_list

## Emotion Score of tweets
def emo_score(self):
	pscore = self.positive()
	nscore = self.negative()
	emoscore = (pscore - nscore)
	return emoscore

## Writing a CSV file to store the Emotion score, Retweet Count and Favorite Count of Tweets about Michael Brown with no location parameters
Tweet_emotion = open("tweet_emotion_scores.csv","w")
Tweet_emotion.write("Emotion Score, Retweet Count, Favorite Count\n")

for x in tweet_dict['statuses']:
	for y in x['text']:
		t = Tweet(x)
		retweet_count = t.retweet_count
		favorite_count = t.favourites_count
		t_emo_score = emo_score(t)
	Tweet_emotion.write("%d, %d, %d, \n" %(t_emo_score, retweet_count, favorite_count))
Tweet_emotion.close()

## Writing a CSV file to store the Emotion score, Retweet count, and Favorite count of tweets within 20 miles of Ferguson
Ferg_tweet_emotion = open("Ferg_tweet_emotion.csv", "w")
Ferg_tweet_emotion.write("Emotion Score, Retweet, Favorite Count\n")


## I am expecting these emotion scores to be much lower since they are in and around Ferguson Missouri.
for x in Ferg_tweet_dict['statuses']:
	for y in x['text']:
		t2 = Tweet(x)
		ferg_retweet_count = t2.retweet_count
		ferg_favorite_count = t.favourites_count
		t2_emo_score = emo_score(t2)
	Ferg_tweet_emotion.write("%d, %d, %d, \n" %(t2_emo_score, ferg_retweet_count, ferg_favorite_count))
Ferg_tweet_emotion.close()



## Accumulating a list of all the hashtags from tweets about Michael Brown.
def hashtag_list(tweet_dict):
	hashtag_lst = []
	for x in tweet_dict['statuses']:
		for y in x['entities']['hashtags']:
			hashtag = y['text']
			hashtag_lst.append(hashtag)
	return hashtag_lst


## Encoding the list so it is no longer unicode
uni_hashtag_lst = hashtag_list(tweet_dict)
hashtag_lst = [x.encode('UTF8') for x in uni_hashtag_lst]
## I am creating a dictionary of hashtags and how often they occur. 
## I will show which hashtags are most common surrounding this topic.
hashtag_dict = {}
for x in hashtag_lst:
	if x not in hashtag_dict:
		hashtag_dict[x] = 1
	else:
		hashtag_dict[x] = hashtag_dict[x] + 1

sorted_hashtag_dict = sorted(hashtag_dict.items(), key=operator.itemgetter(1), reverse = True)

## Encoding the list so it is no longer in Unicode.
uni_ferg_hashtag_lst = hashtag_list(Ferg_tweet_dict)
ferg_hashtag_lst = [x.encode('UTF8') for x in uni_ferg_hashtag_lst]
## I am creating a dictionary of hashtags from tweets within 20 miles of Ferguson and how often they occur.
## I will show which hashtags are most common surrounding this topic near Ferguson, and contrast it to the hashtags with no location parameters.
ferg_hashtag_dict = {}
for x in ferg_hashtag_lst:
	if x not in ferg_hashtag_dict:
		ferg_hashtag_dict[x] = 1
	else:
		ferg_hashtag_dict[x] = ferg_hashtag_dict[x] + 1

sorted_ferg_hashtag_dict = sorted(ferg_hashtag_dict.items(), key = operator.itemgetter(1), reverse = True)

# I am going to show the top three hashtags from around Ferguson, and with no location parameters. 
def top_five(lst):
	for x in lst[0:5]:
		print "#"+x[0]



print "Top Five Hashtags about "+search_parameter+" from around the Nation"
print "-------------------------------------------------------------"
top_five(sorted_hashtag_dict)
print "\n"


print "Top Five Hashtags about "+search_parameter+" within 20 miles of Ferguson."
print"--------------------------------------------------------------------"
top_five(sorted_ferg_hashtag_dict)
print "\n"


## Making a list of politically incorrect words
politic_incorrect_wds = []
p = open('politically-incorrect-words.txt', 'r')
for l in p.readlines()[:]:
    politic_incorrect_wds.append(l.strip())
p.close()


## Now I am going to Request the USA Today API for articles related to Michael Brown and Ferguson
usa_today_key = 'hyymdt75m273dndekhhwfpqu'
usa_today_response = urllib2.urlopen('http://api.usatoday.com/open/articles?tag='+usa_encoded_search+'&encoding=json&api_key=hyymdt75m273dndekhhwfpqu')
txt = usa_today_response.read()  ## Returns the response as a string
usa_today_dict = json.loads(txt)
## print pretty(usa_today_dict)

## This is making a a list of the descriptions of the USA Today articles
descript_list = []
for thing in usa_today_dict['stories']:
	description = thing['description']
	descript_list.append(description)

description_list = [x.encode('UTF8') for x in descript_list]
## print description_list

## Defining a function that will return the political correctness score 0 being the most politically correct.
def political_correctness(list):
	political_score = 0
	for tweet in list:
		y = tweet
		for word in politic_incorrect_wds:
			if word in y:
				political_score = political_score + 2
	return political_score


print "Political Correctness Score of Tweets from around the World."
print political_correctness(tweet_list)
print "\n"

print "Political Correctness Score of Tweets within 20 miles of Ferguson."
print political_correctness(Ferg_tweet_list)
print "\n"


print "Political Correctness Score of USA today Articles"
print political_correctness(description_list)
print "\n"

	
test.testEqual(type(political_correctness(tweet_list)), type(0))
test.testEqual(usa_encode_search("Michael Brown"), ("Michael+Brown"))
test.testEqual(twitter_encode_search("Apple Iphone"), ("Apple%20Iphone"))
test.testEqual(type(hashtag_list(tweet_dict)), type([]))
test.testEqual(type(t2.retweet_count), type(0))