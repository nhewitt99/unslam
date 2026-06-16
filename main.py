import re
from rosbags.rosbag2 import Reader, Writer, StoragePlugin
from rosbags.typesys import Stores, get_typestore, TypesysError
import rosbags.typesys.stores.ros2_dashing as dashing
# from typing import cast
from rosbags.interfaces import ConnectionExtRosbag2

TFMessage = dashing.tf2_msgs__msg__TFMessage

def main():
    bagfile = "bag/20251218-1402"
    outfile = "out"
    filter = r"\/map$|\/slam_toolbox.*"
    filter_regex = re.compile(filter)
    frame_1 = "map"
    frame_2 = "vision"
    version = Stores('ros2_humble')
    storage = StoragePlugin.MCAP
    typestore = get_typestore(version)

    def check_tf(tf : TFMessage):
        # print(tf.header.frame_id)
        return (tf.header.frame_id == frame_1 and tf.child_frame_id == frame_2)

    with Reader(bagfile) as reader, Writer(outfile, version=8, storage_plugin=storage) as writer:
        # Filter out topics
        connections = [c for c in reader.connections if filter_regex.match(c.topic) is None]

        # Set up topics in the output file
        conn_map = {}
        for connection in connections:
            try:
                conn_map[connection.id] = writer.add_connection(
                    connection.topic,
                    connection.msgtype,
                    typestore=typestore,
                    serialization_format=connection.ext.serialization_format,
                    offered_qos_profiles=connection.ext.offered_qos_profiles,
                )
            except TypesysError as e:
                print(e)

        # Iterate through all messages in the input file
        for connection, timestamp, rawdata in reader.messages(connections=connections):
            msg = typestore.deserialize_cdr(rawdata, connection.msgtype)
            if type(msg) == TFMessage:
                msg.transforms = [tf for tf in msg.transforms if not check_tf(tf)]
                rawdata = typestore.serialize_cdr(msg, connection.msgtype)

            try:
                writer.write(conn_map[connection.id], timestamp, rawdata)
            except KeyError:
                pass  # These messages would have given a prior warning for unknown type
            except Exception as e:
                print(e)


if __name__=="__main__":
    main()