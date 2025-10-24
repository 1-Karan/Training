import csv
import logging

# 0. Configure logging
logging.basicConfig(
    filename='sales.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def read_csv(filename: str):
    """Read the CSV file and return data."""
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        logging.info("CSV file loaded successfully: %s", filename)
        return data
    except FileNotFoundError:
        logging.error("File %s not found", filename)
        raise
    except Exception as e:
        logging.error("Error reading the file %s: %s", filename, str(e))
        raise


def compute_sales(data: list):
    """Compute total sales for each product and log the results."""
    for row in data:
        try:
            product = row['product']
            price = float(row['price'])
            quantity = int(row['quantity'])
            total_sales = price * quantity
            print(f"{product} total = {total_sales}")
            logging.info("%s total sales = %s", product, total_sales)
        except ValueError:
            logging.error("Invalid numeric value for price or quantity in row: %s", row)
        except KeyError:
            logging.error("Missing required column in row: %s", row)


def main():
    filename = "sales.csv"

    # Step 1: Read the CSV file
    try:
        data = read_csv(filename)

        # Step 2: Compute sales for each item
        compute_sales(data)

    except Exception as e:
        print("An error occurred. Please check the logs.")
        logging.error("An error occurred: %s", str(e))


if __name__ == "__main__":
    main()
