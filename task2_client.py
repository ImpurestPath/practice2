import random
import time
from datetime import datetime

from smart_m3.m3_kp_api import *

def suggest_number(kp,id, number):
    print("You suggest " + str(number))
    kp.load_rdf_remove(Triple(URI(id), URI('says_number'), Literal(number)))
    kp.load_rdf_insert(Triple(URI(id), URI('says_number'), Literal(number)))

class KP_Handler:
    def __init__(self, kp=None, id=None):
        self.kp = kp
        self.id = id

    def handle(self, added, removed):
        print("Got: {}".format(added))
        for data in added:
            if str(data[2]) == "Not started":
                raise Exception("Something went wrong during start of the game")
            elif str(data[2]) == "Success":
                print("Congratulations! You won this game")
                exit(0)
            else:
                print("Suggest number")
                # number = int(input("Suggest number: "))
                number = random.randint(0, 100)
                suggest_number(self.kp, self.id, number)
                break


if __name__ == '__main__':
    my_id = str(datetime.now())
    kp = m3_kp_api()
    handler = KP_Handler(kp, my_id)
    rdf_subs_triples = [Triple(URI(my_id), URI("has_game_result"), None)]
    rdf_subscription = kp.load_subscribe_RDF(rdf_subs_triples, handler)
    kp.load_rdf_insert(Triple(URI(my_id), URI("has_state"), URI("I wanna play")))
    # suggest_number(kp, my_id, random.randint(0, 100))
    try:
        while True:
            # print("Waiting for updates")
            # time.sleep(1)
            pass
    except KeyboardInterrupt:
        print("Quitting")
    finally:
        kp.load_unsubscribe(rdf_subscription)
        kp.leave()
    exit(0)