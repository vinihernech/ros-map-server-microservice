import yaml
from is_wire.core import Channel, Message, Subscription
from maprequest_pb2 import MapRequest, MapRequestReply
import socket
import numpy as np
from is_msgs.image_pb2 import Image
import cv2

def save_map_img(map_file):
    map_img_cod = map_file.map.data
    map_img_dec = np.frombuffer(map_img_cod, dtype=np.uint8)
    map_img_res = np.reshape(map_img_dec, newshape=(512,512))
    cv2.imwrite('my_map.pgm', map_img_res)
    
 

def build_yaml_file(map_file):
    map_file = [{'image': map_file.map_dir},
    {'resolution': map_file.map_resolution},{'origin': [map_file.origin.position.x, map_file.origin.position.y,map_file.origin.orientation.yaw]},
    {'occupied_thresh': map_file.occupied_thresh}, {'free_thresh':map_file.free_thresh} ]
    with open(r'my_map.yaml', 'w') as file:
        documents = yaml.dump(map_file, file)

def get_map(id, config):
    cons_channel = Channel(config['broker_uri'])
    cons_subscription = Subscription(cons_channel)
    topic = "IsRosMapServer.{}.MapRequest".format(config['map_id'])
    task = MapRequest()
    task.id = id
    message = Message(content=task,reply_to=cons_subscription)
    cons_channel.publish(message,topic=topic)
    try:
        reply = cons_channel.consume(timeout=3.0)
        map_file = reply.unpack(MapRequestReply)
        build_yaml_file(map_file)
        save_map_img(map_file)
        print('RPC Status:', reply.status)
    except socket.timeout:
        print('No reply :(')
   

if __name__ == '__main__':
    try:
        with open(r'../etc/config/config.yaml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
    except:
            print('Unable to load config file')
    
    get_map(0,config)

   


