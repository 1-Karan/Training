import yaml
import logging

# 0. Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_config(filename: str):
    """Load the YAML config file and return the data."""
    try:
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)
        logging.info("Config loaded successfully: %s", filename)
        return config
    except FileNotFoundError:
        logging.error("%s not found", filename)
        raise
    except Exception as e:
        logging.error("Failed to load config file %s: %s", filename, str(e))
        raise


def print_db_connection_string(config: dict):
    """Print the database connection string."""
    db_info = config.get('database', {})
    host = db_info.get('host')
    port = db_info.get('port')
    user = db_info.get('user')

    if host and port and user:
        connection_string = f"Connecting to {host}:{port} as {user}"
        print(connection_string)
        logging.info("Database connection string: %s", connection_string)
    else:
        logging.warning("Missing database info in config!")


def main():
    filename = "config.yaml"

    # Step 1: Load the config file
    try:
        config = load_config(filename)

        # Step 2: Print database connection string
        print_db_connection_string(config)

    except Exception as e:
        # If the config file is not found or error in loading, we catch and handle it
        print("An error occurred. Please check the logs.")
        logging.error("An error occurred: %s", str(e))


if __name__ == "__main__":
    main()
