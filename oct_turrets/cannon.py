import time

from oct_turrets.base import BaseCannon


class Cannon(BaseCannon):

    def run(self):
        """The main run method of the canon
        """
        elapsed = 0
        trans = self.script_module.Transaction(self.config,
                                               self.transaction_context)
        max_oper = self.config.get('max_oper', 0)
        oper_count = 0
        oper_success_count = 0
        oper_failed_count = 0
        trans.custom_timers = {}

        while self.run_loop:
            if max_oper and max_oper == oper_count:
                break
            error = ''

            trans.setup()
            start = time.time()
            try:
                trans.run()
                oper_success_count += 1
            except Exception as e:
                oper_failed_count += 1
                error = str(e)
            oper_count += 1
            scriptrun_time = time.time() - start
            trans.tear_down()

            elapsed = time.time() - self.start_time

            epoch = time.mktime(time.localtime())

            data = {
                'elapsed': elapsed,
                'epoch': epoch,
                'scriptrun_time': scriptrun_time,
                'error': error,
                'custom_timers': trans.custom_timers
            }
            self.result_socket.send_json(data)
        self.local_queue.put({'status': 'finished'})
