from base import BaseTurret
from canon import Canon


class Turret(BaseTurret):
    """This class represent the classic turret for oct
    """
    def run(self):
        """The main run method
        """
        if 'rampup' in self.config:
            timeout = float(self.config['rampup'] / self.config['canons'])
        else:
            timeout = 10
        while self.run_loop:
            if len(self.canons) <= self.config['canons']:
                canon = Canon(self.start_time, self.config['run_time'], self.script_module)
                canon.daemon = True
                self.canons.append(canon)
                canon.start()
            else:
                timeout = None
            socks = dict(self.poller.poll(timeout))
            if self.master_publisher in socks:
                print(self.master_publisher.recv_json())
            if self.local_result in socks:
                self.results_collector.send_json(self.local_result.recv_json())
        for i in self.canons:
            i.join()