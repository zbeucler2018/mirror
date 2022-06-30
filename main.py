

import cv2

from Detector.detector import Detector

from UiDriver import UI_Driver


"""
    Remeber to start the web server before
    cd UI && python -m http.server

    need buster instead of bullseye. RPI is switching from raspistill to libcamera and libcamera has no python bindings right now. raspistill is in buster only
"""


CHANGE_INTERVAL = 30 #frames

detector = Detector(
    min_gest_conf=0.75, 
    min_hand_conf=0.80, 
    show_window=False
)


ui_driver = UI_Driver(port=8000)

ui_driver.change_ui("init")


cam = detector.camera
cam.set_up_camera()
current_frame = cam.read_frame()

frame_count = 0
while current_frame is not False:
    frame_count += 1

    key = cv2.waitKey(10)
    if key == 27:  # ESC
        break

    (label, confidence, img) = detector.run_single(current_frame)

    # if something has been detected
    if label is not None:
        label = detector.labels[label] # get the text of the label
        print(label, confidence)

        
    if frame_count % CHANGE_INTERVAL == 0:
        next_wallpaper = label
        print(f"changing to {next_wallpaper}...")
        ui_driver.change_ui(next_wallpaper)

    else:
        print("No detections") 

    if detector.show_window:
        if img is None:
            cv2.imshow('Hand Gesture Recognition', current_frame)
        else:
            cv2.imshow('Hand Gesture Recognition', cv2.flip(img,1))

    current_frame = cam.read_frame()


cam.release()
if detector.show_window:
    cv2.destroyAllWindows()






