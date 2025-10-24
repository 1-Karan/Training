from queue import Queue

csv_queue = Queue()

import threading
import time
from queue_manager import csv_queue
from producer import producer
from consumer import consumer

t_consumer = threading.Thread(target=consumer)
t_consumer.start()

time.sleep(1)

producer("marks.csv")
t_consumer.join()
