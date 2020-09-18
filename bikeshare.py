import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS_NUMBER = {'all': 0, 'january': 1, 'february': 2,
                 'march': 3, 'april': 4,
                 'may': 5, 'june': 6,
                 'july': 7, 'august': 8}
DAYS = ['all', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter city name: ")
    while city not in CITY_DATA.keys():
        city = input("Enter Valid city name: ")

    # get user input for month (all, january, february, ... , june)
    month = input("Enter month name")
    while month not in MONTHS_NUMBER.keys():
        city = input("Enter VALID month!!: ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter day name")
    while day not in DAYS:
        city = input("Enter VALID Day!!: ")
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month == "all" and day != "all":
        df = df[df['day_of_week'] == day]

    elif month != "all" and day == "all":
        df = df[df['month'] == MONTHS_NUMBER[month]]

    elif month != "all" and day != "all":
        df = df[(df['day_of_week'] == day & df['month'] == MONTHS_NUMBER[month])]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    # display the most common start hour
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    popular_hour = df['hour'].mode()[0]

    print('{} is the most popular month, {} is the most popular day, and {} is the most popular hour'.
          format(popular_month, popular_day, popular_hour))

    # ____________________________________________________________
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    return popular_month, popular_day, popular_hour


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    # display most frequent combination of start station and end station trip
    df['start and end'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    popular_start_end = df['start and end'].mode()[0]

    print('{} is the most popular Start Station,'
          ' {} is the most popular End Station,'
          ' and {} is the most popular travel'.
          format(popular_start_station, popular_end_station, popular_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    return popular_start_station, popular_end_station, popular_start_end


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Total Travel Time'] = df['End Time'] - df['Start Time']

    # display mean travel time
    mean = df['Total Travel Time'].mean()
    print('{} is the mean of total travel time'.format(mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('user count {}'.format(user_types))

    # Display counts of gender
    gender = df['Gender'].value_counts()
    print('user count {}'.format(gender))

    # Display earliest, most recent, and most common year of birth
    earliest_year = df['Birth Year'].min()
    latest_year = df['Birth Year'].max()
    most_common = df['Birth Year'].mode()
    print('{} is Earliest birth year,'
          ' {} is Latest birth year,'
          ' {} is the most common year'.format(earliest_year, latest_year, most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
