import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

def connect_redis():
  try:

    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8.  This is client specific.
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
  except Exception as e:
    print(e)
    
  return r
  
def hello_redis():
    """Example Hello Redis Program"""
    
    # step 3: create the Redis Connection object
    try:
    
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    
        # step 4: Set the hello message in Redis 
        #r.set("msg:hello", "Hello Redis!!!")

        # step 5: Retrieve the hello message from Redis
        msg = r.get("msg:hello")
        print(msg)        
    
    except Exception as e:
        print(e)


if __name__ == '__main__':
  print "Connect to Redis"
  rDb = connect_redis()

  #print "Set Petra"  
  #rDb.set("msg:Petra", "Kilroy")
  
  print "After Petra is set"
  print(rDb.get("msg:Petra"))
  
