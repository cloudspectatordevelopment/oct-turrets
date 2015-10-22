import argparse
import json
import tarfile
import os.path
from oct_turrets.turret import Turret
from oct_turrets.utils import is_valid_conf
# from zmq_helper import ZmqHelper


def start():

    parser = argparse.ArgumentParser(description='Give parameters for start a turret instance')
    parser.add_argument('--config_file', type=str, default='', help='path for config_file')
    parser.add_argument('--tar', type=str, default='', help='Path for the tarball')
    args = parser.parse_args()

    if args.config_file == '' and args.tar == '':
        # print("and args.tar = {}".format(args.tar))
        parser.error('You need a config_file.json to start a turret')

    if args.tar != '':
        tar_path = args.tar
        if tarfile.is_tarfile(tar_path):
            tar = tarfile.open(tar_path)
            files_in_tarfile = tar.getmember("config.json")
            if files_in_tarfile:
                # tar_json_path = tar.extract(files_in_tarfile, "/tmp/")
                if is_valid_conf(tar.extractfile("config.json").read()):
                    config_file = tar.extractfile("config.json").read()
    elif args.config_file != '' and is_valid_conf(args.config_file):
        config_file = args.config_file
    else:
        print("you need a valid config.json")
        exit(0)

    # if args.config_file != '':
    #     config_file = args.config_file
    turret = Turret(config_file)

    turret.start()

    # zmqhlp = ZmqHelper(hq_address, hq_pub_port, hq_rc_port)

    # zmqhlp.producer(res)
