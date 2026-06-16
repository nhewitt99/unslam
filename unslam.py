import re
from rosbags.rosbag2 import Reader, Writer, StoragePlugin
from rosbags.typesys import Stores, get_typestore, TypesysError
import rosbags.typesys.stores.ros2_dashing as dashing

TFMessage = dashing.tf2_msgs__msg__TFMessage


def unslam(
    bagfile_: str,
    output_: str,
    filter_: str = r"\/map$|\/slam_toolbox.*",
    parent_frame_: str = "map",
    child_frame_: str = "vision",
    version_: str = "ros2_humble",
):
    filter_regex = re.compile(filter_)
    store = Stores(version_)
    storage = StoragePlugin.MCAP
    typestore = get_typestore(store)

    def check_tf(tf: TFMessage):
        return tf.header.frame_id == parent_frame_ and tf.child_frame_id == child_frame_

    with Reader(bagfile_) as reader, Writer(output_, version=8, storage_plugin=storage) as writer:
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
