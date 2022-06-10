import pytest
from names import Names


@pytest.fixture
def device_names():
    return ["CLOCK", "AND", "NAND"]


@pytest.mark.parametrize("name,expected_id", [["CLOCK", 0], ["SWITCH", None]])
def test_query_name_normal(name, expected_id, device_names):
    names = Names()
    names.lookup(device_names)
    assert names.query(name) == expected_id


def test_query_type_error(device_names):
    names = Names()
    names.lookup(device_names)
    with pytest.raises(TypeError):
        names.query(12)


def test_lookup(device_names):
    names = Names()
    keys = names.lookup(device_names)
    assert keys == [0, 1, 2]


@pytest.mark.parametrize("name_id, expected_name", [[0, "CLOCK"], [10, None]])
def test_id(name_id, expected_name, device_names):
    names = Names()
    names.lookup(device_names)
    name_str = names.get_name_string(name_id)
    assert name_str == expected_name


def test_id_lookup_type_error():
    names = Names()
    with pytest.raises(TypeError):
        names.get_name_string("test")
