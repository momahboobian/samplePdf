import logging
import os
import sys


def setup_logger(log_level=logging.INFO):
    """Sets up the logging configuration."""

    # Ensure 'logs' directory exists
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'app.log')

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
