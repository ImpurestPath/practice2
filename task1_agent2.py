import time
from datetime import datetime

from smart_m3.m3_kp_api import *


class KP_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        # in case if you want to react on added/removed data - just use self.kp.your_function(....) here
        print('Agent_X reporting: {}'.format(datetime.now()))
        print('    added', added)
        print('    removed', removed)

        for data in added:
            print(data)
            if int(str(data[2])) % 2 == 0:
                print("Removing odd number")
                kp.load_rdf_remove(data)
                break


if __name__ == '__main__':
    kp = m3_kp_api(PrintDebug=False, IP="65.21.7.142")
    handler = KP_Handler(kp)
    rdf_subs_triple = Triple(URI('Agent_X'), URI('has_temperature'), None)
    rdf_subscription = kp.load_subscribe_RDF(rdf_subs_triple, handler)
    try:
        while True:
            print("Waiting for updates")
            time.sleep(1)
    except:
        print("Quitting")
    finally:
        kp.load_unsubscribe(rdf_subscription)
        kp.leave()
