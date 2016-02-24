# govwithmike
# Storytelling with streaming data HW2

Consuming event stream of meetup.com in specific the RSVP event stream to obtain infromation about a reservation.
The idea here is that booking of events reflects the frequency of people organizing an event,
tells about what is the frequency and the urgency. As we discussed in class,
stories require change, and a lot of meeting bookings reflects a lot of
transfer of communication across platforms and involves varied people. 
so here I consider when the rate of events booking changes and steps over the 
certain threshold (e.g. the average time between events has dropped to a small
number, or the events are happening very frequently).

Stream can be accessed at:  
http://stream.meetup.com/2/rsvps with the detailed documentation at:
http://www.meetup.com/meetup_api/docs/stream/2/rsvps/.

# Sample JSON format of a meetup API response

The detailed infromation for the data dictionary can be accessed at: http://www.meetup.com/meetup_api/docs/stream/2/rsvps/

# Included Files:
There are two .sh files, that means two commands to be executed simulatneoulsy: 

1. Step 1: For connecting to the RSVP meetup API, calculating the amount of time that elapsed between two events and loading these time differences into a Redis in-memory database.
2. Step 2: For calculating the average amount of time between consecutive events (using the data in the Redis database), creating an alert when the average time-between-consecutive-events crosses the specified THRESHOLD, and communicating these via Slackbot.

## Files for Step 1: 

- `1-stream-ingest.sh`
	- script to process the step 1. 
	- Before running this, make sure there is a Redis database server serving over the default port (6379)!
- `meet2.py`
	- Connects to the RSVP meetup API, and outputs the edit event messages to stdout.
- `diff.py`
	- Reads the event messages via stdin, retrieves the timestamp (Unix epoch time) and then calculates the elapsed (server) time between two events and outputs them to stdout.
- `redis-insert.py`
	- Takes the time differences and sticks them into a Redis database, each with a 120 second lifespan.

## Files for Step 2:

- `notifysystem.sh`
	- To process the step 2. Make sure to run `1-stream-ingest.sh` and avoid waiting for more than a few seconds else the threshold value tends to give out of order results.
- `avg.py`
	- This script looks at all entries in the Redis database and calculates the average of the time differences there. It outputs this average to stdout.
- `check_detect.py`
	- Reads the average values coming via stdin from `avg.py` and checks if the value is falls under the desired booking phase or tends to cross out of it.
- `pushwithslack.py`
	- This script reads the data from stdin and creates a message to be posted on Slack. It then posts that message to the Slack channel using the URL in `CONFIG_SLACK.py`.
- `CONFIG_SLACK.py`
	- You should create it yourself, or use the repository I have provided! It contain a single line for SLackbot's 
	- url =`https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`.


Please refer to [Slack's API webpage](https://api.slack.com/)--> log in--> click the button that says 'Start building custom integrations,' and follow the instructions to setup an 'Incoming Webhook.' Once that URL is set, you must insert that URL into a file called `CONFIG_SLACK.py`, which should have a single line that looks like this:

```
url = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
```

Of course, insert the URL you got through the Slack API. The online interface allows you to specify what channel you would like it to post to, what the avatar should be for that bot, and some other features like that.

## Step 1:

run the command in 1.stream-ingest.sh
```
python meet2.py | python diff.py | python redis-insert.py
```
or

```
./1.stream-ingest.py
```

## Step 2:

run the following command:

```
./notifysystem.sh
```

or the following command:

```
python avg.py | python check_detect.py | python pushwithslack.py
```
