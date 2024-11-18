import logging
import sys
from dataclasses import asdict

from bottle import route, request, run, response

from tapo_camera.tapo_camera import TapoCamera
from tapo_camera.privacy import PrivacyResponse

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-conf", "--config_file", default="config.json", help="Location of the application config file")
parser.add_argument("-p", "--port", default=8080, type=int, help="Port")
parser.add_argument("-d", "--debug_level", default="INFO", type=str, help="Debug Level CRITICAL/ERROR/WARNING/INFO/DEBUG. Default is WARNING")
args = vars(parser.parse_args())

PORT      = args["port"]
CONF_FILE = args["config_file"]
LOG_LEVEL = args["debug_level"]

logger = logging.getLogger('shelly_http_api')
logger.setLevel(LOG_LEVEL)
log_handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s')
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)
tapo_camera = TapoCamera(CONF_FILE)


def enable_cors(func):
    def wrapper(*args, **kwargs):
        response.set_header("Access-Control-Allow-Origin", "*")
        response.set_header("Content-Type", "application/json")
        response.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Origin, Content-Type")

        # skip the function if it is not needed
        if request.method == 'OPTIONS':
            return

        return func(*args, **kwargs)
    return wrapper


@route('/privacy')
@enable_cors
def camera_statuses():
    # check if request.json contains host parameter
    if request.json is None or 'host' not in request.json:
        privacy_statuses = tapo_camera.get_privacy_statuses()
    else:
        try:
            # Get host parameter from json request
            host: str = request.json['host']
            privacy_statuses = tapo_camera.get_privacy_status(host)
        except ValueError:
            return {'status': 'ERROR', 'message': 'Host not found in the list of hosts'}
    
    privacy_response = PrivacyResponse(privacy_statuses)

    return asdict(privacy_response)


@route('/privacy', method=['OPTIONS', 'POST'])
@enable_cors
def set_privacy_mode():
    if request.json is None or 'privacy' not in request.json:
        return {'status': 'ERROR', 'message': 'Missing privacy parameter'}
    
    input_enable_privacy: bool = request.json['privacy']
    
    if request.json is None or 'host' not in request.json:
        privacy_statuses = tapo_camera.set_privacy_modes(input_enable_privacy)
    else:
        host: str = request.json['host']
        try:
            privacy_statuses = tapo_camera.set_privacy_mode(host, input_enable_privacy)
        except ValueError:
            return {'status': 'ERROR', 'message': 'Host not found in the list of hosts'}
        
    privacy_response = PrivacyResponse(privacy_statuses)

    return asdict(privacy_response)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        configuration_file = sys.argv[1]
        tapo_camera = TapoCamera(configuration_file)

    try:
        run(host='0.0.0.0', port=PORT, debug=LOG_LEVEL.upper() == 'DEBUG')
    finally:
        logger.info("Exiting...")
