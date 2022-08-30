import yaml
from is_msgs.robot_pb2 import RobotTaskRequest, PathRequest, RobotControllerProgress
from is_msgs.common_pb2 import Position, Pose, Orientation
from is_msgs.camera_pb2 import FrameTransformation,FrameTransformations
from is_wire.core import Channel, Message, Logger,Status,StatusCode, Subscription
from is_wire.rpc import ServiceProvider, LogInterceptor
from google.protobuf.empty_pb2 import Empty
from maprequest_pb2 import MapRequest, MapRequestReply
import socket
from streamChannel import StreamChannel



def path_task_robot(id, config):
    cons_channel = Channel(config['broker_uri'])
    cons_subscription = Subscription(cons_channel)
    topic = "IsRosMapServer.{}.MapRequest".format(config['robot_id'])
    task = MapRequest()
    task.id = id
    message = Message(content=task,reply_to=cons_subscription)
    cons_channel.publish(message,topic=topic)
    try:
        reply = cons_channel.consume(timeout=3.0)
        struct = reply.unpack(MapRequestReply)
        print('RPC Status:', reply.status, '\nReply:', struct)
    except socket.timeout:
        print('No reply :(')
   
    



if __name__ == '__main__':
    try:
        with open(r'../etc/config.yaml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
    except:
            print('Unable to load config file')

    path_task_robot(0,config)

   


