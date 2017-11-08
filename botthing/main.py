import mysqlhelper





import requests
import json
import time
import math
import websocket
from websocket import create_connection
from steem import Steem



class Main():
    node_list = []


    def __init__(self, bot_number):
        keys = mysqlhelper.get_keys(bot_number)

        self.posting_key = keys[1]
        self.account_name = keys[0]
        self.start_time = time.time()
        self.bot_number = bot_number


        # First is total, second is time it started, third is average
        # The second is the average time between the last 5, in blocks of 5
        self.broken_nodes = []
        self.check_vars()





    def check_update(self):
        return mysqlhelper.check_update(self.bot_number)




    def check_vars(self):
        # This function sets all of the variables needed based on those in the database

        # Var list

        var_list = mysqlhelper.get_vars(self.bot_number)

        self.plagiarism_threshold = var_list[0]
        self.upvote_threashold = var_list[1]
        self.token_exponent = var_list[2] # single number, fraction for sub linear, 1 for linear, above one for exponential
        # First is upvote, second is advertising, third is post review
        # forth is temporary upvote, fith is temp advertising
        self.token_offset = var_list[3] # Base number, what we give them when they have no tokens,
        self.token_multiplyer = var_list[4] # Number we multiply the tokens by, after the exponent

        self.nodes = var_list[5]

        self.time_period = var_list[6] # Time period for running averages for voting calculation

        self.voting_power_threshold = var_list[7]
        self.upvote_exponential = var_list[8]
        self.update_check_timing = var_list[9]

        print(var_list)

    def check_posts(self):
        #[postid, author, [vote weight for, vote weight against, plagiarism notice weight],
        #  [advertisement token temporary, advertisement token permanent],
        # [review tokens used, reviews],
        # list of people who submitted the post (in order, 0 was the first),
        # [upvote token temporary, upvote token permanent]

        post_list = mysqlhelper.get_posts(self.bot_number)
        # Iterates through each post
        for i in post_list:

            vote_total = i[2][1]+i[2][0]+i[2][2]


            #Checks if the percentage (between 0 and 1) of upvotes is bigger than the upvote threshold

            vote_percentage = (i[2][0]/float(vote_total))


            if vote_percentage >= self.upvote_threashold:

                # This next one checks if more than a set amount of votes say the post has been plagiarism (as a percentage)
                if i[2][2] < self.plagiarism_threshold or i[2][2] == 0:
                    vote_weight = self.vote_weight(vote_percentage, i[6][0], i[6][1])
                    self.vote(i[0], vote_weight[0], i[1])
                    mysqlhelper.vote_information([vote_weight[1], i[0], vote_percentage, i])
                else:
                    mysqlhelper.post_plag_flag([vote_weight[1], i[0], vote_percentage, i])


    def vote_weight(self, upvote_percent, upvote_tokens_temp, upvote_tokens_perm):
        voting_power = mysqlhelper.get_voting_power(self.bot_number)
        averages = mysqlhelper.get_averages(self.time_period, self.bot_number)
        # Each of the two types of tokens are taken into account. Their affect is calculated based on the outside varaibles
        token_power =((self.token_multiplyer[3]* upvote_tokens_temp **self.token_exponent[3]))+\
                   ((self.token_multiplyer[0]* upvote_tokens_perm **self.token_exponent[0])) + 1

        # total posts and power used during that time, for base votes (not tokens). -
        # is total percent that should be used during the time period divided by the amount of posts during the period

        # upvote percent on this post devided by the average upvote percent and controlled by our exponential
        # if below threshold it is dev by 1, if below threshold it is the square root of 1 + by how many times the threshold is bigger
        base_upvote = (averages[3]/(averages[1]+1))*\
                      (upvote_percent/(averages[0]+1))** self.upvote_exponential \
                      / math.sqrt(math.floor(self.voting_power_threshold/voting_power + 1)) * (1-(averages[2]))

        print(base_upvote)
        print(averages[3]/averages[1])
        full_vote = base_upvote * token_power
        if full_vote > 100:
            full_vote = 100

        percent_token = token_power / (base_upvote + token_power)


        return full_vote, percent_token



    def vote(self, post_id, weight, author):

        # This function tries to vote on a post with all nodes until it gets one that works
        # After the vote it will sleep for 6 seconds, and then check to see if it voted on the post
        # If the bot did not vote on the post, it will try again by calling the function again.

        # goes through a list of nodes and first tries the socket create connection.
        # If that works it tries to vote with the keys of our main delagated account.
        # If that works it stops the loop and goes on
        # If it does not it uses node_down(node) to alert us that a node is down and how many are left and tries again with the next
        if len(self.nodes) == 0:
            self.nodes = self.broken_nodes


        for i in range(len(self.nodes)):
           # try:
                #search_id = post_id.split("/", 4)

            # Tries to make a connection to the steem node and make a vote with the predefined weight and post id.
           # If it does not work either the node is down or the key does not work. It automatically treats it as if the node is down.
            voted = False
            try:
                node_connection = create_connection(self.nodes[i])
                s=Steem(node=node_connection, keys=self.posting_key)
                s.vote(post_id, weight, account=self.account_name)
                node_connection = None
                voted = True
                break
            except Exception as e:
                print(e)
                mysqlhelper.log_error(self.bot_number, "node "+ str(self.nodes[i])+ " is down")

                print("node: ", self.nodes[i]," did not work")
                self.node_down(i)

        has_voted = False
        if voted:
            try:
                time.sleep(6)
                votes = s.get_active_votes(author, post_id)

                for i in votes:
                    if self.account_name == i["voter"]:
                        has_voted = True
                        break
            except Exception as e:
                print(e)
                mysqlhelper.log_error(self.bot_number, e)

            if not has_voted:
                self.vote(post_id, weight, author)
                print("Failed to vote on  ", post_id,"  ", author)
        # This checks the post and sees if we are one of the voters. If we are not it tries to vote again



    def node_down(self,node):
        # This function alerts us that a node is down and how many are down
        #  through our accounts on the website
        mysqlhelper.log_error(self.bot_number, self.nodes[node])
        self.broken_nodes.append(self.nodes.pop(node))








main = Main(0)


main.check_posts()