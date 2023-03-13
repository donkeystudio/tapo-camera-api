import unittest

from tapo_camera.tapo_camera import TapoCamera


class TapoCameraTestCase(unittest.TestCase):
    def test_privacy_statuses_are_returned(self):
        tapo_camera = TapoCamera('test/no_hosts_config.json')
        statuses = tapo_camera.get_privacy_statuses()
        self.assertListEqual(statuses, [])

    def test_privacy_statuses_are_not_set(self):
        tapo_camera = TapoCamera('test/no_hosts_config.json')
        statuses = tapo_camera.set_privacy_modes(True)
        self.assertListEqual(statuses, [])
