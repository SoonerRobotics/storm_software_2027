from robotpy_apriltag import AprilTagDetector, AprilTagDetection, AprilTagPoseEstimator
import numpy as np
from scipy.spatial.transform import Rotation as R   
import cv2

class AprilTagProcessing():
    def __init__(self):
        self.detector = AprilTagDetector()

        d_config = AprilTagDetector.Config()
        d_config.decodeSharpening = 0.25
        d_config.refineEdges = 1
        d_config.quadDecimate = 1.0
        d_config.numThreads = 1
        d_config.debug = 0
        d_config.quadSigma = 0.0

        self.detector.setConfig(d_config)
        self.detector.addFamily('tag36h11')

        camera_params = [950.9005621272711, 954.5085929681891, 660.8981732639802, 370.78404998542726]
        tag_size = 0.0635

        estimate_config = AprilTagPoseEstimator.Config(tag_size, *camera_params)
        self.estimator = AprilTagPoseEstimator(estimate_config)

    def pose_estimation(self, frame):
        tags_ID = []
        poses_x = [0] * 12 # Empty space for poses
        poses_z = [0] * 12
        poses_rot_y = [0] * 12  #y is the only rotation we care about
        
        results = self.detector.detect(frame)
        for idx, result in enumerate(results):
            pose = self.estimator.estimate(result)

            # x is horizontal z is depth
            poses_x[idx] = pose.X() * 39.37008 # Convert to inches
            poses_z[idx] = pose.Z() * 39.37008 / 1.2 # The 1.2 is a jerry rig, should probably fix later

            poses_rot_y[idx] = -pose.rotation().y_degrees # negative because I want rotation to be clockwise positive

            tags_ID.append(result.getId())
