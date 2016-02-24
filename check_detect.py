from sys import stdin, stdout
from datetime import datetime
import json

THRESHOLD = 20
posi_count = 0
negi_count = 30
check_detect= False
while True:
    line = stdin.readline()
    avg = json.loads(line).get('rate')
    
    if avg > THRESHOLD:
        posi_count += 1
        if check_detect:
            check_detect = False
            print(json.dumps({'check_detect': False,
                              'message': 'The booking rate on meetup is as per expectation and the team is happy right now.',
                              'rate': avg,
                              'timestamp': str(datetime.now()),
                             }))
            stdout.flush()
        if posi_count > 30:
            THRESHOLD += 10
            posi_count = 0
            
    else:
        negi_count -= 1
        if not check_detect:
            check_detect = True
            print(json.dumps({'check_detect': True,
                              'message': 'The meeting booking rate is low and below the desired rate.',
                              'rate': avg,
                              'timestamp': str(datetime.now()),
                             }))
            stdout.flush()
        if negi_count < 0:
            THRESHOLD -= 10
            negi_count = 30