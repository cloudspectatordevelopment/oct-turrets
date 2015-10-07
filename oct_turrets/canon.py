import time

from base import BaseCanon


class Canon(BaseCanon):

    def run(self):
        """The main run method of the canon
        """
        elapsed = 0
        trans = self.script_module.Transaction()
        trans.custom_timers = {}

        while elapsed < self.run_time:
            error = ''
            start = time.time()

            trans.setup()
            try:
                trans.run()
            except Exception as e:
                error = str(e)
            trans.tear_down()

            scriptrun_time = time.time() - start
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
