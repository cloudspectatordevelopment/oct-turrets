import argparse
import json
from turret import Turret
from path import path
# from zmq_helper import ZmqHelper

parser = argparse.ArgumentParser(description='Give parameters for start a turret instance')
parser.add_argument('config_file', type=str, help='path for config_file')
args = parser.parse_args()

conf_file = path(args.config_file).text()

json_parsed = json.loads(conf_file)

# print (json_parsed['name'])



# print "master adresse is: %s \n pub port is: %d \n result collector port is: %d \n" % (hq_address, hq_pub_port, hq_rc_port )

turret = Turret(args.config_file)

res = turret.start()

# zmqhlp = ZmqHelper(hq_address, hq_pub_port, hq_rc_port)

# zmqhlp.producer(res)

