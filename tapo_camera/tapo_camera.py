import concurrent.futures
import json
import logging
from dataclasses import dataclass

from pytapo import Tapo

from tapo_camera.privacy import Privacy

logger = logging.getLogger('TapoCamera')


@dataclass
class TapoCameraHost:
    host: str
    name: str


class TapoCamera:
    __PRIVACY_MODE_ENABLED = 'on'

    def __init__(self, configuration_file: str):
        with open(file=configuration_file, encoding='UTF-8') as configuration:
            self.__conf = json.load(configuration)
        configuration.close()

        self.__hosts: [TapoCameraHost] = []
        for host in self.__conf['hosts']:
            self.__hosts.append(TapoCameraHost(host['host'], host['name']))

        self.__user = self.__conf['user']
        self.__password = self.__conf['password']

    def get_privacy_statuses(self, retry_count: int = 0) -> [Privacy]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            return list(executor.map(self.__get_privacy_status, self.__hosts))
        
    def get_privacy_status(self, host: str) -> Privacy:
        # Check if the host is in the list of hosts
        if host not in [x.host for x in self.__hosts]:
            raise ValueError('Host not found in the list of hosts')
        else:
            name: str = next((x.name for x in self.__hosts if x.host == host), None)
        return self.__get_privacy_status(TapoCameraHost(host, name))

    def __get_privacy_status(self, host: TapoCameraHost, retry_count=0) -> Privacy:
        try:
            tapo = Tapo(host.host, self.__user, self.__password)
            privacy_mode: dict = tapo.getPrivacyMode()
            is_privacy_enabled = privacy_mode['enabled'] == self.__PRIVACY_MODE_ENABLED
            # Find the name of the camera from self.__hosts
            name: str = next((x.name for x in self.__hosts if x.host == host.host), host.name)

            return Privacy(host.host, is_privacy_enabled, name)
        except:
            logger.exception('Error while fetching camera privacy status')

            # With retry count 10 it can take up to ~30 seconds to finish when IP/host can't be reached
            if retry_count < 10:
                self.__get_privacy_status(host, retry_count + 1)

    def set_privacy_modes(self, enable_privacy: bool) -> [Privacy]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            return list(executor.map(self.__set_privacy_mode(enable_privacy), self.__hosts))
        
    def set_privacy_mode(self, host: str, enable_privacy: bool) -> Privacy:
        # Check if the host is in the list of hosts
        if host not in [x.host for x in self.__hosts]:
            raise ValueError('Host not found in the list of hosts')
        else:
            name: str = next((x.name for x in self.__hosts if x.host == host), None)
        return self.__set_privacy_mode(enable_privacy)(TapoCameraHost(host, name))

    def __set_privacy_mode(self, enable_privacy: bool):
        def __privacy(host: TapoCameraHost) -> Privacy:
            tapo = Tapo(host.host, self.__user, self.__password)
            tapo.setPrivacyMode(enable_privacy)
            # Find the name of the camera from self.__hosts
            name: str = next((x.name for x in self.__hosts if x.host == host.host), host.name)
            return Privacy(host.host, enable_privacy, name)

        return __privacy
