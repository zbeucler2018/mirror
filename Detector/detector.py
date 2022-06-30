#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, copy, sys

from pathlib import Path

import cv2 as cv
import numpy as np
import mediapipe as mp

from .tools import *

from .keypoint_classifier import KeyPointClassifier



class Camera:
    def __init__(self, device, height, width):
        self.device = device
        self.height = height
        self.width = width
        self.cam = None
    
    def set_up_camera(self):
        cap = cv.VideoCapture(self.device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cam = cap

    def read_frame(self):
        ret, frame = self.cam.read()
        if not ret:
            return False
        else:
            return frame

    def release(self):
        self.cam.release()


class Detector:
    def __init__(self, min_gest_conf, min_hand_conf, show_window, cam_device=0, cam_width=960, cam_height=540):
        self.min_gest_conf = min_gest_conf
        self.min_hand_conf = min_hand_conf
        self.show_window = show_window
        self.hands_model = self._load_mp_hands_model(True, 1)
        self.cam_device = cam_device
        self.cam_width = cam_width
        self.cam_height = cam_height
        self.camera = Camera(self.cam_device, self.cam_height, self.cam_width)
        self.labels = self._load_tf_labels()
        self.tf_lite_model = self._load_tf_lite_model()


    def _load_mp_hands_model(self, static_mode, num_hands):
        try:
            mp_hands = mp.solutions.hands
            hands_model = mp_hands.Hands(
                static_image_mode=static_mode,
                max_num_hands=num_hands,
                min_detection_confidence=self.min_hand_conf,
                min_tracking_confidence=0.5
            )
            print("[I] Loaded Hands model")
            return hands_model
        except Exception as e:
            print("[E] Falied to load hands model")
            print(e)
            sys.exit()

    def _load_tf_labels(self):
        try:
            with open(str(Path().absolute())+'/Detector/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
                keypoint_classifier_labels = csv.reader(f)
                keypoint_classifier_labels = [ row[0] for row in keypoint_classifier_labels ]
            print("[I] Loaded labels")
            return keypoint_classifier_labels
        except Exception as e:
            print("[E] Falied to load labels")
            print(e)
            sys.exit()


    def _load_tf_lite_model(self):
        try:
            print("[I] Loaded tf lite model")
            return KeyPointClassifier()
        except Exception as e:
            print("[E] Failed to load tf lite model")
            print(e)
            sys.exit()



    def run_all(self):
        # set up camera
        self.camera.set_up_camera()
        # Calculate FPS
        fpsCalc = CvFpsCalc(buffer_len=10)
        # get current frame
        frame = self.camera.read_frame()
        
        while frame is not False:
            # stop detecting if ESC is pressed
            key = cv.waitKey(10)
            if key == 27:  # ESC
                break

            # Modify current frame to fit mp hands model
            frame = cv.flip(frame, 1)
            debug_image = copy.deepcopy(frame)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            # get results from hands model
            frame.flags.writeable = False
            results = self.hands_model.process(frame) # use mediapipe to detect
            frame.flags.writeable = True

            # Run through detections in current frame
            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:

                    # get coordinates of all landmarks
                    landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                    # Conversion from relative coordinates to normalized coordinates
                    pre_processed_landmark_list = pre_process_landmark(landmark_list)

                    # detect gesture in current frame
                    hand_sign_id, result_confidence = self.tf_lite_model(pre_processed_landmark_list)

                    # draw on image
                    brect = calc_bounding_rect(debug_image, hand_landmarks)
                    debug_image = draw_bounding_rect(self.show_window, debug_image, brect)
                    debug_image = draw_landmarks(debug_image, landmark_list)
                    debug_image = draw_info(debug_image, fpsCalc, 0, 0)

                    # print info about gesture detection
                    if result_confidence > self.min_gest_conf:
                        print(self.labels[hand_sign_id], result_confidence)

            # get the next frame
            frame = self.camera.read_frame()

            if self.show_window: 
                cv.imshow('Hand Gesture Recognition', debug_image)
        
        # cleanup when finished
        self.camera.release()
        if self.show_window: 
            cv.destroyAllWindows()


    def run_single(self, frame):
        # detect on single frame, return (label, confidence)
        # Modify current frame to fit mp hands model
        frame = cv.flip(frame, 1)
        debug_image = copy.deepcopy(frame)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # get results from hands model
        frame.flags.writeable = False
        results = self.hands_model.process(frame) # use mediapipe to detect
        frame.flags.writeable = True


        detection_results = (None, None, None)
        # Run through detections in current frame
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:

                # get coordinates of all landmarks
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # Conversion from relative coordinates to normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(landmark_list)

                # detect gesture in current frame
                hand_sign_id, result_confidence = self.tf_lite_model(pre_processed_landmark_list)


                brect = calc_bounding_rect(debug_image, hand_landmarks)
                debug_image = draw_bounding_rect(self.show_window, debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_info(debug_image, 0, 0, 0)

                detection_results = (hand_sign_id, result_confidence, debug_image)
        

        return detection_results


        





def main():
    detector = Detector(
        min_gest_conf=0.79, 
        min_hand_conf=0.97, 
        show_window=True
    )

    detector.run_all()



if __name__ == "__main__":
    main()





    

    
    

        

