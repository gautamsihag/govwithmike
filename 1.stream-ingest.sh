# This is the script that starts the meetup stream ingestion process.

# meet2.py is connecting to the meetup api and ingesting the flow,
# outputing timestamps to stdout; diff.py is taking those timestamps and outputting the time
# differences between consecutive messages to stdout; redis-insert.py is just
# taking those values and putting them into a redis db on port 6379 with an
# arbitrary key.

python meet2.py | python diff.py | python redis-insert.py