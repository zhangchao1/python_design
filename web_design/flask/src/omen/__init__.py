import logging
logger = logging.getLogger('omen')
handler = logging.FileHandler('logs.log', mode = "a")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
def wirte_log_to_file(str):
    logger.info(str)
    handler.flush()
    handler.close()