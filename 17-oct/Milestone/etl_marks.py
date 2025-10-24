# etl_marks.py
import pandas as pd
import logging
import time
from logger_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def process_marks(input_csv, output_csv='student_results.csv'):
    logger.info(f"ETL started for file: {input_csv}")
    start_time = time.time()
    try:
        df = pd.read_csv(input_csv)
        df['TotalMarks'] = df[['Maths', 'Python', 'ML']].sum(axis=1)
        df['Percentage'] = df['TotalMarks'] / 3
        df['Result'] = df['Percentage'].apply(lambda x: 'Pass' if x >= 50 else 'Fail')
        df.to_csv(output_csv, index=False)
        duration = time.time() - start_time
        logger.info(f"ETL completed for {input_csv} in {duration:.2f} seconds. Output saved to {output_csv}")
    except Exception as e:
        logger.error(f"ETL failed for {input_csv} with error: {e}")
        raise
