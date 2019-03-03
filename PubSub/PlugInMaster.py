import redis
import time
import traceback

# How to publish a START:
# Start a redis client and publish START
#
# >redis-cli 
# PUBLISH startScripts START
#
# OR by another startScripts
# r.publish('startScripts', 'START')  

print "PlugInMaster.py STARTED"

def RedisCheck():
    i = 0
    try:
        r = redis.StrictRedis(host='localhost', port=6379)                          # Connect to local Redis instance
        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p.subscribe('startScripts')                                                 # Subscribe to startScripts channel
        PAUSE = True

        print("Before while PAUSE")
        while PAUSE:                                                                # Will stay in loop until START message received
            i = i+1
            print("Waiting For redisStarter...   ", i)
            message = p.get_message()                                               # Checks for message
            if message:
                command = message['data']                                           # Get data from message

                if command == b'START':                                             # Checks for START message
                    PAUSE = False                                                   # Breaks loop

            time.sleep(1)

        print("Permission to start...")

    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())
        
        
RedisCheck()