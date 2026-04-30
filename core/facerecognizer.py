from camera import Camera
import face_recognition

class FaceRecognizer:
    def __init__(self, tolerance=0.6):
        self._known_face_embeddings=[]
        self._known_names=[]
        self._tolerance = tolerance

    def add_recognized_person(self, name, frame):
        if frame is None:
            return False,"empty_frame"
        
        rgb_frame = frame[:,:,::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) == 0:
            return False, "no_face"
        if len(face_locations) > 1:
            return False, "multiple_faces"
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        self._known_face_embeddings.append(encodings[0])
        self._known_names.append(name)
        return True, "success"


    def is_known_face(self, frame):
        if frame is None:
            return False, [], "empty_frame"
        rgb_frame = frame[:,:,::-1]

        recognized_faces=[]

        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) > 0:
            encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            for face_location, face_encoding in zip(face_locations, encodings):
                matches = face_recognition.compare_faces(self._known_face_embeddings, face_encoding, self._tolerance)
                if not any(matches):
                    recognized_faces.append((face_location, "Unknown"))
                else:
                    first_match_index = matches.index(True)
                    name = self._known_names[first_match_index]
                    recognized_faces.append((face_location, name))
            return True, recognized_faces, "success"
        else:
            return False, [], "no_face"


        