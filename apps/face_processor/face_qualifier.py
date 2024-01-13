import cv2

class FaceQualifier:
    def __init__(self):
        self.ageProto="./models/age_deploy.prototxt"
        self.ageModel="./models/age_net.caffemodel"
        self.genderProto="./models/gender_deploy.prototxt"
        self.genderModel="./models/gender_net.caffemodel"

        self.MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
        self.ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
        self.genderList=['M','F']

        self.ageNet=cv2.dnn.readNet(self.ageModel,self.ageProto)
        self.genderNet=cv2.dnn.readNet(self.genderModel, self.genderProto)

    def detect(self, face):
        blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), self.MODEL_MEAN_VALUES, swapRB=False)
        self.genderNet.setInput(blob)
        genderPreds=self.genderNet.forward()
        gender=self.genderList[genderPreds[0].argmax()]
        self.ageNet.setInput(blob)
        agePreds=self.ageNet.forward()
        age=self.ageList[agePreds[0].argmax()]
        return (gender, age[1:-1])