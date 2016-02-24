# The python script listens over stdin for check_detect JSON messages from
# check-detect.py, converts them into a message and broadcasts to a
# Slack channel. When an undesired period begins, a message is sent with an
# alert and the current average rate. The time recorded, so that when the 
# desired period starts or is regained, the duration of the previous span of time is sent with the
# message.
#
# The webhook URL is stored in tha variable 'url' in CONFIG_SLACK.py
from sys import stdin, stdout, exit
import requests
import json
from datetime import datetime

# import the `url` variable from the CONFIG_SLACK.py file,

try:
    from CONFIG_SLACK import url
except ImportError:
    # Abort this Python process with exit code 1
    # In the case of a missing 'url', the program encounters issues either because the file is not existing
    # or the webhook url to the correct variable name (`url`) is missing.
    print ("issue with the config file or the variable url")
    exit(1)
# Repeat the following process indefinitely; listen to stdin for new out of order
# messages and when it detects on
# send it to the Slack channel specified in CONFIG_SLACK.py.
while True:
    # Reading the JSON format message from stdin.
    line = stdin.readline()
    # decoding the JSON strings to access the keys
    bot = json.loads(line)
    # 'check_detect' =True, for when the out of order period begins and
    # 'false' if it is the end.
    if bot.get('check_detect'):
        # Logging the time code from the message as the start of the non-desired
        # phase and using the same to determine the length of the un-desired
        # period lasted. And decoding, since
        # it is in a string format when in JSON 
        #format: YYYY-MM-DD HH:MM:SS.ffffff
        begin = datetime.strptime(bot.get('timestamp'), '%Y-%m-%d %H:%M:%S.%f')

        
        bot_text = ('Are You there. Take a look {m}. On average, people are organizing an event every '
                      '{t} seconds.').format(m=bot.get('message'),
                                             t=round(float(bot.get('rate')), 2))
    # when check_detect = True, when the program exhibits out of normal behaviour
    else:
        # Decoding the time stamp of the message
        end = datetime.strptime(bot.get('timestamp'), '%Y-%m-%d %H:%M:%S.%f')
        # estimate the duration of the out of desired period by:
        # timestamp (current message) - timestamp(beginning ofthe desired phase)
        # round of it to the nearest second.
        duration = (end - begin).total_seconds()
        duration_est = int(round(duration))
        # the string to output through Slack
        bot_text = ('For you to take a note : {m} That below expectation period lasted about '
                      '{d} seconds.').format(m=bot.get('message'),
    
    # the following is the argument, the content of
    # the message.
    # The Slack API specification: data to be encoded as a JSON string in the body
    # of the post request.
    data = {'text': bot_text}
    r = requests.post(url, json=data)
    # to check the post went through. The status
    # code is 200 (OK), falling back to printing to stdout.
    if r.status_code != 200:
        print('The following message could not be posted to Slack:\n' + bot_text + '\n')
        stdout.flush()