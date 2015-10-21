import time
import json

from base import BaseTurret
from canon import Canon


class Turret(BaseTurret):
    """This class represent the classic turret for oct
    """
    def start(self):
        """Start the turret and wait for the master to run the test
        """
        print("starting turret")
        while self.start_loop:
            msg = self.master_publisher.recv_string()
            print(msg)
            msg = json.loads(msg)

            if 'command' in msg and msg['command'] == 'start':
                print("Starting the test")
                self.start_time = time.time()
                self.start_loop = False
                data = self.build_status_message('running')
                self.result_collector.send_json(data)
                self.run()
            elif 'command' in msg and msg['command'] == 'status_request' and not self.already_responded:
                print("responding to master")
                data = self.build_status_message('ready')
                self.result_collector.send_json(data)
                self.already_responded = True

    def run(self):
        """The main run method
        """
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
            if len(self.canons) <= self.config['canons'] and time.time() - last_insert >= rampup:
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
                if 'command' in data and data['command'] == 'stop':
                    print("Exiting loop, premature stop")
                    self.run_loop = False
                    break
            if self.local_result in socks:
                results = self.local_result.recv_json()
                results['turret_name'] = self.config['name']
                self.result_collector.send_json(results)

        for i in self.canons:
            i.join()

        data = self.build_status_message('ready')
        self.result_collector.send_json(data)
        self.start_loop = True
        self.already_responded = False
        self.start()
