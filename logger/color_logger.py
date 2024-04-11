import logging

class ColoresTerminal:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ColorLogHandler(logging.StreamHandler):
    def emit(self, record):
        levelno = record.levelno
        if(levelno >= 50):
            color = ColoresTerminal.FAIL + ColoresTerminal.BOLD + ColoresTerminal.UNDERLINE
        elif(levelno >= 40):
            color = ColoresTerminal.FAIL
        elif(levelno >= 30):
            color = ColoresTerminal.WARNING
        elif(levelno >= 20):
            color = ColoresTerminal.OKGREEN
        elif(levelno >= 10):
            color = ColoresTerminal.OKCYAN
        else:
            color = ColoresTerminal.ENDC
        record.msg = color + record.msg + ColoresTerminal.ENDC
        super(ColorLogHandler, self).emit(record)

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Ajusta según sea necesario
    handler = ColorLogHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    if not logger.handlers:  # Evita agregar múltiples veces el mismo handler
        logger.addHandler(handler)

