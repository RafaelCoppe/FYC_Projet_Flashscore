import pytest
from main import get_data_for_sport
from main import clean_empty_data
from main import create_directory_structure
from main import write_csv, write_json
from unittest.mock import MagicMock
from unittest.mock import patch

# Fixture pour mocker les infos
@pytest.fixture
def mock_infos():
    info = MagicMock()
    info._get_attribute.side_effect = lambda attr: f"mock_href_{attr}"
    text_values = [
        "", "", "",  # Index 0-2 : non utilisés
        "Mock Team 1",  # Index 3 : Team 1
        "Mock Team 2",  # Index 4 : Team 2
        "1",  # Index 5 : Score 1
        "2",  # Index 6 : Score 2
    ]
    info.text = MagicMock(side_effect=lambda: text_values.pop(0))
    return [info] * 9

def test_get_data_for_sport(mock_infos):
    football_data = get_data_for_sport(mock_infos, "football")
    rugby_data = get_data_for_sport(mock_infos, "rugby")

    assert football_data['team1'] == "Mock Team 1"
    assert football_data['score1'] == "1"
    assert rugby_data['team1'] == "Mock Team 1"
    assert rugby_data['score1'] == "1"

@pytest.mark.parametrize(
    "input_data, expected",
    [
        ({"a": 1, "b": None}, {"a": 1}),  # Cas d'un dictionnaire avec une valeur vide
        ([1, None, 2], [1, 2]),  # Cas d'une liste avec des valeurs vides
        ([{"a": None}, {"b": 2}], [{"b": 2}]),  # Cas d'une liste de dictionnaires
    ],
)

def test_clean_empty_data(input_data, expected):
    clean_empty_data(input_data)
    assert input_data == expected

@patch("os.makedirs")
def test_create_directory_structure(mock_makedirs):
    path = create_directory_structure("base", "football", "entity1", "league1")

    assert mock_makedirs.call_count == 3
    assert path == "base/football/entity1/league1"

@patch("builtins.open", new_callable=MagicMock)
def test_write_json(mock_open):
    write_json("test.json", [{"team1": "Team A", "score1": "1", "team2": "Team B", "score2": "2"}])
    mock_open.assert_called_once_with("test.json", "w", encoding="utf-8")

@patch("builtins.open", new_callable=MagicMock)
@patch("csv.DictWriter")
def test_write_csv(mock_dict_writer, mock_open):
    write_csv("test.csv", [{"team1": "Team A", "score1": "1", "team2": "Team B", "score2": "2"}])
    mock_open.assert_called_once_with("test.csv", "w", encoding="utf-8")
    mock_dict_writer.return_value.writerows.assert_called_once()