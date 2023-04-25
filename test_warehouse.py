from mock import Mock
from warehouse import Warehouse

CAPACITY = 10


def test_valid_warehouse_with_valid_eggs():
    warehouse = Warehouse(CAPACITY)

    egg = Mock()
    egg.is_valid.return_value = True

    warehouse.eggs = [egg]
    assert warehouse.is_valid() == True


def test_invalid_warehouse_with_invalid_eggs():
    warehouse = Warehouse(CAPACITY)

    egg = Mock()
    egg.is_valid.return_value = False

    warehouse.eggs = [egg]
    assert warehouse.is_valid() == False


def test_invalid_warehouse_with_too_many_eggs():
    warehouse = Warehouse(CAPACITY)

    egg = Mock()
    egg.is_valid.return_value = True

    warehouse.eggs = [egg] * (CAPACITY + 5)
    assert warehouse.is_valid() == False


def test_get_capacity():
    warehouse = Warehouse(CAPACITY)

    assert warehouse.get_capacity() == CAPACITY


def test_empty_get_eggs():
    warehouse = Warehouse(CAPACITY)

    assert warehouse.get_eggs() == []


def test_filled_get_eggs():
    warehouse = Warehouse(CAPACITY)

    egg = Mock()
    warehouse.eggs = [egg]

    assert warehouse.get_eggs() == [egg]


def test_add_egg():
    warehouse = Warehouse(CAPACITY)
    egg = Mock()

    warehouse.add_egg(egg)

    assert len(warehouse.eggs) == 1
    assert warehouse.eggs == [egg]


def test_remove_egg():
    warehouse = Warehouse(CAPACITY)
    egg = Mock()

    warehouse.eggs = [egg, Mock()]
    warehouse.remove_egg(egg)

    assert len(warehouse.eggs) == 1
