import pytest
from string_utils import StringUtils


string_utils = StringUtils()


@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("skypro", "Skypro"),
    ("hello world", "Hello world"),
    ("python", "Python"),
])
def test_capitalize_positive(input_str, expected):
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("123abc", "123abc"),
    ("", ""),
    ("   ", "   "),
])
def test_capitalize_negative(input_str, expected):
    assert string_utils.capitalize(input_str) == expected

@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("   skypro", "skypro"),
    ("  hello", "hello"),
    (" test", "test"),
    ("abc", "abc"),           # без пробелов
    ("", ""),                 # пустая строка
    ("a", "a"),               # один символ без пробелов
])
def test_trim_positive(input_str, expected):
    assert string_utils.trim(input_str) == expected

@pytest.mark.negative
def test_trim_negative():
    """Тесты на строки с пробелами не в начале"""
    assert string_utils.trim("hello  ") == "hello  "    # пробелы в конце
    assert string_utils.trim("hello world") == "hello world"  # пробелы в середине
    assert string_utils.trim("  hello  world  ") == "hello  world  "

@pytest.mark.positive
@pytest.mark.parametrize("string, symbol", [
    ("SkyPro", "S"),
    ("SkyPro", "k"),
    ("SkyPro", "P"),
    ("SkyPro", "o"),
    ("Hello World", " "),
    ("123", "2"),
    ("", ""),  # поиск пустой строки в пустой строке
    ("test", "t"),  # несколько вхождений
])
def test_contains_positive(string, symbol):
    assert string_utils.contains(string, symbol) == True

@pytest.mark.negative
@pytest.mark.parametrize("string, symbol", [
    ("SkyPro", "U"),
    ("SkyPro", "s"),  # регистр имеет значение
    ("Hello", "x"),
    ("", "a"),  # поиск в пустой строке
    ("test", "z"),
])
def test_contains_negative(string, symbol):
    assert string_utils.contains(string, symbol) == False

@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    # Удаление одного символа
    ("SkyPro", "k", "SyPro"),
    ("hello", "l", "heo"),
    ("banana", "a", "bnn"),
    # Удаление подстрок
    ("SkyPro", "Pro", "Sky"),
    ("hello world", "o w", "hellorld"),
    ("banana", "nan", "baa"),
])
def test_delete_symbol_positive(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected

@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    # Символ не найден
    ("SkyPro", "x", "SkyPro"),
    ("hello", "z", "hello"),
    ("test", "abc", "test"),
])
def test_delete_symbol_negative(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected



