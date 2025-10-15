"""
Logging setup for the pipeline
"""

import logging
from datetime import datetime
import os

def setup_logger():
    """setup logger that writes to both console and file"""

    #create logs directory if it doesnt exist
    os.makedirs('logs',exist_ok=True)

    #create logger
    logger=logging.getLogger('weather pipeline')
    logger.setLevel(logging.INFO)

    #avoid duplicate handlers
    if logger.handlers:
        return logger
    
    #console handler(colored output)
    console_handler=logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format=logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)

    #file handler (detailed logs)
    log_filename=f"log/pipeline_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_format=logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    #add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger



