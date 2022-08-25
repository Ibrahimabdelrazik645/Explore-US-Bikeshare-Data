import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city and whether they would like to filter the data by month, day, both or not at all to start analyzing.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) filter - filter by month, day, both or none
    """
    print("\nHello! Let's explore some US bikeshare data!")

    # get user input for city (chicago, new york city, washington).
    while True:
        try:
            city=input("\nWhich city would you like to see data for? Chicago, New York or Washington?\n").lower()
            #check the input "city" provided by the user
            if city=="chicago" or city=="new york" or city=="washington":
                break
            else:
                print("\nInvalid city. Please enter one city of the following.")
        except KeyboardInterrupt:
            print("KeyboardInterrupt, please enter a valid city")      

    # get user input for month (all, january, february, ... , june)
    def filter_by_month():
        """
        Asks user to specify a month to filter the data by to start analyzing.

        Returns:
            (str) month - name of the month to filter by, or "all" to apply no month filter
        """
        while True:
            try:
                month=input("\nWhich month? January, February, March, April, May or June?\n").lower()
                #check the input "month" provided by the user
                if month=="january" or month=="february" or month=="march" or month=="april" or month=="may" or month=="june" :
                    break
                else:
                    print("\nInvalid month. Please enter one of the follwing.")
            except KeyboardInterrupt:
                print("KeyboardInterrupt, please enter a valid month") 
        return month                 

    # get user input for day of week (all, monday, tuesday, ... sunday)
    def filter_by_day():
        """
        Asks user to specify a day to filter the data by to start analyzing.

        Returns:
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """        
        while True:
            try:
                day=input("\nWhich day? Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday or Friday?\n").lower()
                #check the input "day" provided by the user
                if day=="saturday" or day=="sunday" or day=="monday" or day=="tuesday" or day=="wednesday" or day=="thursday" or day=="friday":
                    break
                else:
                    print("\nInvalid day. Please enter one of the following.")
            except KeyboardInterrupt:
                print("KeyboardInterrupt, please enter a valid day")   
        return day  

    # get user input to choose to filter the data by month, day, both or not at all 
    while True:
        try:
            filter=input("\nWould you like to filter the data by month, day, both or not at all? Type \"none\" for no time filter.\n").lower()
            #check the input "filter" provided by the user
            if filter=="month" or filter=="day" or filter=="both" or filter=="none":
                break
            else:
                print("\nPlease enter a valid filter option")
        except KeyboardInterrupt:
            print("KeyboardInterrupt, please enter a valid filter option")   
    
    #apply the filter option provided by the user
    if filter=="both":
        month=filter_by_month()
        day=filter_by_day()
    elif filter=="month":
        month=filter_by_month()
        day="all"
    elif filter=="day":
        day=filter_by_day()
        month="all"     
    else:
        month="all"
        day="all"

    print('-'*50)
    return city, month, day, filter

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    df["hour"]=df["Start Time"].dt.hour 


    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df["month"]==month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"]==day.title()]
    
    return df

def time_stats(df,filter):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (str) df - the Pandas DataFrame containing city data filtered by month and day
        (str) filter - filter by month, day, both or none
    """
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    def common_month():
        """display the most common month"""

        months = ['January', 'February', 'March', 'April', 'May', 'June']

        #extact the most common month from the DataFrame and convert the index to month value
        common_month=df["month"].mode()[0]
        common_month_letters=months[common_month-1]

        #count the occurrence of the most common month in the DataFrame
        count=(df[df["month"]==common_month].count())["month"]

        print("\nThe most common month: {} ,    Count: {}".format(common_month_letters,count))

    def common_day():
        """display the most common day of week"""

        #extact the most common day from the DataFrame
        common_day=df["day_of_week"].mode()[0]

        #count the occurrence of the most common day in the DataFrame
        count=(df[df["day_of_week"]==common_day].count())["day_of_week"]

        print("\nThe most common day of the week: {} ,    Count: {}".format(common_day,count))

    def common_hour():
        """display the most common hour"""

        #extact the most common hour from the DataFrame
        common_hour=df["hour"].mode()[0]

        #count the occurrence of the most common hour in the DataFrame
        count=(df[df["hour"]==common_hour].count())["hour"]

        print("\nThe most common hour: {} ,    Count: {}".format(common_hour,count))

    print("Filter:",filter)

    #apply the filter option 
    if filter=="both":
        common_hour()
    elif filter=="month":
        common_day()
        common_hour()
    elif filter=="day":
        common_month()
        common_hour() 
    else:
        common_month()
        common_day()
        common_hour()                     

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def station_stats(df,filter):
    """Displays statistics on the most popular stations and trip.

    Args:
        (str) df - the Pandas DataFrame containing city data filtered by month and day
        (str) filter - filter by month, day, both or none
    """    
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()
    
    print("Filter:",filter,"\n")

    # display most commonly used start station
    common_start_station=df["Start Station"].mode()[0]
    count=df[df["Start Station"]==common_start_station]["Start Station"].count()
    print("The most common start station: {} ,    Count: {}".format(common_start_station,count))

    # display most commonly used end station
    common_end_station=df["End Station"].mode()[0]
    count=df[df["End Station"]==common_end_station]["End Station"].count()
    print("\nThe most common end station: {} ,    Count: {}".format(common_end_station,count))

    # display most frequent combination of start station and end station trip
    df["trip"]=df["Start Station"]+df["End Station"]
    common_trip=df['trip'].mode()[0]
    count=df[df['trip']==common_trip].count()['trip']
    start_station=df[df['trip']==common_trip]["Start Station"].mode()[0]
    end_station=df[df['trip']==common_trip]["End Station"].mode()[0]
    print('\nThe most common trip: ("{}", "{}"),  Count: {}'.format(start_station,end_station,count))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def trip_duration_stats(df,filter):
    """Displays statistics on the total and average trip duration.

    Args:
        (str) df - the Pandas DataFrame containing city data filtered by month and day
        (str) filter - filter by month, day, both or none
    """      
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    print("Filter:",filter,"\n")

    # display total travel time
    total_travel_time=df["Trip Duration"].sum()
    count=df["Trip Duration"].count()
    print("Total Travel Time: {} ,    Count: {}".format(total_travel_time,count))

    # display average travel time
    average_travel_time=df["Trip Duration"].mean()
    print("\nAverage Travel Time: {}".format(average_travel_time))    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def user_stats(df,filter,city):
    """Displays statistics on bikeshare users.

    Args:
        (str) df - the Pandas DataFrame containing city data filtered by month and day
        (str) filter - filter by month, day, both or none
        (str) city - name of the city to analyze
    """   
    print("\nCalculating User Statistics...\n")
    start_time = time.time()

    print("Filter:",filter,"\n")

    
    # Display counts of user types
    user_types = df["User Type"].value_counts()
    subscriber=user_types["Subscriber"]
    customer=user_types["Customer"]
    print("User Type:\n","Subscriber: {} ,    Customer: {}".format(subscriber,customer))
    
    #check whether there is user personal data for the given city or not
    if city=="chicago" or city=="new york":

        # Display counts of gender
        gender = df["Gender"].value_counts()
        male=gender["Male"]
        female=gender["Female"]
        print("\nGender:\n","Male: {} ,    Female: {}".format(male,female))

        # Display earliest, most recent, and most common year of birth
        birth_year= df["Birth Year"]
        earliest_year=int(birth_year.min())
        recent_year=int(birth_year.max())
        common_year=int(birth_year.mode()[0])
        print("\nBirth Year:\n","Earliest Year: {} ,    Recent Year: {} ,    Common Year: {}".format(earliest_year,recent_year,common_year))
    else:
        print("\nNo user personal data to share.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def main():
    while True:
        city,month,day,filter=get_filters()
        df=load_data(city,month,day)

        time_stats(df,filter)
        station_stats(df,filter)
        trip_duration_stats(df,filter)
        user_stats(df,filter,city)
        df = pd.read_csv(CITY_DATA[city])

        n=5
        while True:
            try:
                raw_data = input("\nWould you like to view individual trip data? Enter yes or no.\n").lower()
                if raw_data=="no" or n==df["Start Time"].count()-1:
                    break
                elif raw_data=="yes":
                    print(df.head(n))
                    n+=5  
                else:    
                    print("\nPlease enter a valid option. yes or no.")
            except KeyboardInterrupt:
                print("KeyboardInterrupt, please enter a valid option") 

               

        while True:
            try:
                restart = input("\nWould you like to restart? Enter yes or no.\n").lower()
                if restart =="yes" or restart=="no":
                    break
                else:
                    print("\nPlease enter a valid option. yes or no.")
            except KeyboardInterrupt:
                print("KeyboardInterrupt, please enter a valid option")  

        if restart=="no":
            print("\nGood Luck, Bye!\n")
            break                           


if __name__ == "__main__":
	main()
