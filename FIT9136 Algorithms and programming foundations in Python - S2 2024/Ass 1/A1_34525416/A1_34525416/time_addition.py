"""
This excerpt of the code takes an input of the number of seconds from user 
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


"""
This part of the code takes an input of time-system on Trisolaris
and converts into seconds, minutes, and hours as per the Trisolaris's standard time.
"""

print("\nTIME ON TRISOLARIS")
#Take integer input of number of seconds in a minute on Trisolaris from user 
print("Input the number of seconds in a minute on Trisolaris:")
secs_in_a_min_on_trisolaris = int(input())

#Take integer input of number of minutes in an hour on Trisolaris from user
print("Input the number of minutes in an hour on Trisolaris:")
mins_in_a_hour_on_trisolaris = int(input())

#Calculate number of seconds in an hour on Trisolaris
secs_in_a_hour_on_trisolaris = (mins_in_a_hour_on_trisolaris*secs_in_a_min_on_trisolaris)

# Convert the user input seconds into hours, minutes, and seconds for Trisolaris
# Using the time system on Trisolaris defined by the user
hours_on_Trisolaris = user_time_in_seconds//secs_in_a_hour_on_trisolaris
remaining_seconds_after_hours_on_Trisolaris = user_time_in_seconds%secs_in_a_hour_on_trisolaris
minutes_on_Trisolaris = remaining_seconds_after_hours_on_Trisolaris//secs_in_a_min_on_trisolaris
seconds_on_Trisolaris = remaining_seconds_after_hours_on_Trisolaris%secs_in_a_min_on_trisolaris 

#print the time on Trisolaris in hours, minutes, seconds
print(f"\nThe time on Trisolaris is {hours_on_Trisolaris} hours {minutes_on_Trisolaris} minutes and {seconds_on_Trisolaris} seconds.")

"""
This part of the code takes an input of the number of seconds of waiting from user 
and converts into seconds, minutes, and hours as per the time convention on Trisolaris.
"""

print("\nTIME AFTER WAITING ON TRISOLARIS")

# Input a duration in seconds for waiting
print("Input a duration in seconds:")
seconds_in_waiting = int(input())

#adding the waiting seconds to the user entered seconds for calculation
revised_seconds = user_time_in_seconds+seconds_in_waiting

#calculating the time on trisolaris after waiting 
hours_on_Trisolaris = revised_seconds//secs_in_a_hour_on_trisolaris
remaining_seconds_after_hours_on_Trisolaris = revised_seconds%secs_in_a_hour_on_trisolaris
minutes_on_Trisolaris = remaining_seconds_after_hours_on_Trisolaris//secs_in_a_min_on_trisolaris
seconds_on_Trisolaris = remaining_seconds_after_hours_on_Trisolaris%secs_in_a_min_on_trisolaris 


#This prints the time on Trisolaris in hours, minutes, seconds after waiting:
print(f"\nThe time on Trisolaris after waiting is {hours_on_Trisolaris} hours {minutes_on_Trisolaris} minutes and {seconds_on_Trisolaris} seconds.")
