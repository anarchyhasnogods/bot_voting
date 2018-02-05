from websocket import create_connection
from steem import Steem
import steem
import time
import random
import math

from memo_saving import interpret
from memo_saving import main

class Post_holder:


    def __init__(self, max_posts, max_time, sending_account, key, memo_account):
        # Max time is seconds
        self.max_posts = max_posts
        self.max_time = max_time
        self.post_list = []
        self.post_draw_list = []
        self.sending_account = sending_account
        self.key = key
        self.memo_account = memo_account

    def add_post(self, post_link, submission_author, post_author):
        # post_list = [[postname, submission author, vote list, advertisement_total]]

        ad_tokens = 0

        account_info_post = interpret.get_account_info(post_author) # Gets info on post author

        for i in range(0, int(len(account_info_post[2])), 2): # Finds and adds together all kinds of ad tokens
        
            if account_info_post[2][i] == "ad-token-perm":
                ad_tokens += int(account_info_post[2][i+1])
                print(int(account_info_post[2][i+1]))
            elif account_info_post[2][i] == "ad-token-temp":
                ad_tokens += int(account_info_post[2][i+1])
        # uses add tokens to calculate visibility within system, and save information needed for later.
        self.post_list.append([post_link, submission_author, [], 10 + int(math.sqrt(ad_tokens)), time.time()])




    def add_vote(self, vote, post):
        # vote = [voter, vote]
        # vote is either -1, 0 or +1
        # -1 = plag, 0 = ignore, +1 = vote for
        # goes through every post and checks if it is the correct one, then every voter to see if it has been voted on already

        already_voted = False
        for i in self.post_list:
            if post == i[0]:
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

            memo_pos = interpret.vote_post(i[0], i[1], i[4], votes / len(i[2]),  self.memo_account, self.sending_account, self.key)
            for ii in i[2]:
                interpret.update_account(ii[0], self.sending_account,self.memo_account ["vote", str(ii[1]) + "|"
                                                                                       + str(memo_pos)], self.key)









interpret.update_account("name","anarchyhasnogods","space-pictures",["add1","add2"], "5JFZVDDCmDSkYJKjsdVUzufxhYoNFR2KUSkox4sbVfutQp6DsSK")
#post_thing = Post_holder(100,1000)
#for i in range(10):
 #   post_thing.add_post(str(i),str(i),"x")
#print("x")
while True:
    #print(1,post_thing.get_random())
    #print(2,post_thing.random_posts)
    break





