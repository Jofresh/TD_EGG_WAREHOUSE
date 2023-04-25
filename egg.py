COUNTRIES_CODE = ["FR", "BE", "AL", "LU", "SU", "IT", "ES"]

MONTHS_IN_NUMBER = {
    "JA": "01",
    "FE": "02",
    "MA": "03",
    "AV": "04",
    "MI": "05",
    "JU": "06",
    "JL": "07",
    "AO": "08",
    "SE": "09",
    "OC": "10",
    "NO": "11",
    "DE": "12",
}


class Egg:
    def __init__(self, origin: str, color: str, registration: str):
        self.__origin = origin
        self.__color = color
        self.__registration = registration

    def get_origin(self):
        return self.__origin

    def get_color(self):
        return self.__color

    def is_valid(self):
        """
        Check if an egg is valid according to his registration.
        """

        if len(self.__registration) != 12:
            return False

        weight = self.__registration[:2]
        if not weight.isdigit():
            return False
        if int(weight) % 5 != 0:
            return False

        dash = self.__registration[2]
        if dash != "-":
            return False

        country = self.__registration[3:5]
        if country not in COUNTRIES_CODE:
            return False

        origin_code = self.__registration[5:8]
        if not origin_code.isdigit():
            return False
        if origin_code[0] == origin_code[2]:
            return False

        day = self.__registration[8:10]
        if not day.isdigit():
            return False
        if int(day) not in range(1, 31 + 1):
            return False

        month = self.__registration[10:12]
        if month not in MONTHS_IN_NUMBER.keys():
            return False

        if day == MONTHS_IN_NUMBER[month]:
            return False

        return True
