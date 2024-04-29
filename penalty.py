import numpy as np


# Calculate penalty
def f(x, start, end, weight):
    return (pow(weight, x - (start - 2)) * (1 if x < start else 0)
            + 2 * weight * (1 if (start <= x <= end) else 0)
            + pow(2, -x + (end + 2)) * (1 if x > end else 0))


# Gather penalty values by hour based on calendar events
def gather_penalty_values(events):
    # Initialize a list to store penalty values by hour
    values = np.zeros(24)

    # Cycle through each event at each hour and add value from penalty function to values list
    for hour in range(24):
        for event in events:
            values[hour] += f(hour, event['start'], event['end'], event['weight'])

    return values


# Gather calendar events inputted by user
def gather_events():
    events = []

    print("What is your schedule like on this day?")

    # Allow user to add events until they opt to quit
    while True:

        event_name = input("Enter name of an event (or 'Q' to exit): ")
        if event_name.upper() == 'Q':
            return events

        print(f"When does '{event_name}' start? Type an hour between 0 and 23: ", end="")
        while True:
            event_start = input()
            if event_start.isdigit() and 0 <= int(event_start) <= 22:
                break
            else:
                print("Please enter an hour between 0 and 23: ", end="")

        print(f"When does '{event_name}' end? Enter hour after start time (max 23): ", end="")
        while True:
            event_end = input()
            if event_start.isdigit() and int(event_start) < int(event_end) <= 23:
                break
            else:
                print("Please enter an hour after start time (max 23): ", end="")

        print("Now you will input this event's importance in your schedule.")
        print(f"How important is the commitment '{event_name}' (1 to 5, 5 being highest priority): ", end="")
        while True:
            event_weight = input()
            if event_weight.isdigit() and 1 <= int(event_weight) <= 5:
                break
            else:
                print("Please enter a number between 1 and 5: ", end="")

        # Use data collected from user to create dictionary to add to events list
        event = {
            'name': event_name,
            'start': int(event_start),
            'end': int(event_end),
            'weight': int(event_weight)
        }
        events.append(event)
