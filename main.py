import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import penalty


# ORGANIZE DATASET

# Date first:
# Load the CSV file into a pandas DataFrame
lambda_results = pd.read_csv('~/Desktop/lambda_results.csv')

# Extract the day of the week from the 'dataframe' column
lambda_results['day_of_week'] = lambda_results['dataframe'].apply(lambda x: x.split()[0])

# Define the order of the days of the week
days_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Create an ordered categorical variable for the days of the week
lambda_results['day_of_week'] = pd.Categorical(lambda_results['day_of_week'], categories=days_order, ordered=True)

# Sort the DataFrame by the day of the week
lambda_results.sort_values(by='day_of_week', inplace=True)

# Reset the index of the DataFrame
lambda_results.reset_index(drop=True, inplace=True)

# Time second:
# Extract the time from the 'dataframe' column
lambda_results['time'] = lambda_results['dataframe'].apply(lambda x: x.split()[1] + ' ' + x.split()[2])

# Convert the time to 24-hour format
lambda_results['time_24h'] = pd.to_datetime(lambda_results['time'], format='%I:%M %p').dt.hour.astype(int)

# Sort the DataFrame by the day of the week and the time
lambda_results.sort_values(by=['day_of_week', 'time_24h'], inplace=True)

# Reset the index of the DataFrame
lambda_results.reset_index(drop=True, inplace=True)

print("What day would you like to work out? ", end="")
while True:
    user_day = input().strip().title()
    if user_day in days_order:
        lambda_results = lambda_results[lambda_results['day_of_week'] == user_day]
        break
    else:
        print("Please enter a valid day (e.g. 'Monday'): ", end="")


# GATHER/PROCESS DATA

events_list = penalty.gather_events()
values_list = penalty.gather_penalty_values(events_list)


# Define the Poisson probability function
def poisson_prob(lambda_):
    return np.exp(0 - lambda_)


# Define the penalty function
def penalty_function(lambda_):
    return values_list[lambda_]


# Calculate and store normalized poisson values
lambda_results['poisson_normalized'] = lambda_results['estimated_mean'].apply(
    lambda x: (x - lambda_results['estimated_mean'].min()) / (
            lambda_results['estimated_mean'].max() - lambda_results['estimated_mean'].min()))
lambda_results['poisson_normalized'] = lambda_results.apply(lambda row: poisson_prob(row['poisson_normalized']), axis=1)

# Calculate and store normalized penalty values
lambda_results['penalty'] = lambda_results.apply(lambda row: penalty_function(row['time_24h']), axis=1)
if lambda_results['penalty'].max() > 0:
    lambda_results['penalty_normalized'] = lambda_results['penalty'].apply(
        lambda x: 1 - (x - lambda_results['penalty'].min()) / (
                lambda_results['penalty'].max() - lambda_results['penalty'].min()))
else:
    lambda_results['penalty_normalized'] = lambda_results['penalty']

# Calculate the linear combination of the Poisson probability and the penalty
lambda_results['linear_combination'] = lambda_results.apply(
    lambda row: .5 * row['poisson_normalized'] + .5 * row['penalty_normalized'], axis=1)


# GATHER USER INPUT

open_hour = lambda_results['time_24h'].min()
close_hour = lambda_results['time_24h'].max() + 1

print("When is the earliest you are willing to work out? ", end="")
while True:
    earliest_workout_hour = input().strip()
    if earliest_workout_hour.isdigit() and open_hour <= int(earliest_workout_hour) < close_hour:
        earliest_workout_hour = int(earliest_workout_hour)
        break
    else:
        print(f"Please enter a number between {open_hour} and {close_hour - 1}: ", end="")

print("When is the latest you are willing to work out until? ", end="")
while True:
    latest_workout_hour = input().strip()
    if latest_workout_hour.isdigit() and earliest_workout_hour < int(latest_workout_hour) <= close_hour:
        latest_workout_hour = int(latest_workout_hour)
        break
    else:
        print(f"Please enter a number between {earliest_workout_hour + 1} and {close_hour}: ", end="")

print("How many hours will your workout be? ", end="")
while True:
    workout_length = input().strip()
    if workout_length.isdigit() and 1 <= int(workout_length) <= latest_workout_hour - earliest_workout_hour:
        workout_length = int(workout_length)
        break
    else:
        print(f"Please enter a number between 1 and {latest_workout_hour - earliest_workout_hour}: ", end="")


# CALCULATE/OUTPUT RESULTS

# Find best time slot for the gym
lambda_results_filtered = lambda_results.loc[(lambda_results['time_24h'] >= earliest_workout_hour) &
                                             (lambda_results['time_24h'] < latest_workout_hour)]
best_time = lambda_results_filtered.loc[
    lambda_results_filtered['linear_combination'].rolling(workout_length).sum().idxmax() - (workout_length - 1)]
print("Best time:", best_time['dataframe'])

# Define colors and alpha values
line_color = '#4CAF50'
highlight_color = '#FFC107'
background_color = '#FAFAFA'
events_color = '#7FB8D8'
ecAlpha = .3

# Plot
plt.figure(figsize=(10, 6))
plt.rcParams['axes.facecolor'] = background_color
plt.plot(lambda_results['time_24h'][(lambda_results['time_24h'] >= earliest_workout_hour) & (lambda_results['time_24h'] <= latest_workout_hour)],
         lambda_results['linear_combination'][(lambda_results['time_24h'] >= earliest_workout_hour) & (lambda_results['time_24h'] <= latest_workout_hour)],
         linestyle='-', color=line_color, linewidth=1.5)
plt.title('Optimal Workout Time on ' + best_time['day_of_week'], color='black')
plt.xlabel('Hour', color='black')
plt.ylabel('Recommendation Level', color='black')
x = range(lambda_results['time_24h'].min(), lambda_results['time_24h'].max() + 2, 2)
plt.xticks(x, [f'{hour:02d}:00' for hour in x], color='black')
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1], color='black')
plt.grid(True, linestyle='--', alpha=0.5, color='black')
plt.margins(x=0)

# Highlight important time ranges
highlights = []
highlights.append(plt.axvspan(best_time['time_24h'], best_time['time_24h'] + workout_length, color=(highlight_color, .4), ec=('black', ecAlpha), label='Workout'))
plt.axvspan(lambda_results['time_24h'].min(), earliest_workout_hour, color=('lightgray', 0.8), ec=('black', ecAlpha), label = 'Too Early/Late')
plt.axvspan(latest_workout_hour, lambda_results['time_24h'].max() + 1, color=('lightgray', 0.8), ec=('black', ecAlpha))
for event in events_list:
    random_color = '#%02X%02X%02X' % (random.randint(100, 200), random.randint(150, 220), random.randint(200, 255))
    highlights.append(plt.axvspan(event['start'], event['end'], color=(random_color, .3), ec=('black', ecAlpha), label=event['name']))

# Insert legend in upper right hand corner
legend_handles = highlights
legend_labels = [handle.get_label() for handle in legend_handles]
plt.legend(legend_handles, legend_labels, loc='upper right')

plt.show()

