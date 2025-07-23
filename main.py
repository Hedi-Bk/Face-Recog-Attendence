import cv2
import pickle
from facenet_pytorch import MTCNN ,InceptionResnetV1
import cvzone
import os
import firebase_admin
from firebase_admin import credentials ,db
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://face-recog-attandance-default-rtdb.firebaseio.com/'})


#Create thereference 



cap =cv2.VideoCapture(0)

# Shoose The width of the Frame
frame_w = 640 
frame_h = int(frame_w*480/640)

# Importing the mode images 
folderModePath = "resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList :
    img =cv2.imread(os.path.join(folderModePath,path))
    img =cv2.resize(img ,(413,598))
    imgModeList.append(img)


# MODE types range from 0 -> 3
modeType = 0
counter = 0

mtcnn = MTCNN()
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Load The encoding File 'pickle'
print("Loading Encoding File ... !👇")
file = open("EncodedFile.p","rb")
encodeListKnown,studentNames = pickle.load(file)

file.close()
print(f"Student Name :{studentNames}")
print("Encode File Loaded  🔥")

while True : 
    Background = cv2.imread("D:/ASL/PROJETs/ML/Attendance/resources/Modes/Background.png")
    Background[51:51+598 , 826:826+413] = imgModeList[modeType]
    success, img = cap.read()
    img = cv2.resize(img,(frame_w,frame_h))
    #(x 826 ,y 51)

    # Pass the Image to the Face Detector
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face = mtcnn(img)
    if face is not None:
        boxe , probs = mtcnn.detect(img)
        x1,y1,x2,y2 = boxe[0]
        x1,y1,x2,y2 = int(x1), int(y1),int(x2),int(y2)
        
        cvzone.cornerRect(img,(x1,y1,x2-x1,y2-y1),colorC=(255,255,255))
        cv2.putText(Background,f"Face Detetcted",(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        embedding = resnet(face.unsqueeze(0))

        ## Detetermine The Student Detetcted In the Frame 
        distances =[]
        for i,encodedFace in enumerate(encodeListKnown) :
            distance = (embedding - encodedFace).norm().detach().item()
            distances.append(distance)
        studentIdx = distances.index(min(distances))
        studentName = studentNames[studentIdx]

        if min(distances) < 0.8 : 

            if counter == 0:
                cvzone.putTextRect(img,"Loading",(x1,y1),colorR=(0,0,255))
                cv2.waitKey(1)
                counter =1 
            cv2.rectangle(Background,(35,90),(35+frame_w,90+frame_h),(0,255,0),4)
            if counter != 0:
                ## Only Load the Student Info For th first Time Detettcted From Firebase 
                if counter ==  1:
                    studentInfo = db.reference(f"Students/{studentName}").get()
                    modeType = 1
                    
                    dateTimeObject = datetime.strptime(studentInfo["last_attandance_time"],"%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - dateTimeObject).total_seconds()

                    if secondsElapsed > 30 :
                        # Update the Data of attendece 
                        ref = db.reference(f"Students/{studentName}")
                        studentInfo["total_attandance"] += 1
                        ref.child("total_attandance").set(studentInfo["total_attandance"])
                        #Update the last attendezcne once 
                        ref.child("last_attandance_time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else :
                        modeType = 3 # ALREADY MARKED 
                        counter = 0

                if counter in range(10,21) and modeType != 3:
                    modeType = 2

                Background[51:51+598 , 826:826+413] = imgModeList[modeType]

                if counter<= 10 and modeType != 3: 
                    # Display the Image of the Student
                    imgStudentCopy = cv2.imread(f"images/{studentName}.jpg")
                    imgStudentCopy = cv2.resize(imgStudentCopy,(289,289))
                    Background[176:176+289,892:892+289 ] = imgStudentCopy

                    (w,h),_ = cv2.getTextSize(studentInfo["name"], cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                    spaceW = 1230 -835
                    offset = (spaceW-w)//2
                    cv2.putText(Background,studentInfo["name"],(835+offset,530),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)  
                    cv2.putText(Background,str(studentInfo["total_attandance"]),(920,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
            
                counter += 1
                if counter > 20 :
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    Background[51:51+598 , 826:826+413] = imgModeList[modeType] 

        else :
            cv2.rectangle(Background,(35,90),(35+frame_w,90+frame_h),(0,0,255),5)
            cv2.putText(Background,f"But not recognized",(300,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    else :
        modeType = 0
        counter = 0




    Background[90:90+frame_h,35:35+frame_w] =cv2.cvtColor(img,cv2.COLOR_RGB2BGR) 


    cv2.imshow("Video",Background)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break