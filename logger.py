import logging
import sys

stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] %(levelname)s\t %(message)s',
    handlers=handlers
)

logger = logging.getLogger('cloudflare-ddns')

