# -*- coding:utf-8 -*-
import os
import logging
import logging.config
from baosteel100.libs.options import config

def get_logger(type):
    log_path = config.path.log
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    try:
        logging.config.fileConfig(os.path.join(config.root_path,"logging.config"))
        logger = logging.getLogger(type)
        return logger
    except Exception as e:
        print (e)
        print ("get logger error")

