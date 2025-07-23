from facenet_pytorch import MTCNN ,InceptionResnetV1
import cv2 
import os
import pickle

mtcnn = MTCNN()
resnet = InceptionResnetV1(pretrained='vggface2').eval()
# Importing the Student Imagges 
folderPath ="./images"
imagesPathList = os.listdir(folderPath)
imgList = []
nameList = []   

for imagePath in imagesPathList:
    nameList.append(imagePath.split(".")[0])
    imgList.append(cv2.imread(os.path.join(folderPath, imagePath)))

def findEncodings(imgList):

    encodeList =[]
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face = mtcnn(img)
        if face is not None:
            # Extraction embedding
            embedding = resnet(face.unsqueeze(0))
            encodeList.append(embedding)
    return encodeList


print("Encoding Started ... !")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithId = [encodeListKnown, nameList]
print("Encoding Complete 🔥 ")

file = open("EncodedFile.p","wb")
pickle.dump(encodeListKnownWithId,file)
file.close()
print("File Saved .. !🔥")