from operator import itemgetter
import random

def get_post(amount, random=False, time=True, post_list_length = 100, vote_time=600, randomness = 10):
    # Random gives a random list back if true, time gives the posts in the order they should be given out in
    # post_list_length controls how large the list of posts the function checks for at once
    # vote_time is how old the post will be the maxiumum age of the post, in blocks
    # randomness is for random = True and time = True, it will change posts on a % based on that number


    node_connection = create_connection(node)
    s = Steem(node=node_connection)
    block_thing = steem.blockchain.Blockchain(s)
    block = block_thing.get_current_block_num()
    node_connection.close()
    return_list_posts = []
    while True:
        try:
            posts = post_list(post_list_length)

            for i in posts:
                if i[2] + vote_time > block:
                    return_list_posts.append(i)
            if return_list_posts > amount or len(posts) == 0:
                break

        except:
            pass
    if time and random:
        new_list = sorted(return_list_posts, key=itemgetter(2))
        for i in range(len(new_list)):
            if randomness > random.randrange(100):
                new_pos = random.randrange(len(new_list))
                old_el = new_list[new_pos]
                new_list[new_pos] = new_list[i]
                new_list[i] = old_el
        return new_list[0:amount+1]

    elif time:
        return sorted(return_list_posts, key=itemgetter(2))[0:(amount+1)]

    elif random:
        return shuffle(return_list_posts)[0:(amount+1)]










def post_list(amount):
    # Post list returns a list of lists that are of length 3
    # for i in return_list, i[0] is author, i[1] is perm_link, i[2] is block the post was made
    pass