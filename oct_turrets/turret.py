import time
import json

from oct_turrets.base import BaseTurret
from oct_turrets.canon import Canon


class Turret(BaseTurret):
    """This class represent the classic turret for oct
    """

    def init_commands(self):
        """Initialize the basics commandes for the turret
        """
        self.commands['start'] = self.run
        self.commands['status_request'] = self.send_status

    def send_status(self, msg=None):
        """Reply to the master by sending the current status
        """
        if not self.already_responded:
            print("responding to master")
            reply = self.build_status_message()
            self.result_collector.send_json(reply)
            self.already_responded = True

    def start(self):
        """Start the turret and wait for the master to run the test
        """
        print("starting turret")
        self.status = "Ready"
        while self.start_loop:
            payload = self.master_publisher.recv_string()
            payload = json.loads(payload)
            self.exec_command(payload)

    def run(self, msg=None):
        """The main run method
        """
        print("Starting tests")

        self.start_time = time.time()
        self.start_loop = False
        self.status = 'running'
        self.send_status()

        if 'rampup' in self.config:
            rampup = float(self.config['rampup']) / float(self.config['canons'])
        else:
            rampup = 0

        last_insert = 0
        print(rampup)

        if rampup > 0 and rampup < 1:
            timeout = rampup * 1000
        else:
            timeout = 1000

        while self.run_loop:
            if len(self.canons) < self.config['canons'] and time.time() - last_insert >= rampup:
                canon = Canon(self.start_time, self.config['run_time'], self.script_module, self.uuid)
                canon.daemon = True
                self.canons.append(canon)
                canon.start()
                last_insert = time.time()
                print(len(self.canons))

            socks = dict(self.poller.poll(timeout))
            if self.master_publisher in socks:
                data = self.master_publisher.recv_string()
                data = json.loads(data)
                if 'command' in data and data['command'] == 'stop':  # not managed, must break the loop
                    print("Exiting loop, premature stop")
                    self.run_loop = False
                    break
            if self.local_result in socks:
                results = self.local_result.recv_json()
                results['turret_name'] = self.config['name']
                self.result_collector.send_json(results)

        for i in self.canons:
            i.join()

        self.local_result.close()
        # data = self.build_status_message()
        # self.result_collector.send_json(data)
        # self.start_loop = True
        # self.already_responded = False
