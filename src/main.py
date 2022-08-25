from math import cos, sin, pi
import yaml
from is_wire.core import Channel, Message, Subscription, StatusCode, Status, Logger
from is_wire.rpc import ServiceProvider, LogInterceptor
from google.protobuf.empty_pb2 import Empty
from maprequest_pb2 import MapRequest, MapRequestReply
from streamChannel import StreamChannel

if __name__ == '__main__':

   try:
      with open(r'../etc/config.yaml') as file:
         config = yaml.load(file, Loader=yaml.FullLoader)
   except:
      print('Unable to load config file')

   log = Logger(name='Map')
   try:
      channel = Channel(config['broker_uri'])  
      log.info("connected to broker")
   except:
      log.info("Can't connect to broker")

   provider = ServiceProvider(channel)
   logging = LogInterceptor()
   provider.add_interceptor(logging)
   robot_id = config['robot_id']
   topic = "IsRosMapping.{}.MapRequest".format(robot_id)
   subscription = Subscription(channel) 


   provider.delegate(
   topic = topic,
   function = get_is_points,
   request_type = MapRequest,
   reply_type = MapRequestReply)

   provider.run()


