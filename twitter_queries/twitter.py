from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager
from collections import Counter
import pandas as pd
from pandas import DataFrame, Series
import os

### Set working directory and open file
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# Note: you may need to replace credentials with your own
o = TwitterOAuth.read_file('credentials.txt')
print (o.access_token_key)
twitter = TwitterAPI(o.consumer_key,
                 o.consumer_secret,
                 o.access_token_key,
                 o.access_token_secret)
                 

### Query twitter for topic "big+data"
response = twitter.request('search/tweets', {'q': 'big+data',  'count':100})
tweets = [r for r in response]

# Identify a user
user = tweets[0]['user']
print ('screen_name={a}, name={b}, location={c}'.format(a=user['screen_name'], b=user['name'], c=user['location']))

# Identify a user's follower
screen_name = user['screen_name']
response  = twitter.request('followers/list', {'screen_name': screen_name, 'count':200})
followers = [follower for follower in response]
print ('found {a} followers for {b}'.format(a=len(followers), b=screen_name))
print ('''The first follower in the list is '{}\''''.format(followers[0]['screen_name']))

# Print the user's timeline
timeline = [tweet for tweet in twitter.request('statuses/user_timeline',
                                                {'screen_name': screen_name,
                                                 'count': 15})]
print ('got {a} tweets for user {b}'.format(a=len(timeline), b=screen_name))

# Print user's timeline (limit to first 5 in list)
print ('\n\n\n'.join(t['text'] for t in timeline[:5]))

# Identify most common words in timeline
counts = Counter()
for tweet in timeline:
    counts.update(tweet['text'].lower().split())
print ('found {a} unique terms in {b} tweets'.format(a=len(counts), b=len(timeline)))
counts.most_common(10)
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
print ('\n'.join('%s=%d' % (term[0], term[1]) for term in sorted_counts[:10]))


### Begin to query information about 2016 US presidential candidates' twitter "friends"
LOT_presidentialCandidates = [('HillaryClinton', 'D'), 
                              ('MartinOMalley', 'D'), 
                              ('BernieSanders', 'D'),
                              ('realDonaldTrump', 'R'),
                              ('JebBush', 'R'),
                              ('RealBenCarson', 'R'),
                              ('ScottWalker', 'R'),
                              ('CarlyFiorina', 'R'),
                              ('GovMikeHuckabee', 'R'),
                              ('DrRandPaul', 'R')]

candidatesFriends={}
for candidate in  LOT_presidentialCandidates:
    response = twitter.request('friends/list', {'screen_name': candidate[0], 'count':200})
    friends = [r for r in response]
    print ('{a} has {b} friends.'.format(a=candidate[0],b=len(friends)))
    candidatesFriends[candidate[0]]=friends

# Separate candidates by party.
republicans = [candidate[0] for candidate in LOT_presidentialCandidates if candidate[1] == 'R']
democrats = [candidate[0] for candidate in LOT_presidentialCandidates if candidate[1] == 'D']
print ('{a} republicans, {b} democrats'.format(a=len(republicans), b=len(democrats)))
print ('Republicans:\n{a}'.format(a=republicans))
print ('Democrats:\n{a}'.format(a=democrats))

# Find most commons friends amongst Republican candidates
print('popular Republican friends:')
republican_counts = Counter()
for candidate in  LOT_presidentialCandidates: 
    if candidate[0] in republicans:
        for friend in candidatesFriends[candidate[0]]:
            republican_counts[friend['screen_name']] += 1
print republican_counts.most_common(15)


# Find most common friends amongst all candidates (using alternative method)
friendFollowers = pd.DataFrame(columns=list(['ScreenName','Name']))
for candidate in LOT_presidentialCandidates:
    for friend in candidatesFriends[candidate[0]]:
        a = friend['screen_name']
        b = friend['name']
        df = pd.DataFrame([[a,b]], columns=list(['ScreenName','Name']))
        friendFollowers = friendFollowers.append(df, ignore_index=True)
friendList = friendFollowers['ScreenName'].value_counts().head(15)
print ('The top 15 friends followed by all candidates are:\n{a}'.format(a=friendList))

# Find most popular friends of Democrat candidates
demFriendsFollowers = []

for candidate in LOT_presidentialCandidates:
    if candidate[0] in democrats:
        for friend in candidatesFriends[candidate[0]]:
            a = friend['screen_name']
            b = friend['followers_count']
            demFriendsFollowers.append([a,b])

demFriendsFollowers = pd.DataFrame(demFriendsFollowers, columns=(['ScreenName','FollowerCount']))
demReadout = demFriendsFollowers.sort_values('FollowerCount',ascending=False).drop_duplicates(subset='ScreenName').head(10).reindex()
print(demReadout.to_string(index=False))