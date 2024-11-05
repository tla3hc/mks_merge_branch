import os
import logging
from datetime import datetime
from functools import wraps
from .. import config

# ANSI escape codes for colors
RESET = "\033[0m"
YELLOW = "\033[33m"
RED = "\033[31m"

def format_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_level = func.__name__.upper()
        
        # Determine color based on log level
        if log_level == 'WARNING':
            color = YELLOW
        elif log_level == 'ERROR':
            color = RED
        else:
            color = ""
        
        args = (f"{current_time}: {color}{args[0]:^30} : {args[1]}{RESET}",) + args[2:]
        return func(*args, **kwargs)
    return wrapper

logging.info = format_log(logging.info)
logging.warning = format_log(logging.warning)
logging.error = format_log(logging.error)
logging.debug = format_log(logging.debug)

 
class Logger:
   
    m_class_name = "Logger"
    m_log_folder = config.LOG_FOLDER_NAME
   
    def __init__(self):
        today = datetime.today().strftime('%Y_%m_%d')
        FORMAT = '%(message)s'
        # Check and create log folder
        if not os.path.isdir(self.m_log_folder):
            os.makedirs(self.m_log_folder)
 
        logging.basicConfig(filename=f'{self.m_log_folder}/{today}.log', encoding='utf-8', level=logging.DEBUG, force=True, format=FORMAT)
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.info("Logger", 'Init')
 
    def info(self, data):
        logging.info("Logger", data)
       
    def warning(self, data):
        logging.warning("Logger", data)
       
    def error(self, data):
        logging.error("Logger", data)
    
    def debug(self, data):
        logging.debug("Logger", data)