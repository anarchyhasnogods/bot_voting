from websocket import create_connection
from steem import Steem
import steem
import time
import random
import math

from memo_saving import interpret
from memo_saving import main
import json

class Post_holder:
    def __init__(self, max_posts, max_time, sending_account, key, memo_account,nodes,posting_key, vote_threshold):
        self.vote_threshold = vote_threshold # min vote ratio for a vote
        self.average_post = interpret.get_vote_amount()

        print("VOTE AMOUNT")
        print(self.average_post)
        self.posting_key = posting_key
        # [average post, time period]
        # for average vote calculation, uses average of 10 full 100 % votes(1000) and devides it by average (voted on) posts
        # Max time is seconds
        self.max_posts = max_posts
        self.max_time = max_time
        self.post_list = []
        self.post_draw_list = []
        self.sending_account = sending_account
        self.key = key
        self.memo_account = memo_account
        self.votes_finished = False
        self.nodes = nodes
        self.account_info = {}
        self.ratio_num = 0.75


    def add_post(self, post_link, submission_author, post_author):
        # post_list = [[postname, submission author, vote list, advertisement_total]]

        # gets account info for reward calculation
        account_info_post = interpret.get_account_info(post_author)[2] # Gets info on post author
        ad_tokens = int(account_info_post["ad-token-perm"])  # + int(account_info_post["ad-token-temp"])
        self.account_info[post_link] = account_info_post
        # uses add tokens to calculate visibility within system, and save information needed for later.
        self.post_list.append([post_link, submission_author, [], 10 + int(math.sqrt(ad_tokens)), time.time(), post_author])



    def add_vote(self, vote, post):
        # vote = [voter, vote]
        # vote is either -1, 0 or +1
        # -1 = plag, 0 = ignore, +1 = vote for
        # goes through every post and checks if it is the correct one, then every voter to see if it has been voted on already
        print(vote,post)
        already_voted = False
        for i in self.post_list:
            if post[0] == i[0]:
                for ii in i[2]:
                    if ii[0] == vote[0]:
                        already_voted = True #so that it changes it instead of adding a new vote onto the end
                        ii[1] = vote[1]
                        break
                if not already_voted:
                    i[2].append(vote)
                else:
                    break



    def set_random(self):
        # takes list of all posts produced earlier and shuffles them visibility is based on amount of post in list
        # the amount in the list is based on the number assigned earlier
        self.random_posts = []
        for i in self.post_list:
            for ii in range(i[3]):
                self.random_posts.append(i)
        random.shuffle(self.random_posts)

    def get_random(self):
        # finds the next post in the random order and removes it
        # when it runs out it just creates the list again
        # this forces the posts to be seen roughly the same amount of times as their chance
        try:
            if len(self.random_posts) == 0:
                self.set_random()
            return self.random_posts.pop(0)
        except AttributeError:
            self.set_random()
            return self.get_random()


    def finish_post_set(self):
        account_update_list = [] # calculates the total votes of each post
        for i in self.post_list:
            votes = 0
            for vote in i[2]:
                if vote[1] == 1:
                    in_list = False
                    for ii in account_update_list:
                        if ii[0] == vote[0]:
                            in_list = True
                            ii[1].append(i[0])
                            break

                    votes += 1

            # Make post memo, link to in vote memo
            ratio = votes/len(i[2])
            vote_size = self.make_vote(ratio,i[0])
            memo_pos = interpret.vote_post(i[0], i[1], i[4],i[2], votes / len(i[2]),  self.memo_account, self.sending_account, self.key,random.choice(self.nodes), vote_size)
            for ii in i[2]:
                #interpret.update_account(ii[0], self.sending_account,self.memo_account )
                pass
            self.votes_finished = True
#--------------------------------------
# FINISH

    def make_vote(self, ratio, post_link):
        if ratio < self.vote_threshold:
            return 0
        upvote_tokens = self.account_info[post_link]["token-upvote-perm"] + self.account_info[post_link]["token-upvote-temp"]
        print("UPVOTE TOKENS", upvote_tokens)

        equation = self.average_post[0] * (math.sqrt(upvote_tokens)/25 + 1) * (ratio/self.average_post[1])
        if equation > 100:
            equation = 100

        for i in nodes:
            try:
                steem = Steem(node=i, keys=self.posting_key)
                steem.vote(post_list, equation, account=self.sending_account)
                return equation
            

            except:
                pass
        return 0
#----------------------------------------

post_holder = Post_holder(100,1000000,"anarchyhasnogods","KEY","space-pictures",["wss://rpc.buildteam.io"],"posting_key", 0.5)
for i in range(5):
    post_holder.add_post("post-link"+str(i), "0","1")

print(post_holder.post_list)

post_list = []

for i in range(250):

    post_list.append(post_holder.get_random())
    pass


# is [0]
for i in range(len(post_list)):
    print(i)
    post_holder.add_vote(["account" + str(i),random.randrange(3)-1],post_list[i])





print(post_holder.post_list)

post_holder.finish_post_set()

