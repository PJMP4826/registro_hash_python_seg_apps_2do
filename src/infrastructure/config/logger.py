import logging
import colorlog
from pathlib import Path

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# ruta relativa a la raiz del proyecto
BASE_DIR = Path(__file__).resolve().parents[3]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# FILE HANDLER
file_handler = logging.FileHandler(
    filename=LOG_DIR / "app.log",
    mode="a",
    encoding="utf-8"
)

file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

file_handler.setFormatter(file_formatter)

# COLORED CONSOLE HANDLER
console_handler = colorlog.StreamHandler()

console_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s | %(filename)s:%(lineno)d | %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# logger.debug("Debug message")
# logger.info("Info message")
# logger.warning("Warning message")
# logger.error("Error message")
# logger.critical("Fatal message")
# logger.info(f"LOG_DIR: {LOG_DIR}")
