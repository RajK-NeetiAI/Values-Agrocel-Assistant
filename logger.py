import logging
import sys

format = "[%(asctime)s]: %(levelname)s: %(module)s: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=format,
    handlers=[logging.StreamHandler(sys.stdout)]
)

values_bot_logger = logging.getLogger("Values-Assistant")
