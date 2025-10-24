import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(
    filename='etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def run_etl(input_file='marks.csv'):
    try:
        df = pd.read_csv(input_file)
        df['TotalMarks'] = df[['Maths', 'Python', 'ML']].sum(axis=1)
        df['Percentage'] = df['TotalMarks'] / 3
        df['Result'] = df['Percentage'].apply(lambda x: 'Pass' if x >= 50 else 'Fail')

        today = datetime.now().strftime('%Y%m%d')
        output_file = f'daily_report_{today}.csv'
        df.to_csv(output_file, index=False)

        logging.info(f"ETL completed successfully. Output saved to {output_file}")
        print(f"ETL completed successfully. Output saved to {output_file}")
    except Exception as e:
        logging.error(f"ETL failed: {e}")
        print(f"ETL failed: {e}")


if __name__ == '__main__':
    run_etl()
