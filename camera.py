import cv2

class Camera:

    def __init__(self, camera_index=0):
        self._video_capture = None
        self._camera_index = camera_index

    def setup(self):
        self._video_capture = cv2.VideoCapture(self._camera_index)

        if not self._video_capture.isOpened():
            raise RuntimeError("Camera is already being used")

        self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)


    def get_frame(self):
        ret, frame = self._video_capture.read()
        if ret:
            return frame
        raise None
    
    def release(self):
        self._video_capture.release()



