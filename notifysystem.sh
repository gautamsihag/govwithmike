# The script that launches the
# notification system. there should be redis server currently
# running, and that all of the entries contain a number of seconds between two
# subsequent events in the stream. When executed, this generates a message for Slackbot
# url specified in CONFIG_SLACK.py.
#
# avg.py takes all of those redis entries, calculates the average, and dumps it
# out of stdout, estimating the beta parameter in an exponential
# distribution check_detect.py takes those averages from stdin and looks for desired
# value phase, based on the CDF of an exponential distribution 
# When the value falls below the threshold, a
# JSON string is generated containing information about that event and output to
# stdout. That JSON string is read into puchwithslack.py, which loads the incoming
# messages url hook from CONFIG_SLACK.py and posts it to the Slack channel
# associated with it.

python avg.py | python check_detect.py | python pushwithslack.py