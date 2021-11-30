import random
import time
from datetime import datetime

from smart_m3.m3_kp_api import *


class KP_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        for data in added:
            if str(data[1]) == "has_state":
                if str(data[2]) == "I wanna play":
                    kp.load_query_rdf(Triple(data[0], URI('is playing'), None))
                    if len(kp.result_rdf_query) == 0:
                        print("Starting new game with " + str(data[0]))
                        kp.load_rdf_insert(Triple(data[0], URI('is playing'), Literal(random.randint(0, 100))))
                    kp.load_rdf_insert(Triple(data[0], URI("has_game_result"), URI("Fail")))
            elif str(data[1]) == "says_number":
                kp.load_query_rdf(Triple(data[0], URI('is playing'), None))
                print(str(data[0]) + " suggests " + str(data[2]) + ". Right number is " + str(kp.result_rdf_query[0][2]))
                if len(kp.result_rdf_query) == 1:
                    if str(kp.result_rdf_query[0][2]) == str(data[2]):
                        kp.load_rdf_remove(Triple(data[0], URI("has_game_result"), URI("Fail")))
                        kp.load_rdf_insert(Triple(data[0], URI("has_game_result"), URI("Success")))
                        kp.load_rdf_remove(kp.result_rdf_query[0])
                    else:
                        kp.load_rdf_remove(Triple(data[0], URI("has_game_result"), URI("Fail")))
                        kp.load_rdf_insert(Triple(data[0], URI("has_game_result"), URI("Fail")))
                else:
                    kp.load_rdf_insert(Triple(data[0], URI("has_game_result"), URI("Not started")))


if __name__ == '__main__':
    kp = m3_kp_api()
    handler = KP_Handler(kp)
    rdf_subs_triples = [Triple(None, URI('has_state'), None), Triple(None, URI('says_number'), None)]
    rdf_subscription = kp.load_subscribe_RDF(rdf_subs_triples, handler)
    try:
        while True:
            # print("Waiting for updates")
            # time.sleep(1)
            pass
    except KeyboardInterrupt:
        print("Quitting")
    finally:
        kp.load_unsubscribe(rdf_subscription)
        kp.clean_sib()  # remove all data from Smart Space
        kp.leave()
    exit(0)
