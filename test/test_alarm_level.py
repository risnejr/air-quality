import json
import unittest
from alarm_level.alarm_level import AlarmLevel


class TestAlarmLevel(unittest.TestCase):

    def test_no_csv(self):
        self.assertRaises(FileNotFoundError, AlarmLevel,
                          '', 'test/non_existing_csv.csv')
        self.assertRaises(FileNotFoundError, AlarmLevel, '', '')

    def test_no_asset(self):
        test_1 = AlarmLevel('', 'test/test_key.csv')
        test_2 = AlarmLevel('not present', 'test/test_spacing.csv')
        self.assertRaises(KeyError, test_1.asset_ids)
        self.assertRaises(KeyError, test_2.asset_ids)

    def test_csv_spacing(self):
        test = AlarmLevel('test', 'test/test_spacing.csv')
        test.read_ids()
        self.assertDictEqual({'test': {'1': 'uuid_1', '2': 'uuid_2'}},
                             test.node_ids)

    def test_csv_columns(self):
        test = AlarmLevel('test', 'test/test_columns.csv')
        test.read_ids()
        self.assertDictEqual({'test': {'2': 'uuid_2'}}, test.node_ids)

    def test_run(self):
        test = AlarmLevel('test', 'test/test_key.csv')
        with open('test/test_response.json') as f:
            json_file = f.read()

        data = DotDict(json.loads(json_file))
        self.assertRaises(KeyError, test.run, data)


class DotDict(dict):

    def __getattribute__(self, name):
        return self[name]
