from websocket import create_connection
from steem import Steem
import steem
import time

class Main:
    def __init__(self, max_post, max_time, port_list):
        self.max_post = max_post
        self.max_time = max_time
        self.port_list = port_list
        self.set_list = []

    def create_set(self):
        # This will create a new process of python that will manage the introduction of posts
        p = Process(target=vote_set,
                    args=(account_list, follow_weight, o, active_nodes[int(random.randrange(len(active_nodes)) / 2)]))
        p.start()


    def set_loop(self, max_posts, max_time, sending_account, key, memo):

        pass