import logging
from queue_manager import csv_queue
from logger_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def producer(csv_file_path):
    logger.info(f"Putting file path in queue: {csv_file_path}")
    csv_queue.put(csv_file_path)
    logger.info("File path pushed to queue")

if __name__ == '__main__':
    producer("marks.csv")
