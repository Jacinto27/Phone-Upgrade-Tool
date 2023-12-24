import os

import Levenshtein as Lev
import pandas as pd

# Path configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))

datafile = os.path.join(project_root, 'Data', 'Processed', 'cleaned_all_phones_processed.csv')  # File Location
# Read data
data = pd.read_csv(datafile)
data = pd.DataFrame(data)
data['announcement_date'] = pd.to_datetime(data['announcement_date'])
data['price(USD)'] = pd.to_numeric(data['price(USD)'], errors='coerce')


# Functions


def user_conditions():
    conditions_strictness = dict.fromkeys(
        ['announcement_date', 'resolution', 'battery', 'ram(GB)', 'storage(GB)', 'system', 'recording quality'])
    print(
        'Select strict conditions, type y or 1 for conditions that must be strictly equal or higher than your current '
        'phone, any other value inputted will be assumed flexible: ')
    for key in conditions_strictness:
        if key == 'system':
            if input(f'Is the launch OS version strict? (this only takes into account version numbers for the same '
                     f'OSs) (y): ').lower().strip() in ('y', 1):
                conditions_strictness[key] = True
        else:
            if input(f'Is {key} strict? (y): ').lower().strip() in ('y', 1):
                conditions_strictness[key] = True
    if all(condition is None for condition in conditions_strictness.values()):
        conditions_strictness = {key: True for key in conditions_strictness}

    return conditions_strictness


def optimized_suggestion(user_phone, strict_specs, data_compare_to=data):
    user_phone_row = data_compare_to[data_compare_to['brand'] + ' ' + data_compare_to['phone_name'] == user_phone]

    valid_rows = data_compare_to.apply(lambda row: check_conditions(user_phone_row, row, strict_specs), axis=1)

    # Filter the data based on valid_rows and sort by price
    upgrade = data_compare_to[valid_rows].sort_values(by=['price(USD)'])
    upgrade = upgrade.drop(upgrade.iloc[:, 7:16], axis=1)
    return print(upgrade)


def check_conditions(user_phone_row, phones_to_compare, specs: list):
    # def check_row(row):
    for spec in specs:
        if spec == 'recording quality':
            if not check_record_q(user_phone_row, phones_to_compare):
                return False
        elif spec == 'announcement_date':
            if phones_to_compare[spec].strftime('%Y') < user_phone_row['announcement_date'].dt.strftime('%Y').iloc[0]:
                return False
        elif spec == 'system':
            if phones_to_compare['system'] == user_phone_row['system'].iloc[0]:
                if phones_to_compare['version'] < user_phone_row['version'].iloc[0]:
                    return False
        else:
            if phones_to_compare[spec] < user_phone_row[spec].iloc[0]:
                return False
    return True


def check_record_q(user_phone_row, compared_row) -> bool:
    video_resolution = ['video_720p', 'video_1080p']
    video_quality = ['video_4K', 'video_8K']
    video_fps = ['video_30fps', 'video_60fps', 'video_120fps', 'video_240fps', 'video_480fps', 'video_960fps']
    return (is_higher_in_category(user_phone_row, compared_row, video_resolution) or
            is_higher_in_category(user_phone_row, compared_row, video_quality) or
            is_higher_in_category(user_phone_row, compared_row, video_fps))


def is_higher_in_category(benchmark_row, compared_row, categories):
    """
    Compares two rows from right to left in a given set of categories.
    Returns True if the first mismatch favors the compared row.
    """
    for category in reversed(categories):
        if compared_row[category] != benchmark_row[category].iloc[0]:
            return compared_row[category]
    return False


def get_user_phone():
    phone_order = int()
    user_phone = input('Whats your phone? ').strip().lower()
    matches = find_match(user_phone, data['brand'] + ' ' + data['phone_name'])
    try:
        matches[0]
    except IndexError:
        print('No matches, try again.')
        return

    if len(matches) != 1 and len(matches) != 0:
        print('Possible matches:', matches)
        max_attempts = 3
        attempt_number = 0

        while attempt_number < max_attempts:
            try:
                phone_order = input('Choose a number (1-10): ')
                phone_order = int(phone_order)  # Convert to integer and store back

                if phone_order < 1 or phone_order >= 10:
                    raise ValueError('Number must be less than 10 and greater than 1, try again.')

                # If input is valid, break from the loop
                break

            except ValueError:
                # This will catch both, non-integer values and integers greater than 10
                attempt_number += 1
                print('Invalid input. Please put a number less than 10.')
                if attempt_number == max_attempts:
                    print("Maximum number of attempts reached. Exiting.")
        return matches[phone_order - 1]


def find_match(user_input, options, max_distance=2, max_matches=10):
    matches = []
    for i in options:
        if len(matches) >= max_matches:
            break
        distance = Lev.distance(user_input, i.lower())
        if distance <= max_distance:
            matches.append((i, distance))

    matches.sort(key=lambda x: x[1])
    return [match[0] for match in matches[:max_matches]]


def main():
    user_phone = get_user_phone()

    if user_phone is None:
        return
    else:
        strict_conditions = [key for key, value in user_conditions().items() if value is True]
        if input('Is "Staying in the same Operating System" relevant? (y/n):').lower().strip() in ('y', 1, 'yes', True):
            user_phone_system = data[data['brand'] + ' ' + data['phone_name'] == user_phone]['system']
            data_OS_filter = data[data['system'] == user_phone_system]
            return optimized_suggestion(user_phone, strict_conditions, data_compare_to=data_OS_filter)
        else:
            return optimized_suggestion(user_phone, strict_conditions, )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
