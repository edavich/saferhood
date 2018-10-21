import dlib
import face_recognition
import cv2
import time
import os


# Describes a known face, this will come from analyzing a file uploaded by the user
class Face:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = face_recognition.load_image_file("input/" + image_path);
        self.encoding = face_recognition.face_encodings(self.image)[0]
        self.known = True
        self.name = image_path.split('.')[0]
        if '_' in self.name:
            self.name = self.name.replace('_', ' ')



def AnalyzeFeed(faces):
    video_capture = cv2.VideoCapture(0) #refernce to the default webcam

    face_locations = []
    face_encodings = []
    face_names = []

    process_this_frame = True
    known_face_encodings = [face.encoding for face in faces]
    known_face_names = [face.name for face in faces]

    print("Starting")
    font_color = (255, 255, 255) # (white)
    red_font_color = (0, 0, 255) # (red)
    font = cv2.FONT_HERSHEY_DUPLEX
    hot_names = ["Trump", "Biden", "matt link"]
    displayed_names = []
    found_names = []

    while True:
        # Get the current frame
        ret, frame = video_capture.read()

        # Resize frame to 1/4 size for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from OpenCV BGR color to RGB color use by face_recognition
        rgb_small_frame = small_frame[:, :, ::-1]

        # Process every other frames of video to save time
        if process_this_frame:
            # Locate faces in the current frame of the video feed
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for encoding in face_encodings:
                # check if it matches a known face
                matches = face_recognition.compare_faces(known_face_encodings, encoding)
                name = "Unknown"

                # If a match is found, use the first match
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

                if name in hot_names:
                    found_names.append(name)
                if len(found_names) > 0:
                    for i in range(len(found_names)):
                        if found_names[i] not in displayed_names:
                            displayed_names.append(found_names[i])

                if len(displayed_names) > 0:
                    cv2.putText(frame, "ALERT:", (2, 30), font, 1.0, red_font_color, 1)
                    
                for i in range(len(displayed_names)):
                    cv2.putText(frame, displayed_names[i], (25, i * 30 + 65), font,  1.0, red_font_color, 1)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 Resize
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Outline face with box
            outline_color = (255, 0, 0)
            cv2.rectangle(frame, (left, top), (right, bottom), outline_color, 2)

            # Label the box with the name of the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), outline_color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, font_color, 1)

        # Display the image
        cv2.imshow('Video', frame)

        # Allow user to quit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Realease handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    # read all images to create faces from them
    faces = []
    images = [file for file in os.listdir('input') if file[0] != '.'] # filter out "dot" files
    print(images)
    for image_path in images:
        faces.append(Face(image_path))

    print(faces)

    AnalyzeFeed(faces)
