# This file is for setting up the main bot object and controlling the specifics of the actions and numbers

import main
import time
import mysqlhelper
def start():
    main_1 = main.Main(0)

    main_objects = []
    main_objects.append(main_1)
    while True:


        for i in range(len(main_objects)):
            bot_number = run_bot(main_objects[i])
            print(bot_number)
            if type(bot_number) == list:


                if bot_number[0] == 1:
                    main_objects[bot_number[1]] = main.Main(bot_number[1])

                elif bot_number[0] == 2:
                    main_objects.insert(main.Main(bot_number[1]), bot_number[1])
                    for i in range(len(main_objects)):

                        main_objects[i].bot_number = i

                elif bot_number[0] == 3:
                    main_objects.pop(bot_number[1])
                    for i in range(len(main_objects)):
                        main_objects[i].bot_number = i


        time.sleep(10)



def run_bot(main_object):
    try:
        update_codes = main_object.check_update()  # checks for possible actions
        print(update_codes, "coeds")
        for i in update_codes:
            if type(i) == list():
                return i

            else:
                try:

                    if i == 1:  # vote

                        main_object.check_posts()

                    if i == 2:  # update variables


                        main_object.check_vars()

                    if i == 3:  # Restart bot
                        return [1, main_object.bot_number]
                except Exception as e:
                    mysqlhelper.log_error(main_object.bot_number, e)



    except Exception as e:

        print(e, "run function")
        mysqlhelper.log_error(main_object.bot_number, e)

    return -1









start()

