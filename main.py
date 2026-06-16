import argparse
from unslam import unslam


def main():
    parser = argparse.ArgumentParser(description="Filter SLAM topics and TF frames from a rosbag.")
    parser.add_argument("bagfile", help="Path to the input bag file")
    parser.add_argument("output", help="Path for the output bag file")
    parser.add_argument("--filter", default=r"\/map$|\/slam_toolbox.*",
                        help="Regex to exclude topics (default: %(default)r)")
    parser.add_argument("--parent-frame", default="map",
                        help="Source TF frame to filter out (default: %(default)s)")
    parser.add_argument("--child-frame", default="vision",
                        help="Child TF frame to filter out (default: %(default)s)")
    parser.add_argument("--version", default="ros2_humble",
                        help="ROS2 typestore version string (default: %(default)s)")
    args = parser.parse_args()

    unslam(
        bagfile_=args.bagfile,
        output_=args.output,
        filter_=args.filter,
        parent_frame_=args.parent_frame,
        child_frame_=args.child_frame,
        version_=args.version,
    )


if __name__ == "__main__":
    main()