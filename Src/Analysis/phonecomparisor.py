# Data must be continiously updated to mantain valuable results


# Author: Jacinto27

# Author: Jacinto27
import os

import Levenshtein as Lev
import pandas as pd

# Path configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
pd.options.mode.chained_assignment = None  # default='war

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
                     f'OSs) (y): ').lower().strip() in ('y', 1, '1'):
                conditions_strictness[key] = True
        else:
            if input(f'Is {key} strict? (y): ').lower().strip() in ('y', 1, '1'):
                conditions_strictness[key] = True
    if all(item is None for item in conditions_strictness.values()):
        conditions_strictness = {key: True for key in conditions_strictness}

    return conditions_strictness


def optimized_suggestion(user_phone, strict_specs, data_compare_to=data):
    user_phone_row = data_compare_to[data_compare_to['brand'] + ' ' + data_compare_to['phone_name'] == user_phone]

    valid_rows = data_compare_to.apply(lambda row: check_conditions(user_phone_row, row, strict_specs), axis=1)

    # Filter the data based on valid_rows and sort by price
    upgrade = data_compare_to[valid_rows]
    valueAdded = upgrade['price(USD)'] - user_phone_row['price(USD)'].iloc[0]
    upgrade.loc[:, 'value_added'] = valueAdded
    # .clip(lower=0)
    # upgrade.loc[:, 'price_normalized'] = (upgrade['value_added'] - upgrade['value_added'].min()) / (
    #            upgrade['value_added'].max() - upgrade['value_added'].min())
    upgrade.loc[:, 'price_normalized'] = (upgrade['value_added'] - upgrade['value_added'].mean()) / upgrade[
        'value_added'].std()
    # ValueAdded variables

    """
        for index, row in upgrade.iterrows():
        if row['system'] == user_phone_row['system'].iloc[0]:
            systemUpgrade = upgrade['version'] - user_phone_row['version'].iloc[0]
        else:
            systemUpgrade = None
    upgrade['systemUpgrade'] = systemUpgrade
    """

    # TODO: Fix value assignment as per python warning
    # TODO: Make the values used for the final equation dependant of the first inputs that ask which specs are important
    for spec in ['version', 'resolution', 'battery', 'ram(GB)', 'storage(GB)']:
        if spec == 'version':
            upgrade.loc[upgrade['system'] == user_phone_row['system'].iloc[0], 'systemUpgrade'] = upgrade[spec].astype(
                float) - user_phone_row[spec].astype(float).iloc[0]
            upgrade.loc[upgrade['system'] != user_phone_row['system'].iloc[0], 'systemUpgrade'] = upgrade[
                'systemUpgrade'].mean()
            upgrade.loc[:, 'systemUpgrade'] = (upgrade['systemUpgrade'] - upgrade['systemUpgrade'].mean()) / upgrade[
                'systemUpgrade'].std()
        else:
            upgrade.loc[:, spec] = upgrade[spec] - user_phone_row[spec].iloc[0]
            upgrade.loc[:, spec] = (upgrade[spec] - upgrade[spec].mean()) / upgrade[spec].std()

    # In terms of tangible upgrades, a phone being newer isn't necessarily an upgrade, release date ignored

    # TODO: Incorporate video q specs into equation, not just filtering

    upgrade = upgrade.drop(upgrade.iloc[:, 7:17], axis=1)

    upgrade.loc[:, 'phoneValueAdded'] = (upgrade['version'].astype(float) + upgrade['resolution'].astype(int) +
                                         upgrade['battery'].astype(int) + upgrade['ram(GB)'].astype(int) +
                                         upgrade['storage(GB)'].astype(int))

    upgrade.loc[:, 'norm_results'] = upgrade['phoneValueAdded'] - upgrade['price_normalized']

    upgrade = upgrade.sort_values(by=['norm_results'], ascending=False)

    # TODO: Make internal function that filters results for a price range, however, prince data is unreliable as of now
    phone_in_data = upgrade.loc[upgrade['phone_name'] == user_phone_row['phone_name'].iloc(0)]

    if len(phone_in_data) == 0:  # If phone inside upgrade list then show only results above phone, else show the top 50
        return upgrade[['brand', 'phone_name', 'announcement_date', 'norm_results', 'price(USD)']].iloc[1:50]
    else:
        return upgrade[['brand', 'phone_name', 'announcement_date', 'norm_results', 'price(USD)']].loc[
            (upgrade['norm_results'] > phone_in_data['norm_results']),]


def custom_print(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
        print(df)


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
    This is because the Compared rows are boolean and are structured as such:
        QUALITY_LOW, QUALITY_MID, QUALITY_HIGH
    1   T           T               F
    2   T           F               F
    3 ...
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
    else:
        if len(matches) == 1:
            print('Is this your phone?', matches)
            answer = input('(y/n): ').lower().strip()
            if answer in ('y', 1, '1'):
                return matches[0]
        else:
            print('Exiting, please restart.')


# TODO: Fix the levenshtein search function, not always reliable
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
        if input('Is "Staying in the same Operating System" relevant? (y/n):').lower().strip() in (
                'y', 1, '1', 'yes', True):
            user_phone_system = data[data['brand'] + ' ' + data['phone_name'] == user_phone]['system'].iloc[0]
            data_OS_filter = data[data['system'] == user_phone_system]
            return custom_print(optimized_suggestion(user_phone, strict_conditions, data_compare_to=data_OS_filter))
        else:
            custom_print(optimized_suggestion(user_phone, strict_conditions, ))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
