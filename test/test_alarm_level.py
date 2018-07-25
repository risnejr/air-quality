import json
import unittest
from alarm_level.alarm_level import AlarmLevel


class TestAlarmLevel(unittest.TestCase):

    def test_no_asset(self):
        self.test_1 = AlarmLevel('', 'test/test_spacing.csv')
        self.test_2 = AlarmLevel('not present', 'test/test_spacing.csv')
        with self.assertRaises(KeyError):
            self.test_1.read_node_ids()
        self.assertRaises(KeyError, self.test_2.read_node_ids)

    def test_csv_spacing(self):
        self.test = AlarmLevel('test', 'test/test_spacing.csv')
        self.test.read_node_ids()
        self.assertDictEqual({'1': 'uuid_1', '2': 'uuid_2'},
                             self.test.node_ids)

    def test_csv_columns(self):
        self.test = AlarmLevel('test', 'test/test_columns.csv')
        self.test.read_node_ids()
        self.assertDictEqual({'2': 'uuid_2'}, self.test.node_ids)

    def test_run(self):
        with open('test/test_response.json') as f:
            json_file = f.read()

        DotDict(json.loads(json_file))


class DotDict(dict):
    def __getattribute__(self, name):
        return self[name]
