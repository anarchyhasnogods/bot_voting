

def get_posts(bot_number):
    print("getting posts")

    return [["https://steemit.com/science/@anarchyhasnogods/the-impact-of-melting-glaciers#@anarchyhasnogods/re-anarchyhasnogods-the-impact-of-melting-glaciers-20171002t222800349z"

        , "anarchyhasnogods", [100, 50, 0], [0, 0], [0, 0], ["anarchyhasnogods", "othername"],
            [10, 10]]]


def get_keys(bot_number):


    return ["space-pictures","5KhPasPoKWvw3yt5uSnbyLoQYkH91oHz8nkVh3JGGRorkknS4Mz"]

def get_averages(time_period, bot_number):
    # Average upvote percent (through our platform)
    # Total posts during the period of time
    # What percent of total power went towards upvote tokens. Is a decimal.
    # What amount of power should have been used total during that time. Expressed as percent of one upvotes -
    # 1000 is 10 full votes, which would be 24 hours.
    return [80, 10, 0.0005, 1000]
    pass

def get_vars(bot_number):


    return [0, .50 , [1,1,1,1,1], [100,100,100], [1,1,1,1,1], ['node'], 6, 80, 1, 600]

def get_voting_power_used(time_period, bot_numbr):

    return None


def get_voting_power(bot_number):
    # Expressed as a percent out of 100
    return 100
    pass


def check_update(bot_number):
    return [1]


def node_down(node, bot_number):
    pass



def vote_information(post_input):

    # This takes information on votes and puts it into the mysql database in a format that it can retrive later for other functions


    pass
def post_plag_flag(post_input):
    pass