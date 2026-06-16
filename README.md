# unslam
Simple script to remove specific transforms from a ROS bag and filter topics.

Originally intended to remove SLAM results from recorded bag files, unslamming them.
But really you can "unslam" whatever you want: unpercept, ungps, unestimate, I won't stop you.

## Installation
```
pip install .
```

## Usage
```
unslam <your_bag_file>
```

This will create a new bag file named `out`.
Default behavior is to remove map->odom tfs and the /map topic.

Remove arbitrary topics with the `filter` argument, which specifies a regex to reject any matching topics.

Change frames with `parent-frame` and `child-frame` arguments.