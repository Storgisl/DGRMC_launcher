import os
import logging


class LoggerFactory:
    def __init__(self, name, log_file=None, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        # Always create the formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        if not self.logger.hasHandlers():  # Prevents duplicate handlers
            if log_file:
                log_dir = "logs"
                os.makedirs(log_dir, exist_ok=True)
                log_path = os.path.join(log_dir, log_file)

                # File handler
                file_handler = logging.FileHandler(log_path)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            else:
                # Console handler if no log file is specified
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
