import pytest
from merge import merge_ingredients as m


def one(items):
    return m(items)[0][1]


def test_cup_plus_tbsp():            assert one([("milk", 1, "cup"), ("milk", 8, "tbsp")]) == ["1 1/2 cups"]
def test_quarter_cups():             assert one([("oil", .25, "cup"), ("oil", .25, "cup")]) == ["1/2 cup"]
def test_tbsp_roll_up_to_cup():      assert one([("butter", 6, "tbsp"), ("butter", 2, "tbsp")]) == ["1/2 cup"]
def test_tsp_roll_up_to_tbsp():      assert one([("salt", 1, "tsp"), ("salt", 2, "tsp")]) == ["1 tbsp"]
def test_awkward_stays_in_tsp():     assert one([("sugar", 2, "tbsp"), ("sugar", 1, "tsp")]) == ["7 tsp"]
def test_metric_weights():           assert one([("rice", 500, "g"), ("rice", 1, "kg")]) == ["1 1/2 kg"]
def test_us_weights():               assert one([("beef", 8, "oz"), ("beef", 1, "lb")]) == ["1 1/2 lb"]
def test_counts():                   assert one([("egg", 2, "each"), ("egg", 3, "each")]) == ["5"]
def test_name_case_and_spaces():     assert m([("Egg", 1, "each"), (" egg ", 1, "each")]) == [("egg", ["2"])]
def test_volume_and_weight_kept_apart():
    assert one([("flour", 1, "cup"), ("flour", 200, "g")]) == ["1 cup", "200 g"]
def test_separate_ingredients():     assert [n for n, _ in m([("b", 1, "cup"), ("a", 1, "cup")])] == ["a", "b"]
def test_unknown_unit():
    with pytest.raises(ValueError): m([("x", 1, "handful")])
def test_bad_quantity():
    with pytest.raises(ValueError): m([("x", 0, "cup")])
