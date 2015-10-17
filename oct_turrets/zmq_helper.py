import time
import zmq
class ZmqHelper():

    
    def __init__(self, hq_address, hq_pub_port, hq_rc_port):
    self.hq_address = hq_address
    self.hq_pub_port = hq_pub_port
    self.hq_rc_port = hq_rc_port

    def producer(self, message):
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PUSH)
        zmq_socket.bind("tcp://"+self.hq_address":"+self.hq_rc_port)
        #start your result manager and workers before you start your producers
        work_message = {'message': message, 'time': time()}
        zmq_socket.send_json(work_message)