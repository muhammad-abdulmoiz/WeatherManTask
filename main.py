import sys
import os
from typing import Optional


class WeatherReading:
    def __init__(self, date=None, max_temp=None, mean_temp=None, min_temp=None,
                 dew_point=None, mean_dew_point=None, min_dew_point=None,
                 max_humidity=None, mean_humidity=None, min_humidity=None,
                 max_pressure=None, mean_pressure=None, min_pressure=None,
                 max_visibility=None, mean_visibility=None,
                 min_visibility=None, max_wind_speed=None,
                 mean_wind_speed=None, max_gust_speed=None,
                 precipitation=None, cloud_cover=None, events=None,
                 wind_direction_degrees=None):

        self.date = date
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp
        self.dew_point = dew_point
        self.mean_dew_point = mean_dew_point
        self.min_dew_point = min_dew_point
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.max_pressure = max_pressure
        self.mean_pressure = mean_pressure
        self.min_pressure = min_pressure
        self.max_visibility = max_visibility
        self.mean_visibility = mean_visibility
        self.min_visibility = min_visibility
        self.max_wind_speed = max_wind_speed
        self.mean_wind_speed = mean_wind_speed
        self.max_gust_speed = max_gust_speed
        self.precipitation = precipitation
        self.cloud_cover = cloud_cover
        self.events = events
        self.wind_direction_degrees = wind_direction_degrees


class WeatherDataParser:
    def __init__(self, files_path):
        self.files_path = files_path
        self.readings = []

    def read_files(self):
        for filename in os.listdir(self.files_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.files_path, filename)
                with open(filepath, "r") as file:
                    # Skip the first row containing Headers
                    next(file)
                    for line in file:
                        # If the line is empty
                        if not line.strip():
                            continue
                        reading = self.parse_line(line)
                        if reading:
                            self.readings.append(reading)

    @staticmethod
    def parse_line(line: str) -> Optional[WeatherReading]:
        data = line.strip().split(",")
        # There are 23 fields in each row of readings
        if len(data) == 23:
            try:
                date = data[0]
                max_temp = float(data[1]) if data[1] else None
                mean_temp = float(data[2]) if data[2] else None
                min_temp = float(data[3]) if data[3] else None
                dew_point = float(data[4]) if data[4] else None
                mean_dew_point = float(data[5]) if data[5] else None
                min_dew_point = float(data[6]) if data[6] else None
                max_humidity = int(data[7]) if data[7] else None
                mean_humidity = int(data[8]) if data[8] else None
                min_humidity = int(data[9]) if data[9] else None
                max_pressure = float(data[10]) if data[10] else None
                mean_pressure = float(data[11]) if data[11] else None
                min_pressure = float(data[12]) if data[12] else None
                max_visibility = float(data[13]) if data[13] else None
                mean_visibility = float(data[14]) if data[14] else None
                min_visibility = float(data[15]) if data[15] else None
                max_wind_speed = int(data[16]) if data[16] else None
                mean_wind_speed = int(data[17]) if data[17] else None
                max_gust_speed = int(data[18]) if data[18] else None
                precipitation = float(data[19]) if data[19] else None
                cloud_cover = int(data[20]) if data[20] else None
                events = data[21]
                wind_direction_degrees = int(data[22]) if data[22] else None

                return WeatherReading(date, max_temp, mean_temp, min_temp,
                                      dew_point, mean_dew_point, min_dew_point,
                                      max_humidity, mean_humidity,
                                      min_humidity, max_pressure,
                                      mean_pressure, min_pressure,
                                      max_visibility, mean_visibility,
                                      min_visibility, max_wind_speed,
                                      mean_wind_speed, max_gust_speed,
                                      precipitation, cloud_cover, events,
                                      wind_direction_degrees)
            except ValueError:
                # Error occurred while converting data types, skip this line
                return None
        else:
            # Line doesn't contain the expected number of fields, skip it
            return None


class WeatherResultsCalculator:
    def __init__(self):
        pass

    @staticmethod
    def calculate_yearly_extremes(readings, year):
        highest_temp = float("-inf")
        highest_temp_day = None
        lowest_temp = float("inf")
        lowest_temp_day = None
        highest_humidity = float("-inf")
        highest_humidity_day = None

        for reading in readings:
            # Get year from the reading date (date format: YYYY-MM-DD)
            reading_year = reading.date.split('-')[0]
            if reading_year == year:
                if reading.max_temp and (highest_temp is None or
                                         reading.max_temp > highest_temp):
                    highest_temp = reading.max_temp
                    highest_temp_day = reading.date
                if reading.min_temp and (lowest_temp is None or
                                         reading.min_temp < lowest_temp):
                    lowest_temp = reading.min_temp
                    lowest_temp_day = reading.date
                if reading.max_humidity and (highest_humidity is None or
                                             reading.max_humidity >
                                             highest_humidity):
                    highest_humidity = reading.max_humidity
                    highest_humidity_day = reading.date

        return {
            "highest_temp": highest_temp,
            "highest_temp_day": highest_temp_day,
            "lowest_temp": lowest_temp,
            "lowest_temp_day": lowest_temp_day,
            "highest_humidity": highest_humidity,
            "highest_humidity_day": highest_humidity_day
        }

    @staticmethod
    def calculate_monthly_averages(readings, year, month):
        total_max_temp = 0
        total_min_temp = 0
        total_mean_humidity = 0
        no_of_entries = 0

        for reading in readings:
            reading_year, reading_month = reading.date.split('-')[:2]
            if reading_year == year and reading_month == month:
                if reading.max_temp:
                    total_max_temp += reading.max_temp
                if reading.min_temp:
                    total_min_temp += reading.min_temp
                if reading.mean_humidity:
                    total_mean_humidity += reading.mean_humidity
                no_of_entries += 1

        return {
            "avg_max_temp": WeatherResultsCalculator.calculate_average(
                total_max_temp, no_of_entries),
            "avg_min_temp": WeatherResultsCalculator.calculate_average(
                total_min_temp, no_of_entries),
            "avg_mean_humidity": WeatherResultsCalculator.calculate_average(
                total_mean_humidity, no_of_entries)
        }

    @staticmethod
    def calculate_average(total_value, no_of_entries):
        if no_of_entries <= 0:
            return None
        return total_value / no_of_entries


class WeatherReportsGenerator:
    def __init__(self, readings):
        self.readings = readings

    def display_yearly_extremes(self, year):
        extremes = WeatherResultsCalculator.calculate_yearly_extremes(
            self.readings, year)

        if extremes['highest_temp'] and extremes['highest_temp_day']:
            print(
                f"Highest: {extremes['highest_temp']}°C on "
                f"{self.format_date(extremes['highest_temp_day'])}")
        else:
            print("Highest temperature data not available.")

        if extremes['lowest_temp'] and extremes['lowest_temp_day']:
            print(
                f"Lowest: {extremes['lowest_temp']}°C on "
                f"{self.format_date(extremes['lowest_temp_day'])}")
        else:
            print("Lowest temperature data not available.")

        if extremes['highest_humidity'] and extremes['highest_humidity_day']:
            print(
                f"Humidity: {extremes['highest_humidity']}% on "
                f"{self.format_date(extremes['highest_humidity_day'])}")
        else:
            print("Highest humidity data not available.")

    @staticmethod
    def format_date(date_str):
        parts = date_str.split('-')
        # year = parts[0]
        month = parts[1]
        day = parts[2]
        month_name = WeatherReportsGenerator.get_month_name(int(month))
        return f"{month_name} {day}"

    @staticmethod
    def get_month_name(month):
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November",
                  "December"]
        return months[month - 1]

    def display_monthly_averages(self, year, month):
        averages = WeatherResultsCalculator.calculate_monthly_averages(
            self.readings, year, month)

        if averages['avg_max_temp']:
            print(f"Highest Average: {averages['avg_max_temp']:.2f}°C")
        else:
            print("Highest average temperature data not available.")

        if averages['avg_min_temp']:
            print(f"Lowest Average: {averages['avg_min_temp']:.2f}°C")
        else:
            print("Lowest average temperature data not available.")

        if averages['avg_mean_humidity']:
            print(
                f"Average Mean Humidity: {averages['avg_mean_humidity']:.2f}%")
        else:
            print("Average mean humidity data not available.")

    def display_monthly_temperature_charts(self, year, month):
        daily_temperature_readings = self._get_daily_temperature_readings(
            year, month)

        month_name = WeatherReportsGenerator.get_month_name(int(month))
        print(f"{month_name} {year}")

        self._draw_temperature_charts(daily_temperature_readings)

    def _get_daily_temperature_readings(self, year, month):
        daily_temperature_readings = {}

        for reading in self.readings:
            reading_year, reading_month, reading_day = reading.date.split('-')
            if reading_year == year and reading_month == month:
                day = int(reading_day)
                if day not in daily_temperature_readings:
                    daily_temperature_readings[day] = {'max_temp': None,
                                                       'min_temp': None}
                if reading.max_temp:
                    daily_temperature_readings[day][
                        'max_temp'] = reading.max_temp
                if reading.min_temp:
                    daily_temperature_readings[day][
                        'min_temp'] = reading.min_temp

        return daily_temperature_readings

    @staticmethod
    def _draw_temperature_charts(daily_temperature_readings):
        _RED = '\033[91m'  # Red
        _BLUE = '\033[94m'  # Blue
        _END_COLOR = '\033[0m'  # Reset color

        for day in sorted(daily_temperature_readings.keys()):
            max_temp = daily_temperature_readings[day]['max_temp']
            min_temp = daily_temperature_readings[day]['min_temp']

            max_bar = f"{_RED}{'+' * int(max_temp)}{_END_COLOR}" if (
                max_temp) else ''
            min_bar = f"{_BLUE}{'+' * int(min_temp)}{_END_COLOR}" if (
                min_temp) else ''

            print(f"{day:02} {max_bar} {max_temp}C")
            print(f"{day:02} {min_bar} {min_temp}C")


def main():
    if not validate_arguments(sys.argv):
        print_usage_and_exit()

    files_path = sys.argv[1]
    weather_data_reader = WeatherDataParser(files_path)
    weather_data_reader.read_files()
    reports_generator = WeatherReportsGenerator(weather_data_reader.readings)

    process_arguments(sys.argv[2:], reports_generator)


def validate_arguments(args):
    # Check if the arguments provided are valid.
    return len(args) >= 4 and len(args) % 2 == 0


def print_usage_and_exit():
    print("Usage: python main.py <file_path> -e <year> -a <year>/<month> -c "
          "<year>/<month>")
    sys.exit(1)


def process_arguments(arguments, reports_generator):
    for index in range(0, len(arguments), 2):
        option = arguments[index]
        date_string = arguments[index + 1]

        if option == "-e":
            process_yearly_extremes(date_string, reports_generator)
        elif option == "-a" or option == "-c":
            process_monthly_data(option, date_string, reports_generator)
        else:
            print("Invalid option. Options should be -e, -a, or -c.")
            sys.exit(1)


def process_yearly_extremes(date_string, reports_generator):
    if not is_valid_year(date_string):
        print("Invalid year format. Usage: -e <year>")
        sys.exit(1)
    reports_generator.display_yearly_extremes(date_string)


def is_valid_year(year):
    return year.isdigit() and len(year) == 4


def process_monthly_data(option, date_string, reports_generator):
    year, month = parse_year_month(date_string)
    if year is None or month is None:
        print("Invalid date format. Usage: -a/-c <year/month>")
        sys.exit(1)

    if option == "-a":
        reports_generator.display_monthly_averages(year, month)
    else:
        reports_generator.display_monthly_temperature_charts(year, month)


def parse_year_month(date_string):
    date_parts = date_string.split("/")
    if len(date_parts) != 2:
        return None, None

    year, month = date_parts
    if not (is_valid_year(year) and is_valid_month(month)):
        return None, None

    return year, month


def is_valid_month(month):
    if not month.isdigit():
        return False
    month_int = int(month)
    return 1 <= month_int <= 12


if __name__ == "__main__":
    main()
