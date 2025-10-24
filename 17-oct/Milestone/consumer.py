import logging

from etl_marks import process_marks
from logger_config import setup_logging
from queue_manager import csv_queue

setup_logging()
logger = logging.getLogger(__name__)

def consumer():
    logger.info("Consumer started and waiting for CSV file path...")
    while True:
        csv_file_path = csv_queue.get()
        logger.info(f"Received CSV file path from queue: {csv_file_path}")

        try:
            output_file = f"processed_{csv_file_path}"
            process_marks(csv_file_path, output_file)
            logger.info(f"Successfully processed {csv_file_path}")
        except Exception as e:
            logger.error(f"Error processing {csv_file_path}: {e}")
        finally:
            csv_queue.task_done()

if __name__ == '__main__':
    consumer()
