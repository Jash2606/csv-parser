import zmq
import threading
import os
from dotenv import load_dotenv

load_dotenv()

local = threading.local()

def get_push_socket():
    """
    Get a thread-local PUSH socket for sending tasks
    """
    if not hasattr(local, 'zmq_context'):
        local.zmq_context = zmq.Context()
    
    if not hasattr(local, 'push_socket'):
        local.push_socket = local.zmq_context.socket(zmq.PUSH)
        local.push_socket.connect(f"tcp://{os.environ.get('ZMQ_HOST', '127.0.0.1')}:{os.environ.get('ZMQ_PORT', '5557')}")
    
    return local.push_socket

def get_pull_socket():
    """
    Get a PULL socket for receiving tasks (used by workers)
    """
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    # Use 127.0.0.1 instead of localhost
    socket.bind(f"tcp://127.0.0.1:{os.environ.get('ZMQ_PORT', '5557')}")
    return socket, context
