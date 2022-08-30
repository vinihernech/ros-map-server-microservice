from math import cos, sin, pi
import yaml
from is_wire.core import Channel, Message, Subscription, StatusCode, Status, Logger
from is_wire.rpc import ServiceProvider, LogInterceptor
from maprequest_pb2 import MapRequest, MapRequestReply
from streamChannel import StreamChannel
import cv2
import argparse


def send_map(message, ctx):
   map_id = message.id
   try:
      with open(r'{}.yaml'.format(map_name)) as file:
         map_config = yaml.load(file, Loader=yaml.FullLoader)
   except:
      print('Unable to load config file')
   map_image = cv2.imread("{}.pgm".format(map_name),-1)
   map_image_data = map_image.tobytes()
   map_msg = MapRequestReply()
   map_msg.map.data = map_image_data
   map_msg.map_dir = map_config['image']
   map_msg.map_resolution = map_config['resolution']
   map_msg.origin.position.x = map_config['origin'][0]
   map_msg.origin.position.y = map_config['origin'][1]
   map_msg.origin.position.z = 0
   map_msg.origin.orientation.yaw = map_config['origin'][2]
   map_msg.negate = map_config['negate']
   map_msg.occupied_thresh = map_config['occupied_thresh']
   map_msg.free_thresh = map_config['free_thresh']
   print(map_msg)
   return map_msg
   
map_name = 'my_map0'



if __name__ == '__main__':

   try:
      with open(r'config.yaml') as file:
         config = yaml.load(file, Loader=yaml.FullLoader)
   except:
      print('Unable to load config file')

   log = Logger(name='Map')
   try:
      channel = Channel(config['broker_uri'])  
      log.info("connected to broker")
   except:
      log.info("Can't connect to broker")

   parser = argparse.ArgumentParser()
   parser.add_argument('map_name', type= str, default='my_map0')
   args = parser.parse_args()
   provider = ServiceProvider(channel)
   logging = LogInterceptor()
   provider.add_interceptor(logging)
   robot_id = config['robot_id']
   topic = "IsRosMapServer.{}.MapRequest".format(robot_id)
   subscription = Subscription(channel) 


   map_name = args.map_name


   provider.delegate(
   topic = topic,
   function = send_map,
   request_type = MapRequest,
   reply_type = MapRequestReply)

   provider.run()


