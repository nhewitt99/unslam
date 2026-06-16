import re
from rosbags.rosbag2 import Reader, Writer
from rosbags.typesys import Stores, get_typestore
import rosbags.typesys.stores.ros2_dashing as dashing

TFMessage = dashing.tf2_msgs__msg__TFMessage

def main():
    bagfile = "bag/20251218-1402"
    outfile = "out"
    filter = r"/map$"
    filter_regex = re.compile(filter)
    frame_1 = "map"
    frame_2 = "vision"
    version = Stores('ros2_humble')
    # version = cast(Stores, 'ros2_humble')
    # print(version)
    # version = Stores.ROS2_JAZZY
    # print(version)
    typestore = get_typestore(version)

    def check_tf(tf : TFMessage):
        # print(tf.header.frame_id)
        return (tf.header.frame_id == frame_1 and tf.child_frame_id == frame_2)

    total = 0

    with Reader(bagfile) as reader, Writer(outfile, version=8) as writer:
        connections = [c for c in reader.connections if filter_regex.match(c.topic) is None]
        for connection, timestamp, rawdata in reader.messages(connections=connections):
            msg = typestore.deserialize_cdr(rawdata, connection.msgtype)
            if type(msg) == TFMessage: #stores.ros2_dashing.tf2_msgs__msg__TFMessage:
                oldlen = len(msg.transforms)
                msg.transforms = [tf for tf in msg.transforms if not check_tf(tf)]
                rawdata = typestore.serialize_cdr(msg, connection.msgtype)
                newlen = len(msg.transforms)
                total += (oldlen - newlen)

            try:
                # writer.write(connection, timestamp, rawdata)
                pass
            except Exception as e:
                print(e)
    print(total)


if __name__=="__main__":
    main()