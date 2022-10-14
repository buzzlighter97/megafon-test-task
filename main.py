import sys
from pprint import pprint

from parsing import get_weather_by_city
from excel_write import write_to_excel


def main():
    if len(sys.argv) > 1:
        city_name = sys.argv[1]
    else:
        city_name = input("Введите город для загрузки прогноза: ")
    result = get_weather_by_city(city_name)
    pprint(result)
    write_to_excel(city_name=city_name, result_list=result)


if __name__ == "__main__":
    main()
