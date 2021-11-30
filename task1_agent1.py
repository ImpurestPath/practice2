import random
import time

from smart_m3.m3_kp_api import *

def show_query(kp, query):
    kp.load_query_rdf(query)
    print('Query result: {}'.format(kp.result_rdf_query))


if __name__ == '__main__':
    # basic program, which connects to the smart space and clears it
    kp = m3_kp_api(PrintDebug=False, IP="65.21.7.142")
    try:
        while True:
            kp.load_rdf_insert(Triple(URI('Agent_X'), URI('has_temperature'), Literal(random.randint(-10, 20))))
            time.sleep(2)
    except KeyboardInterrupt:
        print("Quitting")
    kp.clean_sib()  # remove all data from Smart Space
    kp.leave()
