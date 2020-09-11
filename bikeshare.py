#This code provides stats based on bikeshare information from three cities

import time
import pandas as pd
import numpy as np
from datetime import datetime


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input('Would you like to see data for New York City, Chicago, or Washington?\n').lower()

    #Ask user for city name
    while city not in CITY_DATA:
        print('Sorry that is not a valid input. Please try again.')
        city = input('Would you like to see data for New York City, Chicago, or Washington?\n').lower()
    #Ask user if they would like to filter the data
    filter_response = ['month','weekday','both','none']
    filter = input('Would you like to filter by month, weekday, both or view all data?, type "none" to view all data.\n').lower()
    while filter not in filter_response:
        print('Sorry that is not a valid input. Please Try again.')
        filter = input('Please only enter: month, weekday, both, none.\n').lower()
    #Set month and day input as neccessary
    if filter=='month':
        day=0
        month_response = [1,2,3,4,5,6]
        month = int(input('Which month would you like to view data for? Please enter as integer (e.g. Jan=1).\n'))
        while month not in month_response:
            print('Sorry that is not a valid input. Please Try again.')
            month = input('Please enter as integer:Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6\n').lower()

    elif filter=='weekday':
        month=0
        day_response = [0,1,2,3,4,5,6]
        day = int(input('Which day would you like to view data for? Please enter day of week as integer (e.g. monday=0, tuesday=1...sunday=6).\n'))
        while day not in day_response:
            print('Sorry that is not a valid input. Please Try again.')
            day = input('Please enter: monday=0, tuesday=1, wednesday=2, thursday=3, friday=4, saturday=5, sunday=6.\n')

    elif filter=='both':
        month_response = [1,2,3,4,5,6]
        month = int(input('Which month would you like to view data for? Please enter as integer (e.g. Jan=1).\n'))
        while month not in month_response:
            print('Sorry that is not a valid input. Please Try again.')
            month = input('Please enter as integer:Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6\n').lower()
        day_response = [0,1,2,3,4,5,6]
        day = int(input('Which day would you like to view data for? Please enter day of week as integer (e.g. monday=0, tuesday=1...sunday=6).\n'))
        while day not in day_response:
            print('Sorry that is not a valid input. Please Try again.')
            day = input('Please enter: monday=0, tuesday=1, wednesday=2, thursday=3, friday=4, saturday=5, sunday=6.\n')
    else:
        month=0
        day=0


    print('-'*60)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month_int'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if month != 0:
        df = df[df['month_int']==month]
    if day != 0:
        df = df[df['day_of_week']==day]

    return df

def check_data(df):
    print("Nan in each columns" , df.isnull().sum(), sep='\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nWhat are the most frequent times of travel?\n')
    start_time = time.time()
    #Convert month integer to month name for output
    df['month_name']=pd.to_datetime(df['month_int'], format='%m').dt.month_name()
    #Create a list of days of week to output weekday
    days_of_week=['Mon', 'Tue', 'Wed', 'Thu','Fri','Sat','Sun']
    # Most common month
    common_month=df['month_name'].mode()[0]
    # Most common day of week
    common_day=days_of_week[df['day_of_week'].mode()[0]]
    # Most common start hour
    common_start_hour=df['Start Time'].dt.hour.mode()[0]

    #Display output
    print("The most common month of travel is {}.\nThe most common day to travel is {}.\nThe most common hour to start a journey is {}.\n".format(common_month,common_day,common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df['Start Station'].mode()[0]
    print("What is the most common station to start a journey?\n{}".format(common_start_station))

    # display most commonly used end station
    common_end_station=df['End Station'].mode()[0]
    print("What is the most common station to end a journey?\n{}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    start_and_end_station="Start:" +df['Start Station'] + " " + "End:" + df['End Station']
    combination_of_start_and_end=start_and_end_station.mode()[0]
    print("What is the most frequent combination of start and end stations?\n{}".format(combination_of_start_and_end))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].sum()))

    print("What is the total journey time in HH:MM:SS\n{}".format(total_travel_time))

    # display mean travel time
    average_travel_time=time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].mean()))
    print("What is the average journey time in HH:MM:SS\n{}".format(average_travel_time))

    # display longest travel time and retrieve start and end stations for this journey
    sorted_trip_duration=df.sort_values('Trip Duration', ascending=False)
    max_start_station=sorted_trip_duration['Start Station'].head(1)
    max_end_station=sorted_trip_duration['End Station'].head(1)
    max_travel_time=time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].max()))
    print("What is the longest journey time in HH:MM:SS\n{}".format(max_travel_time))
    print("The start station for this journey was:{}\n".format(max_start_station))
    print("The end station for this journey was:{}\n".format(max_end_station))

    # display shortes travel time and retrieve start and end station for this journey
    min_start_station=sorted_trip_duration['Start Station'].tail(1)
    min_end_station=sorted_trip_duration['End Station'].tail(1)
    min_travel_time=time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].min()))
    print("What is the shortest journey time in HH:MM:SS\n{}".format(min_travel_time))
    print("The start station for this journey was:{}\n".format(min_start_station))
    print("The end station for this journey was:{}\n".format(min_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types=df['User Type'].value_counts()
    print("How many different user types do we have?:")
    print(user_types)

    # Display counts of gender
    gender_count=df['Gender'].value_counts()
    print("How many males and females do we have?:")
    print(gender_count)

    # Display earliest, most recent, and most common year of birth
    earliest_birth_year=df['Birth Year'].min()
    most_recent_birth_year=df['Birth Year'].max()
    most_common_birth_year=df['Birth Year'].mode()[0]
    print("what year was the oldest user born?\n{}\nWhat year was the youngest user born?\n{}\nWhat is the most common birth year?\n{}".format(int(earliest_birth_year),int(most_recent_birth_year),int(most_common_birth_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        check_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city=='washington':
            print("No User stats available")
        else:
            user_stats(df)

        preview_data = input('\nWould you like to preview top 10 rows of your selected data? Enter yes or no.\n')
        if preview_data.lower() =='yes':
            print(df.head(10))
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
