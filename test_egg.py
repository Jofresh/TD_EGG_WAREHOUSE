from egg import Egg

EGG_ORIGIN = "farm"
EGG_COLOR = "yellow"


def test_get_origin():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "05-FR12301FE")
    assert egg.get_origin() == EGG_ORIGIN


def test_get_color():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "05-FR12301FE")
    assert egg.get_color() == EGG_COLOR


def test_get_registration():
    registration = "05-FR12301FE"
    egg = Egg(EGG_ORIGIN, EGG_COLOR, registration)
    assert egg.get_registration() == registration


def test_valid_egg_registration():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "05-FR12301FE")
    assert egg.is_valid() == True


def test_invalid_egg_weight():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "12-FR12301FE")
    assert egg.is_valid() == False


def test_invalid_egg_dash():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "05 FR12301FE")
    assert egg.is_valid() == False


def test_invalid_egg_country():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "05-ZZ12301FE")
    assert egg.is_valid() == False


def test_invalid_egg_origin_code():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "05-FR12101FE")
    assert egg.is_valid() == False


def test_invalid_egg_day():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "05-FR12399FE")
    assert egg.is_valid() == False


def test_invalid_egg_month():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "05-FR12301ZZ")
    assert egg.is_valid() == False


def test_invalid_day_same_as_month():
    egg = Egg(EGG_ORIGIN, EGG_COLOR, "05-FR12302FE")
    assert egg.is_valid() == False
