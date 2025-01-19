import unittest
import os
import json
import csv
from datetime import datetime
from main import get_data_for_sport, clean_empty_data, write_csv, write_json, create_directory_structure

class TestMainFunctions(unittest.TestCase):

    def test_get_data_for_sport_football(self):
        infos = [
            MockElement("http://example.com"),
            None, None,
            MockElement("Team A"),
            MockElement("Team B"),
            MockElement("2"),
            MockElement("3")
        ]
        result = get_data_for_sport(infos, "football")
        expected = {
            'link': "http://example.com",
            'team1': "Team A",
            'score1': "2",
            'team2': "Team B",
            'score2': "3",
        }
        self.assertEqual(result, expected)

    def test_clean_empty_data_dict(self):
        data = {
            'key1': 'value1',
            'key2': '',
            'key3': None,
            'key4': {'nested1': 'value2', 'nested2': ''},
            'key5': {}
        }
        clean_empty_data(data)
        expected = {
            'key1': 'value1',
            'key4': {'nested1': 'value2'}
        }
        self.assertEqual(data, expected)

    def test_clean_empty_data_list(self):
        data = ['value1', '', None, {}, [], ['nested_value'], [None]]
        clean_empty_data(data)
        expected = ['value1', ['nested_value']]
        self.assertEqual(data, expected)

    def test_write_csv(self):
        file_path = "test.csv"
        matches = [
            {'link': 'http://example.com', 'team1': 'Team A', 'score1': '2', 'team2': 'Team B', 'score2': '3'},
            {'link': 'http://example2.com', 'team1': 'Team C', 'score1': '1', 'team2': 'Team D', 'score2': '4'}
        ]
        write_csv(file_path, matches)

        # Read the file and check contents
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        os.remove(file_path)  # Clean up
        self.assertEqual(rows, matches)

    def test_write_json(self):
        file_path = "test.json"
        matches = [
            {'link': 'http://example.com', 'team1': 'Team A', 'score1': '2', 'team2': 'Team B', 'score2': '3'},
            {'link': 'http://example2.com', 'team1': 'Team C', 'score1': '1', 'team2': 'Team D', 'score2': '4'}
        ]
        write_json(file_path, matches)

        # Read the file and check contents
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

        os.remove(file_path)  # Clean up
        self.assertEqual(data, matches)

    def test_create_directory_structure(self):
        base_path = "test_data"
        sport = "football"
        entity = "entity1"
        league = "league1"

        league_path = create_directory_structure(base_path, sport, entity, league)

        self.assertTrue(os.path.exists(league_path))

        # Clean up
        shutil.rmtree(base_path)

# Helper class to mock Selenium elements
class MockElement:
    def __init__(self, text):
        self.text = text

    def get_attribute(self, attr):
        if attr == 'href':
            return self.text
        return None

    def find_element(self, *args, **kwargs):
        return self

    def find_elements(self, *args, **kwargs):
        return [self]

if __name__ == '__main__':
    unittest.main()
