import logging
import sys
from dataclasses import asdict

from bottle import route, request, run, response

from tapo_camera.tapo_camera import TapoCamera
from tapo_camera.privacy import PrivacyResponse

logger = logging.getLogger('shelly_http_api')
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s')
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)
tapo_camera = TapoCamera('config.json')


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
    privacy_statuses = tapo_camera.get_privacy_statuses()
    privacy_response = PrivacyResponse(privacy_statuses)

    return asdict(privacy_response)


@route('/privacy', method=['OPTIONS', 'POST'])
@enable_cors
def set_privacy_mode():
    input_enable_privacy: bool = request.json['privacy']
    privacy_statuses = tapo_camera.set_privacy_modes(input_enable_privacy)
    privacy_response = PrivacyResponse(privacy_statuses)

    return asdict(privacy_response)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        configuration_file = sys.argv[1]
        tapo_camera = TapoCamera(configuration_file)

    try:
        run(host='0.0.0.0', port=5020, debug=True)
    finally:
        logger.info("Exiting...")
