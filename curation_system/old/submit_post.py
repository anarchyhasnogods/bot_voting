from websocket import create_connection
from steem import Steem
import steem
import time


def submit_post(post_link, submission_user, curation_reward, time,node="wss://steemd-int.steemit.com"):
    # post link is a list of two strings, the username and then the permlink

    author_is_submittor = post_link[0] == submission_user
    post_time = get_post_time(post_link, node)
    print(time)
    
    if author_is_submittor:
        curation_reward = 0
    if time/2 > post_time:
        return False
    # send post submission memo
    index = make_memo(post_link, submission_user, curation_reward)



    return index, curation_reward





def make_memo(thing ="",o="",f=0,c=0,s=0,d=0):
    # Just so it doesn't error, we will put in the needed functions for each step later
    pass




def get_post_time(post_id,node):
    node_connection = create_connection(node)
    s = Steem(node=node_connection)
    block_thing = steem.blockchain.Blockchain(s)
    size = s.get_account_history(post_id[0], -1, 0)[0][0]

    history_list = s.get_account_history(post_id[0], size,size-1)
    memos = []
    for i in history_list:

        for ii in i:

            if type(ii) == dict:

                try:
                    if ii['op'][0] == 'comment' and ii['op'][1]['title'] == post_id[1]:
                        memos.append(ii['block'])
                        #print("append")



                except:

                    pass
    block = block_thing.get_current_block_num()


    node_connection.close()
    try:

        memos = sorted(memos)

        return block-memos[0]

    except:
        return False



submit_post(["theironfelix","Dialectics, what is it?"],"anarchyhasnogods",1000)
