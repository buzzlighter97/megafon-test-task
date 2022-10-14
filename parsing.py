from typing import Any, List

import bs4
import requests


def parse_date(card_object: Any) -> str:
    result = card_object.find("strong", class_="forecast-details__day-number")
    if result:
        return result.text


def parse_month_name(card_object: Any) -> str:
    result = card_object.find("span", class_="forecast-details__day-month")
    if result:
        return result.text


def parse_magnetic_field_status(card_object: Any) -> str:
    forecast_line = card_object.find("dl", class_="forecast-fields")
    if forecast_line:
        labels = forecast_line.find_all("dt", class_="forecast-fields__label")
        for label in labels:
            if label.text == "Магнитное поле":
                return label.findNext("dd").text
    return ""


def calculate_median_temperature(temp_values: List) -> int:
    if len(temp_values) == 3:
        median_temperature = int((temp_values[0] + temp_values[1])/2)
        return median_temperature
    else:
        return temp_values[0]


def get_median_daytime_temperature(row_obj: Any) -> int:
    temp_values = row_obj.find_all("span", class_="temp__value")
    temperature = []
    for temp in temp_values:
        temperature.append(int(temp.text))
    return calculate_median_temperature(temperature)


def parse_info(card_object: Any) -> List:
    result_list = []
    rows = card_object.find_all("tr", class_="weather-table__row")
    for row in rows:
        daypart = row.find("div", "weather-table__daypart").text
        temperature = get_median_daytime_temperature(row)
        weather_condition = row.find(
            "td",
            class_="weather-table__body-cell weather-table__body-cell_type_condition",
        ).text
        air_pressure = int(
            row.find(
                "td",
                class_="weather-table__body-cell weather-table__body-cell_type_air-pressure",
            ).text
        )
        air_humidity = int(
            row.find(
                "td",
                class_="weather-table__body-cell weather-table__body-cell_type_humidity",
            ).text[:-1]
        )
        # wind_speed = float(row.find('span', class_="wind-speed").text)
        # wind_direction = row.find("div",  class_="weather-table__wind-direction").text
        info_tuple = (
            daypart,
            temperature,
            air_pressure,
            air_humidity,
            weather_condition,
        )
        result_list.append(info_tuple)
    return result_list


def calculate_average_day_temperature(info_list: List) -> float:
    summ_temperature = 0
    for i in range(3):
        summ_temperature += info_list[i][1]
    average_temperature = int(summ_temperature / 3)
    return average_temperature


def check_pressure_difference(info_list: List) -> str:
    pressure_values = [x[2] for x in info_list]
    max_pressure = pressure_values[0]
    min_pressure = pressure_values[0]
    max_pressure_index = 0
    min_pressure_index = 0
    for i in range(4):
        if pressure_values[i] > max_pressure:
            max_pressure = pressure_values[i]
            max_pressure_index = i
        if pressure_values[i] < min_pressure:
            min_pressure = pressure_values[i]
            min_pressure_index = i
    pressure_difference = max_pressure - min_pressure
    if pressure_difference >= 5:
        if max_pressure_index > min_pressure_index:
            return "ожидается резкое увеличение давления"
        else:
            return "ожидается резкое увеличение давления"
    else:
        return ""


def get_weather_by_city(city_name: str) -> List:
    response = requests.get(
        url=f"https://yandex.ru/pogoda/{city_name}/details"
    )
    soup = bs4.BeautifulSoup(response.text, "lxml")
    cards_list = soup.find_all("article", class_="card")

    result_list = []

    days_counter = 0
    for card in cards_list:
        if days_counter == 7:
            break
        if len(card["class"]) == 1:
            date = parse_date(card)
            month = parse_month_name(card)
            magnetic_field = parse_magnetic_field_status(card)
            info = parse_info(card)
            average_temperature = calculate_average_day_temperature(info)
            pressure_difference_status = check_pressure_difference(info)
            day_info = [
                date,
                month,
                magnetic_field,
                info,
                average_temperature,
                pressure_difference_status,
            ]
            result_list.append(day_info)
        days_counter += 1
    return result_list
