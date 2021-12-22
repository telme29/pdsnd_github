import os
import time
import pandas as pd
#import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# list of months to get the index and the corresponding int
MONTH_LIST = ['all','january', 'february', 'march', 'april', 'may', 'june']
WEEKDAY_LIST = ['all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def system_exit(city_month_day):
    """Stops the program if the user types quit.
    """
    if city_month_day == 'quit':
        raise SystemExit 


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWould you like see the data for New York City, " 
                     "Chicago or Washington?\n>").lower().strip()
        while city not in CITY_DATA.keys():
            print("\nSomething is not right." 
                  "Please type the input as in the following or quit to stop.>")
            city = input("\nPlease type one of the cities New York City, Chicago or Washington!\n>").lower().strip()
            #System exit
            system_exit(city)

    # TO DO: get user input for month (all, january, february, ... , june)
        month = input("\nFor which month (january, february, march april, may, june or all for no filter) do you want the data?\n>").lower().strip()
        while month not in MONTH_LIST:
            print("\nSomething is not right. Please mind the formatting and be sure to enter a valid selection:>")
            month = input("\nPlease type one of the months (e.g. january, february, march april, may, june)"
                          "or all for no filter!\n>").lower().strip()
            #System exit
            system_exit(city)  

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("\nFor which weekday(monday, tuesday, wednesday etc. or all for no filter) do you want the data?\n>").lower().strip()
        while day not in WEEKDAY_LIST:
            print("\nSomething is not right. Please mind the formatting and be sure to enter a valid selection:>")
            day = input("\nPlease type one of the weekdays (monday, tuesday, wednesday etc.) "
                        "or all for no filter!\n>").lower().strip()
            #System exit
            system_exit(city) 
            
        # Filter input confirmation
        selected_filter = input("\nYour filter selection is [{}], [{}] and [{}]," 
                                "do you agree(please type [yes] or [no])?\n>".format(city, month, day))
        
        if selected_filter.lower() == 'yes':
            break
        else:
            print("\nOk, let's restart!") 

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
    #Kommentare all austauschen!! Yoktular template!!
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        month = MONTH_LIST.index(month)
        # create the new dataframe for the selected month
        df = df[df['month'] == month]

    if day != 'all':
        # create the new dataframe for the selected weekday
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month =  df['month'].mode()[0]
    print('The most common month: {}'.format(MONTH_LIST[common_month].title()))

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week: {}'.format(common_day_of_week))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is: {}'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commonly_used_start_station = str(df['Start Station'].mode()[0])
    print("The most commonly used start station is: {}".format(most_commonly_used_start_station))

    # display most commonly used end station
    most_commonly_used_end_station = str(df['End Station'].mode()[0])
    print("The most commonly used end station is: {}".format(most_commonly_used_end_station))

    # display most frequent combination of start station and end station trip
    df['Start_End_Station_Combination'] = (df['Start Station']+'to'+df['End Station'])
    frequent_start_end_station = str(df['Start_End_Station_Combination'].mode()[0])
    print("The most frequent combination of start station and end station trip is: {}".format(frequent_start_end_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    day = str(int(total_travel_time//86400))
    hour = str(int(total_travel_time % 86400)//3600)
    minutes = str((int(total_travel_time % 86400) % 3600) // 60)
    seconds = str(((int(total_travel_time % 86400) % 3600) % 60) % 60)          
    print('The total travel time is : {}d {}h {}min {}sec'.format(day, hour, minutes, seconds))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    hours_mean = str(int(mean_travel_time %86400)//3600)
    minutes_mean = str(int(mean_travel_time//60))
    seconds_mean = str(int(mean_travel_time % 60))
    print("The mean travel time is :{}h {}min {}sec".format(hours_mean, minutes_mean, seconds_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("The counts of user types are:")
    print(user_types)


    # Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nThe counts of genders are:")
        print(gender_distribution)
    except KeyError as err:
        print("Ooops! The given city doesn't contains data about user genders: {}. Error {} occured".format(city.title(), err))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nThe earliest year of birth: ",  earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("The most recent year of birth: ",  most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("The most common year of birth: ",  most_common_birth_year)
    except KeyError as err:
        print("We're sorry! There is no data of birth year for {}. Error {} occured.".format(city.title(), err))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def view_raw_data(df):
    """Displays data rows according users input
    Argument:
        Dataframe(df) - pandas dataframe(city data, mont, day)
    """       
    start_loc = 0
    while True:
        view_data = input('\nWould you like to see the first 5 rows of the individual trip data? Enter [yes] or [no]\n>')
        if view_data.lower() =='yes':
            # Display the raw data
            print("Five DataFrame rows:", df.head())
            start_loc += 5
            while True:            
                view_data = input("\nDo you wish to see the next 5 rows? Please enter [yes] or [no]?:\n>").lower()
                if view_data.lower() == 'yes':
                    print("\nOk, let's see the next 5 rows!\n") 
                    print(df.iloc[start_loc:start_loc+5])
                    start_loc += 5
                else:
                    return                   
        else:
            break

def main():
    """ The main function to start call the functions
    """    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        clear_console()
        
        if restart.lower() != 'yes':
            break


def clear_console():
    """Clear the console
    """    
    command = 'clear'
    # If Machine is running on Windows, use cls
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

if __name__ == "__main__":
    clear_console()
    main()
