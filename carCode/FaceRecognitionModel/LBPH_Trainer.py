import cv2
import os
import numpy as np
import json

FaceRecognitionModel = os.path.join(os.path.dirname(__file__), "LBPH_Trainer.yml")
FaceRecognitionDatasetPath = os.path.join(os.path.dirname(__file__), "FaceTrainingDataset")
FaceRecognitionLabelMap = os.path.join(os.path.dirname(__file__), "labelMap.json")

def TrainModel():
    faces = []
    labels = []

    if os.path.exists(FaceRecognitionLabelMap):
        with open(FaceRecognitionLabelMap, "r") as f:
            labelMap = json.load(f)
        print("[INFO] Loaded existing label map.")
    else:
        labelMap = {}
        
    for PersonFolderName in os.listdir(FaceRecognitionDatasetPath):
        PersonFolder = os.path.join(FaceRecognitionDatasetPath, PersonFolderName)
        if not os.path.isdir(PersonFolder):
            continue

        try:
            personName, personIdStr = PersonFolderName.rsplit("_", 1)
            personId = int(personIdStr)
        except ValueError:
            print(f"[WARNING] Skipping folder with invalid name: {PersonFolderName}")
            continue

        labelMap[personIdStr] = personName

        for imageFile in os.listdir(PersonFolder):
            imagePath = os.path.join(PersonFolder, imageFile)
            image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

            if image is None:
                print(f"[WARNING] Skipping unreadable file: {imagePath}")
                continue
            
            image = cv2.resize(image, (200, 200))

            faces.append(image)
            labels.append(personId)
        
        if not faces:
            print(f"No valid training images found for {personName}.")
    
    # faces = np.array(faces)
    labels = np.array(labels)
    print(f"[INFO] Found {len(faces)} images across {len(labelMap)} people.")

    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
    faceRecognizer.train(faces, labels)
    os.makedirs(os.path.dirname(FaceRecognitionModel), exist_ok=True)
    faceRecognizer.save(FaceRecognitionModel)

    with open(FaceRecognitionLabelMap, "w") as f:
        json.dump(labelMap, f)
    
    print(f"[INFO] Model updated and saved at: {FaceRecognitionModel}")
    print(f"[INFO] Label map updated and saved at: {FaceRecognitionLabelMap}")

# # Load existing LBPH model if it exists
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# if os.path.exists(FaceRecognitionModel):
#     recognizer.read(FaceRecognitionModel)

# # Function to load all images and labels
# def get_images_and_labels(path):
#     faces = []
#     ids = []
#     for file in os.listdir(path):
#         if file.endswith(".jpg"):
#             img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
#             label = int(file.split("_")[1])  # assuming filename format: name_ID_#.jpg
#             faces.append(img)
#             ids.append(label)
#     return faces, np.array(ids)

# # Step 1: Collect new samples for the new person
# new_person_name = "Bob"
# new_person_id = 2
# new_faces = []  # list of grayscale images
# # For example, populate new_faces from camera capture
# # new_faces.append(gray_face)

# # Step 2: Save new faces to dataset folder
# for i, face in enumerate(new_faces):
#     cv2.imwrite(f"{dataset_path}/{new_person_name}_{new_person_id}_{i}.jpg", face)

# # Step 3: Reload all faces + labels (old + new)
# faces, ids = get_images_and_labels(dataset_path)

# # Step 4: Retrain LBPH
# recognizer.train(faces, ids)
# recognizer.save(model_path)
# print("LBPH model updated with new person.")
