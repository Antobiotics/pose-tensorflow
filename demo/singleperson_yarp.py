import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../")

from scipy.misc import imread

from config import load_config
from nnet import predict
from util import visualize
from dataset.pose_dataset import data_to_input
import matplotlib.pyplot as plt
from util.timer import Timer
import cv2
import yarp
import argparse
import numpy as np

def read_yarp_image(inport):

    # Create numpy array to receive the image and the YARP image wrapped around it
    img_array = np.ones((240, 320, 3), dtype=np.uint8)
    yarp_image = yarp.ImageRgb()
    yarp_image.resize(320, 240)
    yarp_image.setExternal(img_array, img_array.shape[1], img_array.shape[0])
    # Read the data from the port into the image
    inport.read(yarp_image)
    # display the image that has been read
    #matplotlib.pylab.imshow(img_array)

    return img_array, yarp_image


def draw_links(im, pose, threshold=0.5):

    num_joints = pose.shape[0]
    pose_conf = pose[:, 2]
    pose = pose.astype(int)
    im = im.copy()
    for jnt_idx in range(6, 11):
        if pose_conf[jnt_idx] >= threshold and pose_conf[jnt_idx+1] >= threshold:
            pt1 = (pose[jnt_idx, 0], pose[jnt_idx, 1])
            pt2 = (pose[jnt_idx+1, 0], pose[jnt_idx+1, 1])
            cv2.line(im, pt1, pt2, color=(255, 0, 0), thickness=3)
    pt1 = (pose[12, 0], pose[12, 1])
    pt2 = (pose[13, 0], pose[13, 1])
    cv2.line(im, pt1, pt2, color=(0, 0, 255), thickness=3)
    return im


def im_process(sess, cfg, inputs, outputs, image, fig="preview"):

    image_batch = data_to_input(image)

    image = image[:, :, (2, 1, 0)]
    timer = Timer()
    timer.tic()
    # Compute prediction with the CNN
    outputs_np = sess.run(outputs, feed_dict={inputs: image_batch})
    scmap, locref = predict.extract_cnn_output(outputs_np, cfg)

    # Extract maximum scoring location from the heatmap, assume 1 person
    pose = predict.argmax_pose_predict(scmap, locref, cfg.stride)

    timer.toc()
    print('Detection took {:.3f}s'.format(timer.total_time))

    # Visualise
    # visualize.show_heatmaps(cfg, image, scmap, pose)
    # plt.figure()
    # plt.imshow(visualize.visualize_joints(image, pose))
    CONF_THRES = 0.8

    image = draw_links(image, pose)
    cv2.imshow(fig, visualize.visualize_joints(image, pose, threshold=CONF_THRES))


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Pose Estimation demo')
    parser.add_argument('--src', dest='src_port', help='Yarp port of source images',
                        default='/icub/camcalib/left/out')
    parser.add_argument('--des', dest='des_port', help='Yarp port of receiver',
                        default='/leftCam')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    cfg = load_config("demo/pose_cfg.yaml")

    args = parse_args()

    # Initialise YARP
    yarp.Network.init()
    # Create a port and connect it to the iCub simulator virtual camera
    input_port = yarp.Port()
    input_port.open(args.des_port)
    port_connected = True
    if not yarp.Network.connect(args.src_port, args.des_port):
        print('Cannot connect to camera port!')
        port_connected = False

    # Load and setup CNN part detector
    sess, inputs, outputs = predict.setup_pose_prediction(cfg)

    cv2.namedWindow(args.des_port)

    while port_connected:
        im_arr, _ = read_yarp_image(inport=input_port)
        im_process(sess=sess, cfg=cfg, inputs=inputs, outputs=outputs, image=im_arr, fig=args.des_port)
        key = cv2.waitKey(20)
        if key == 27:
            break

    input_port.close()
    cv2.destroyAllWindows()