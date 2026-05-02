import face_recognition
from databasemanager import DataBaseManager
import os
import numpy as np
import cv2

class FaceRecognizer:
    def __init__(self, tolerance=0.6):
        self._databasemanager = DataBaseManager()
        all_data = self._databasemanager.load_all_users()
        if all_data:
            names, embeddings, pictures = zip(*all_data)
            self._known_names = list(names)
            self._known_face_embeddings = list(embeddings)
            self.picture_paths = list(pictures)
        else:
            self._known_names = []
            self._known_face_embeddings = []
            self.picture_paths = []
        self._tolerance = tolerance

    def add_recognized_person(self, name, frame, picture_path):
        if frame is None:
            return False,"empty_frame"
        if name in self._known_names:
            return False, "name_occupied"

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) == 0:
            return False, "no_face"
        if len(face_locations) > 1:
            return False, "multiple_faces"
        
        encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

        if self._known_face_embeddings: 
            matches = face_recognition.compare_faces(self._known_face_embeddings, encoding, self._tolerance)
            if any(matches):
                return False, "face_is_known"
            
        success, message = self._databasemanager.save_user(name, encoding, picture_path)
        if success:
            self._known_face_embeddings.append(encoding)
            self._known_names.append(name)
            self.picture_paths.append(picture_path)
        return True, "success"


    def is_known_face(self, frame):
        if frame is None:
            return False, [], "empty_frame"
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        recognized_faces=[]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        if len(face_locations) > 0:
            encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            for face_location, face_encoding in zip(face_locations, encodings):
                name = "Unknown"
                if self._known_face_embeddings:
                    face_distances = face_recognition.face_distance(self._known_face_embeddings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if face_distances[best_match_index] <= self._tolerance:
                        name = self._known_names[best_match_index]

                top, right, bottom, left = face_location
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                recognized_faces.append(((top, right, bottom, left), name))
            return True, recognized_faces, "success"
        else:
            return False, [], "no_face"
        
    def color_faces(self, frame, recognized_faces):
        font_scale = 0.6  
        font_thickness = 1
        font = cv2.FONT_HERSHEY_DUPLEX
        for(top, right, bottom, left), name in recognized_faces:
            color = (76, 156, 0)
            if name == "Unknown":
                color = (0,0,255)
            cv2.rectangle(frame, (left,top), (right, bottom),color, 2)
            (text_width, text_height), baseline = cv2.getTextSize(name, font, font_scale, font_thickness)
            box_width = max(right - left, text_width + 10)
            cv2.rectangle(frame, (left, bottom), (left + box_width, bottom + text_height + 10), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 5, bottom + text_height + 5), font, font_scale, (255, 255, 255), font_thickness)
        return frame
    
    def delete_recognized_person(self, name):
        if name not in self._known_names:
            return False, "unknown_name"
        
        index = self._known_names.index(name)
        path_to_delete = self.picture_paths[index]
        self._databasemanager.delete_user(name)

        picture_deleted = False
        try:
            if os.path.exists(path_to_delete):
                os.remove(path_to_delete)
                picture_deleted = True
        except Exception as e:
            pass
        
        self._known_names.pop(index)
        self.picture_paths.pop(index)
        self._known_face_embeddings.pop(index)
        
        if not picture_deleted:
            return False, "picture_not_deleted"
        return True, "deleted"




        