import cv2
import os
import numpy as np
import json

FaceRecognitionModel = os.path.join(os.path.dirname(__file__), "Model.yml")
FaceRecognitionDatasetPath = os.path.join(os.path.dirname(__file__), "FaceTrainingDataset")
FaceRecognitionLabelMap = os.path.join(os.path.dirname(__file__), "labelMap.json")
trainerImageSize = (200, 200)

def TrainModel():
    faces = []
    labels = []

    if os.path.exists(FaceRecognitionLabelMap):
        with open(FaceRecognitionLabelMap, "r") as f:
            labelMap = json.load(f)
        print("Loaded existing label map.")
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
            print(f"Skipping folder with invalid name: {PersonFolderName}")
            continue

        labelMap[personIdStr] = personName

        for imageFile in os.listdir(PersonFolder):
            imagePath = os.path.join(PersonFolder, imageFile)
            image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

            if image is None:
                print(f"Skipping unreadable file: {imagePath}")
                continue
            
            image = cv2.resize(image, trainerImageSize)

            faces.append(image)
            labels.append(personId)
        
        if not faces:
            print(f"No valid training images found for {personName}.")
    
    # faces = np.array(faces)
    labels = np.array(labels)

    if len(faces) == 0 or len(labelMap) == 0:
        print("Training Failed")
        return False

    print(f"Found {len(faces)} images across {len(labelMap)} people.")

    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
    faceRecognizer.train(faces, labels)
    os.makedirs(os.path.dirname(FaceRecognitionModel), exist_ok=True)
    faceRecognizer.save(FaceRecognitionModel)

    with open(FaceRecognitionLabelMap, "w") as f:
        json.dump(labelMap, f)
    
    print(f"Model updated and saved at: {FaceRecognitionModel}")
    print(f"Label map updated and saved at: {FaceRecognitionLabelMap}")
    return True
