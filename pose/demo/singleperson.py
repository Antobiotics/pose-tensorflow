
from scipy.misc import imread

from pose.config import load_config
from pose.nnet import predict
from pose.util import visualize
from pose.dataset.pose_dataset import data_to_input

import matplotlib.pyplot as plt

cfg = load_config("pose/demo/pose_cfg.yaml")

# Load and setup CNN part detector
sess, inputs, outputs = predict.setup_pose_prediction(cfg)

# Read image from file
file_name = "/Volumes/bobby//tag_walk/tag_walk//data/outputs//paperdoll_images/38163.jpg"
image = imread(file_name, mode='RGB')

image_batch = data_to_input(image)

# Compute prediction with the CNN
outputs_np = sess.run(outputs, feed_dict={inputs: image_batch})
scmap, locref = predict.extract_cnn_output(outputs_np, cfg)

# Extract maximum scoring location from the heatmap, assume 1 person
pose = predict.argmax_pose_predict(scmap, locref, cfg.stride)

# Visualise
visualize.show_heatmaps(cfg, image, scmap, pose)
plt.show()
