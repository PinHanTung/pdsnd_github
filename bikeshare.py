import time
import pandas as pd
from datetime import timedelta


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city_dict = { 1: 'chicago',
              2: 'new york city',
              3: 'washington' }
month_dict = { 0: 'all',
                1: 'January',
                2: 'February',
                3: 'March',
                4: 'April',
                5: 'May',
                6: 'June' }
day_dict = { 0: 'all',
                1: 'monday',
                2: 'tuesday',
                3: 'wednesday',
                4: 'thursday',
                5: 'friday',
                6: 'saturday',
                7: 'sunday' }
rev_month_dict = {value: key for key, value in month_dict.items()}
rev_day_dict = {value: key for key, value in day_dict.items()}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!\n')
    city, month, day = None, None, None

    # input 1: city
    while city not in city_dict:
        city = eval(input('Hint: 1 for Chicago, 2 for New York City, and 3 for Washington.\nEnter the code for the city: '))
        if city not in city_dict:
            print('Code not found, please enter again.\n')
        else:
            print(f'You\'ve chosen the city {city_dict[city].title()}.\n')
    city = city_dict[city]

    # input 2: month
    while month not in month_dict:
        month = eval(input('Enter a month number between 1 and 6, or type 0 for all months: '))
        if month not in month_dict:
            print('Invalid input, please enter again.\n')
        else:
            print(f'You\'ve chosen {month_dict[month]}.\n')
    month = month_dict[month]

    # input 3: day
    while day not in day_dict:
        day = eval(input('Hint: 1 for Monday, 2 for Tuesday, and so on. Enter 0 to select all days.\nEnter a number for the day of the week: '))
        if day not in day_dict:
            print('Invalid input, please enter again.\n')
        else:
            print(f'You\'ve chosen {day_dict[day]}.\n')
    day = day_dict[day]

    print('-'*40)
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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour 

    if month != 'all':
        df = df[df['month'] == rev_month_dict[month]]
    if day != 'all':
        df = df[df['day'] == rev_day_dict[day]] 
    
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = month_dict[ df['month'].mode()[0] ]
    print(f'The most common month: {common_month}')

    # display the most common day of week
    common_day = day_dict[ df['day'].mode()[0] ]
    print(f'The most common day: {common_day}')

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f'The most common start hour: {common_hour} (24-hour format)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'The most common start station: {common_start_station}')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'The most common end station: {common_end_station}')

    # display most frequent combination of start station and end station trip
    common_station_pair = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of start station and end station trip: \nFrom \'{}\' to \'{}\''.format(*common_station_pair))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    total_time_format = timedelta(seconds=total_travel_time)
    print(f'total travel time: {total_travel_time}s ({total_time_format})')

    # display mean travel time
    mean_travel_time = total_travel_time // df.shape[0]
    mean_time_format = timedelta(seconds=mean_travel_time)
    print(f'mean travel time: {mean_travel_time}s ({mean_time_format})')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    num_user_types = df['User Type'].value_counts()
    print(num_user_types, '\n')

    # Display counts of gender
    if 'Gender' in df.columns.to_list():
        num_gender = df['Gender'].value_counts()
        print(num_gender, '\n')
    else:
        print('No gender information is provided for this city.\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns.to_list():
        earliest_birth_year = int(df['Birth Year'].min())
        print(f'Earliest year of birth: {earliest_birth_year}')
        latest_birth_year = int(df['Birth Year'].max())
        print(f'Most recent year of birth: {latest_birth_year}')
        common_birth_year = int(df['Birth Year'].value_counts().idxmax())
        print(f'Most common year of birth: {common_birth_year}')
    else:
        print('No birth information is provided for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_data(df):
    '''Displays five rows of raw data in each iteration.'''
    for i in range(0, df.shape[0], 5):
        yield df[i:i+5]



def main():
    while True:
        print('-'*40)
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        answer = None
        result = None

        while (answer != 'no') & (answer != 'yes'):
            answer = input('\nWould you like to view the first five rows of raw data? Enter yes or no.\n')
            answer = answer.lower()
            if answer == 'yes':
                result = True
                gen = view_data(df)
            if (answer != 'no') & (answer != 'yes'):
                print('Answer yes or no. Please provide the answer again.')

        while result == True: 
            print('-'*40)
            print(next(gen))
            print('-'*40)
            result = False
            answer2 = None
            while (answer2 != 'no') & (answer2 != 'yes'):
                answer2 = input('\nWould you like to view the next five rows of raw data? Enter yes or no.\n')
                answer2 = answer2.lower()
                if answer2 == 'yes':
                    result = True
                if (answer2 != 'no') & (answer2 != 'yes'):
                    print('Answer yes or no. Please provide the answer again.')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
