# The following script receives a stream of average (time-between-messages), computed by
# avg.py using entries of the redis db, the diffs from the previous
# 120 seconds over stdin, and emits a JSON string to stdout if the average time
# between messages is greater than the specified threshold. When the
# undesired phase ends, the duration when the average meeting events booked falls below the threshold 
# the program sends an JSON ['ending'] message. This
# will continue indefinitely until the program is terminated. The bookending
# notifications helps to track the of desired vs undesired booking phase.
# from README: the idea here is that booking of events reflects the frequency of people organizing an event,
# tells about what is the frequency and the urgency. As we discussed in class,
# stories require change, and a lot of meeting bookings reflects a lot of
# transfer of communication across platforms and involves varied people. 
# so here I consider when the rate of events booking changes and steps over the 
# certain threshold (e.g. the average time between events has dropped to a small
# number, or the events are happening very frequently).
from sys import stdin, stdout
from datetime import datetime
import json
# I am using the following as a measure for different consideration. The explanation for each of the
# variable is as follows.
# THRESHOLD has been explained above. I am using the time span between two booking in a single state crosses 20 minutes. But
# this is original pin-point, which I increase or devrease by 10, i.e., THRESHOLD +- 10. So explaining the logic as put across in the 
# readme is that, posi_count keeps track of the number of events that has occurred when the rate is above THRESHOLD, to simplify, if the
# system receives 30 consecutive events, the system redefines its THRESHOLD and increses it's value by 10. The negi_count keep track of
# the reverse process, i.e., when the system is below the THRESHOLD and it receives 30 consecutive events, it decreses the 
# THRESHOLD. After each change, the value of each of the counter is set back to original values
# defining the THRESHOLD and other variables
THRESHOLD = 20
posi_count = 0
negi_count = 30

# This is a variable that will keep track of whether the system is currently
# in an undesired phase or not. This is the main mechanism for preventing
# duplicate messages during a period of out of desired phase.
check_detect= False
while True:
    # Read in the input from stdin, which is a JSON[key]='rate' containing
    # the average for the values in the DB(which have been there for < 120 seconds
    line = stdin.readline()
    avg = json.loads(line).get('rate')
    # Now, if we find that the current average is greater than the threshold,
    # we are enjoying favourable conditon.
    if avg > THRESHOLD:
        # incrementing the count for the purpose explained above.
        posi_count += 1
        if check_detect:
            # reverse the boolean, to avoid getting the same message
            # in case of a repeat reading
            check_detect = False
            # Printing JSON with the message. The JSON content:
            # the rate
            # current time: for logging
            print(json.dumps({'check_detect': False,
                              'message': 'The booking rate on meetup is as per expectation and the team is happy right now.',
                              'rate': avg,
                              'timestamp': str(datetime.now()),
                             }))
            # make sure to flush the stdout to prevent Python from
            # keeping a buffer.
            stdout.flush()
            # checking the posi_count and increasing the threshold if required and setting back to zero
        if posi_count > 30:
            THRESHOLD += 10
            posi_count = 0
    # If the average reading out of the desired zone        
    else:
        # decrementing the negative count
        negi_count -= 1
        if not check_detect:
            # This is executes when the previous phase was desired phase. It
            # allows us to identify when the system is experiencing out of comfort zone, and to
            # prevent us from sending messages when nothing is happening.
            check_detect = True 
            # Print a JSON string to stdout when the system is experiencing the undesired rate,
            # the current timestamp
            print(json.dumps({'check_detect': True,
                              'message': 'The meeting booking rate is low and below the desired rate.',
                              'rate': avg,
                              'timestamp': str(datetime.now()),
                             }))
            # Again, prevent Python from buffering the stdout.
            stdout.flush()
        if negi_count < 0:
            THRESHOLD -= 10
            negi_count = 30
