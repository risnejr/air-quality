import json
import unittest
from aq_level.aq_level import AQLevel


class TestAQLevel(unittest.TestCase):


    def test_no_asset(self):
        with open('../config.json', 'r') as f:
            node_ids = json.load(f)
        test_1 = AQLevel('install_team_room', '', node_ids)
        test_2 = AQLevel('nope, not here', 'not present', node_ids)
        self.assertRaises(KeyError, test_1.asset_ids)
        self.assertRaises(KeyError, test_2.asset_ids)


    def test_run(self):
        with open('test/test_config.json', 'r') as f:
            node_ids = json.load(f)

        test = AQLevel('test', 'test', node_ids)
        with open('test/test_response.json', 'r') as f:
            data = DotDict(json.load(f))

        self.assertRaises(KeyError, test.run, data)


class DotDict(dict):

    def __getattribute__(self, name):
        return self[name]
