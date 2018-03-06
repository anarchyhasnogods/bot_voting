from websocket import create_connection
from steem import Steem
import steem
import time
from multiprocessing import Process
import post_holder
import os
import threading
class Main:
    def __init__(self, max_post, max_time, port_list):
        self.max_post = max_post
        self.max_time = max_time
        self.port_list = port_list
        self.set_list = []

    def create_set(self):
        # This will create a new process of python that will manage the introduction of posts within a group
        # group is based on catagory and time

        p = Process(target=set_loop,
                    args=(account_list, follow_weight, o, active_nodes[int(random.randrange(len(active_nodes)) / 2)]))
        p.start()


    def set_loop(self, max_posts, max_time, sending_account, key, max_voting_time, communication_threads):

        lock = threading.Lock()
        lock_flag = threading.Lock()
        flag = "NONE"
        # This tells them what step they should be on
        #NONE = still starting up/done voting, #Post_Collection = getting posts, #Post_Voting = letting people vote on posts
        communication_list = []
        # [type (str name), data]
        # [data (post add)] = [post_link, submission_author, post_author]
        # [data (vote add)] = [vote, post_link]
        # [vote] = [voter, vote] (vote = -1, 0, 1)

        post_holder.Post_holder(max_posts, max_time, sending_account, key)

        start_time = time.time()

        thread_list = []

        for i in range(communication_threads):
            thread_list.append(Communication(lock, lock_flag, flag, communication_list))
        for i in thread_list:
            i.start()

        with lock_flag:
            flag = "Post_Collection"

        while True:

            if post_holder.votes_finished:

                break
            elif len(post_holder.post_list) >= post_holder.max_posts or time.time() - start_time > post_holder.max_time:
                with lock_flag:
                    flag = "Post_Voting"
                start_time = time.time()
            elif time.time() - start_time > max_voting_time:
                with lock_flag:
                    flag = "NONE"
                post_holder.finish_post_set()
            with lock:
                for i in communication_list:
                    if i[0] == "VOTE":
                        post_holder.add_post(i[1][0], i[1][1], i[1][2])
                    elif i[0] == "POST_SUBMIT":
                        post_holder.add_vote(i[1][0], i[1][1])









class Communication(threading.Thread):
    def __init__(self, lock, lock_flag, flag, communication_list):
        self.lock = lock
        self.lock_flag = lock_flag
        self.flag = flag
        self.communication_list = communication_list
        threading.Thread.__init__()

    def start_voting(self):
        pass
    
    def votes_over(self):

        pass

    def run(self):
        for i in range(10):
            time.sleep(5)
            with self.lock:
                print("locking, communication")
                self.communication_list.append(["link" + str(i),"submission_user", "post_author"])
        pass
print("here")

thing = Main(100,100,100)
