from __future__ import unicode_literals

import six
import zmq
import json
import uuid
import os.path
from threading import Thread

from oct_turrets.utils import load_file


class BaseTurret(object):
    """The base turret class

    :param hq_address str: the ip address of the HQ runing OCT
    :param hq_pub_port int: the port of the publish socket in the HQ
    :param hq_rc_port int: the port of the result collector in the HQ
    """
    def __init__(self, config_file):

        if os.path.isfile(config_file):
            with open(config_file) as f:
                self.config = json.load(f)
        else:
            self.config = json.loads(config_file)

        self.canons = []
        self.script_module = load_file(self.config['script'])
        self.start_time = None
        self.run_loop = True
        self.start_loop = True
        self.already_responded = False
        self.uuid = six.text_type(uuid.uuid4())
        self.commands = {}
        self.status = "Initialized"

        context = zmq.Context()

        self.poller = zmq.Poller()
        self.local_result = context.socket(zmq.PULL)
        self.local_result.bind("ipc://turret-{}".format(self.uuid))

        self.master_publisher = context.socket(zmq.SUB)
        self.master_publisher.connect("tcp://{}:{}".format(self.config['hq_address'], self.config['hq_publisher']))
        self.master_publisher.setsockopt_string(zmq.SUBSCRIBE, '')
        self.master_publisher.setsockopt_string(zmq.SUBSCRIBE, self.uuid)

        self.result_collector = context.socket(zmq.PUSH)
        self.result_collector.connect("tcp://{}:{}".format(self.config['hq_address'], self.config['hq_rc']))

        self.poller.register(self.local_result, zmq.POLLIN)
        self.poller.register(self.master_publisher, zmq.POLLIN)

        self.init_commands()

    def init_commands(self):
        """Initialize the commands dictionnary. This dict will be used when master send a command to interpret them
        """
        pass

    def build_status_message(self):
        data = {
            'turret': self.config['name'],
            'status': self.status,
            'uuid': self.uuid,
            'rampup': self.config['rampup'],
            'script': self.config['script'],
            'canons': self.config['canons']
        }
        return data

    def exec_command(self, payload):
        """Execute the given command by searching it in the self.commands property.

        :param payload str: the dict containing the message from the master
        :return: True if the command exists, false if the payload does not contain a command or the command is not found
        :rtype: bool
        """
        if 'command' in payload:
            command = self.commands.get(payload['command'])
            if command is None:
                print("command not found")
                return False
            else:
                command(payload['msg'])
            return True
        print("The message does not contain a command")
        return False

    def start(self):
        """Start the turret and wait for the master to call the run method
        """
        raise NotImplementedError("Start method must be implemented")

    def send_result(self, result):
        """Send result to the result collector

        :param result dict: the result to send to the master
        :return: None
        """
        raise NotImplementedError("send_result error must be implemented")

    def run(self):
        """Main loop for the turret
        """
        raise NotImplementedError("run method must be implemented")


class BaseCanon(Thread):
    """The base canon class, inherit from thread

    :param start_time int: the start_time of the test
    :param run_time int: the total run time for the script in second
    :param script_module: the module containing the test
    """

    def __init__(self, start_time, script_module, turret_uuid):
        super(BaseCanon, self).__init__()
        self.start_time = start_time
        self.script_module = script_module
        self.run_loop = True

        context = zmq.Context()
        self.result_socket = context.socket(zmq.PUSH)
        self.result_socket.connect("ipc://turret-{}".format(turret_uuid))

    def run(self):
        """The main run method for the canon
        """
        raise NotImplementedError("run method must be implemented")


class BaseTransaction(object):
    """The base transaction class for writing tests
    """

    def __init__(self):
        pass

    def setup(self):
        """This method will be call before the run method, use it to setup all needed datas.
        The setup time will not be included in the scriptrun_time
        """
        pass

    def run(self):
        """This is the main function that will be executed for the tests
        """
        pass

    def tear_down(self):
        """This method will be call once the run method has ended. Since the transaction instance will never be
        destroyed before the end of the test, use this method to clean and reset all variables, etc.
        The tear down time will not be included in the scriptrun_time
        """
        pass
