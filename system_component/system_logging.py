import logging,sys
# Define logger
logger = logging.getLogger()
# Define formatter
stdout_log_formatter = logging.Formatter(
    ' %(asctime)s | %(filename)s:%(lineno)s | %(levelname)s | %(message)s'
)
# Define handler
stdout_log_handler = logging.StreamHandler(stream=sys.stdout)
stdout_log_handler.setLevel(logging.INFO)
stdout_log_handler.setFormatter(stdout_log_formatter)
logger.addHandler(stdout_log_handler)
# Set level
logger.setLevel(logging.INFO)

class Logger():
    @staticmethod
    def info(message: str):
        assert message, "Message cant be None"
        logger.info(message)

    @staticmethod
    def warning(message: str):
        assert message, "Message cant be None"
        logger.warning(message)

    @staticmethod
    def exception(message: str):
        assert message, "Message cant be None"
        logger.exception(message)