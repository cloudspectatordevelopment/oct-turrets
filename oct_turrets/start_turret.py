import argparse
import json
import tarfile
import path as path
from turret import Turret
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
                tar_json_path = tar.extract(files_in_tarfile, "/tmp/")
                if is_valid_conf("/tmp/config.json"):
                    config_file = "/tmp/config.json"
                print(tar_json_path)
    else:
        print("you need a valid config.json file in your tarball ")
        exit(0)

    if args.config_file != '':
        config_file = args.config_file

    turret = Turret(config_file)

    turret.start()

    # zmqhlp = ZmqHelper(hq_address, hq_pub_port, hq_rc_port)

    # zmqhlp.producer(res)


def is_valid_conf(config_file_path):
    with open(config_file_path, 'r') as content_file:
        conf_file = content_file.read()

    json_parsed = json.loads(conf_file)

    # if json_parsed['script']:
    #     return (1)

    print (json_parsed['script'])

    return (json_parsed['script'])
