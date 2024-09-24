import logging

def setup_logging(log_file: str):
    """Set up logging configuration."""
    with open(log_file, 'w'):  # Clear the file before logging for each run to easier error search
        pass    # clear log file on each run
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )