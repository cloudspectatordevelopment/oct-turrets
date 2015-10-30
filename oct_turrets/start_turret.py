import os
import logging
import argparse
import tarfile
from oct_turrets.turret import Turret
from oct_turrets.utils import is_valid_conf

log = logging.getLogger(__name__)


def start():

    parser = argparse.ArgumentParser(description='Give parameters for start a turret instance')
    parser.add_argument('--config-file', type=str, default='', help='path for config_file')
    parser.add_argument('--tar', type=str, default='', help='Path for the tarball')
    args = parser.parse_args()

    if args.config_file == '' and args.tar == '':
        parser.error('You need a config_file.json to start a turret')

    if args.tar != '':
        tar_path = args.tar
        if tarfile.is_tarfile(tar_path):
            tar = tarfile.open(tar_path)
            files_in_tarfile = tar.getmember("config.json")
            if files_in_tarfile:
                if is_valid_conf(tar.extractfile("config.json").read(), tar):
                    config_file = tar.extractfile("config.json").read()
    elif args.config_file != '' and os.path.isfile(args.config_file):
        config_file = args.config_file
    else:
        log.error("you need a valid config.json")
        exit(0)

    turret = Turret(config_file)
    turret.start()
