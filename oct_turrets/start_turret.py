import argparse
from turret import Turret

parser = argparse.ArgumentParser(description='Give parameters for start a turret instance')
parser.add_argument('hq_address', type=str, help='Head Quater adresse')
parser.add_argument('--hq_pub_port', type=int, default=5555 ,help='Head Quater pub zmq socket port')
parser.add_argument('--hq_rc_port', type=int, default=5556, help='Head Quater result collector zmq socket port')
parser.add_argument('script_file', type=str, help='Path for script_file')
parser.add_argument('config_file', type=str, help='path for config_file')
args = parser.parse_args()
#print(args)

hq_address = args.hq_address
hq_pub_port = args.hq_pub_port
hq_rc_port = args.hq_rc_port

print "master adresse is: %s \n pub port is: %d \n result collector port is: %d \n" % (hq_address, hq_pub_port, hq_rc_port )

turret = Turret(args.hq_address, args.hq_pub_port, args.hq_rc_port, args.script_file, args.config_file)

res = turret.run()

print (run)

