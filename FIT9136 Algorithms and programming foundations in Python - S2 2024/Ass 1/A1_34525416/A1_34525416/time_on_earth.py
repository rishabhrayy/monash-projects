"""
This code takes an input of the number of seconds from user 
and performs time conversions based on Earth's standard time.
"""

print("TIME ON EARTH")

#Take integer input from user with time in seconds
print("Input a time in seconds:")
user_time_in_seconds = int(input())

#floor divide the user input seconds by 60*60 (1hr=3600sec on Earth) to convert seconds into integer hours
#using floor divide as we need the integer floor output after division
hours = user_time_in_seconds//(60*60)
#calculate the seconds that remains after calculating the number of hours using the remainder operator
remaining_seconds_after_hours = user_time_in_seconds%(60*60) 

#floor divide the remaining seconds after calculating hours by 60 (1min=60sec on Earth) to convert remaining seconds into integer minutes
minutes = remaining_seconds_after_hours//(60) 
#calculate the seconds that remain after calculating the number of minutes.
seconds = remaining_seconds_after_hours%(60) 

#print the time on Earth in hours, minutes, seconds
print(f"\nThe time on Earth is {hours} hours {minutes} minutes and {seconds} seconds.")

