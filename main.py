import argparse
from unslam import unslam


def main():
    parser = argparse.ArgumentParser(
        description="Filter SLAM topics and TF frames from a rosbag."
    )
    parser.add_argument("bagfile", help="Path to the input bag file")
    parser.add_argument(
        "--output",
        default="out",
        help="Path for the output bag file (default: %(default)r)"
    )
    parser.add_argument(
        "--filter",
        default=r"\/map$|\/slam_toolbox.*",
        help="Regex to exclude topics (default: %(default)r)",
    )
    parser.add_argument(
        "--parent-frame",
        default="map",
        help="Source TF frame to filter out (default: %(default)s)",
    )
    parser.add_argument(
        "--child-frame",
        default="vision",
        help="Child TF frame to filter out (default: %(default)s)",
    )
    parser.add_argument(
        "--version",
        default="ros2_humble",
        help="ROS2 typestore version string (default: %(default)s)",
    )
    args = parser.parse_args()

    unslam(
        bagfile=args.bagfile,
        output=args.output,
        filter=args.filter,
        parent_frame=args.parent_frame,
        child_frame=args.child_frame,
        version=args.version,
    )


if __name__ == "__main__":
    main()
