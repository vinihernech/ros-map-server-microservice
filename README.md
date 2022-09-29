# ros-map-server-microservice

## About 
Microservice that provides a map saved on an NFS server for the intelligent space environment and the ROS environment.

### Programmable Intelligent Space (PIS)
This microservice uses an RPC to send the map image and metadata to the user when requested. The RPC, or Remote Procedure Call, provided here acts as a remote server that binds a specific function to a topic. 

### ROS
The second functionality of this microservice provides a [map_server](http://wiki.ros.org/map_server) for the ROS environment. The map_server provides a node, which offers map data as a ROS Service. The map_server can be used in other packages like [AMCL](http://wiki.ros.org/amcl) and [move_base](http://wiki.ros.org/move_base).

## Dependences 
[ROS-master](http://wiki.ros.org/Master): Provides naming and registration services to the rest of the nodes in the ROS system.

# Usage 

## RPCs:
| Name | ⇒ Input | Output  ⇒ | Description |
| ---- | ------- | --------- | ----------- |
| IsRosMapServer | :incoming_envelope: **topic:** `IsRosMapServer.{robot_id}.MapRequest` <br> :gem: **schema:** [MapRequest](https://github.com/vinihernech/ros-map-server-microsservice/blob/main/src/conf/maprequest.proto)| :incoming_envelope: **topic:**  `IsRosMapServer.{robot_id}.MapRequest` <br> :gem: **schema:** [MapRequestReply](https://github.com/vinihernech/ros-map-server-microsservice/blob/main/src/conf/maprequest.proto)| Receives a map request and sends the map image and its respective metadata.|

## Configuration :gear:

The behavior of the microservice can be customized by passing a YAML configuration file.

An example configuration file can be found in [`etc/config/config.yaml`](https://github.com/vinihernech/ros-map-server-microsservice/blob/main/etc/config/config.yaml) and [`etc/k8s/hector_config/deployment.yaml`](https://github.com/vinihernech/ros-map-server-microsservice/blob/main/etc/k8s/deployment.yaml).

## Kubernetes <img alt="k8s" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/kubernetes/kubernetes.png" />

In a simplified way, a service on the Intelligent Space is a python (or cpp, etc.) application running in a docker container which is orchestrated on a kubernetes platform across a set of hosts.

Make sure you have [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) installed and the right `~/.kube/config` file to be able to interact with the cluster.

Deploy the stream application:

```bash
kubectl apply -f etc/k8s/deployment.yaml
```

The `.yaml` file describes a deployment. A deployment is a way to run our application and guarantee that an N number of replicas will be running. See more about [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

## Example
An example of use is shown in [examples/client.py](https://github.com/vinihernech/ros-map-server-microsservice/blob/main/examples/client.py).
