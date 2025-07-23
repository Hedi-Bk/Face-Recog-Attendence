![Demo](DemoAttendence.gif)

#  Real-Time Face Attendance System with Firebase

A smart solution to automate attendance tracking using face recognition and cloud-based storage.  
No more manual attendance or long lists — just a camera and your face. 🔥

---

##  Why This Project?

In conferences, workshops, or classrooms, tracking attendance manually is time-consuming and error-prone.  
This project solves that by **automatically verifying and logging attendance using facial recognition**.

✅ **Efficient** – No manual attendance  
✅ **Real-time** – Live presence updates via camera  
✅ **Accurate** – Prevents duplicate attendance per day  
✅ **Scalable** – Works for any number of participants

---

## Pipeline Overview

1. **Face Collection**  
   Authorized users provide a clear image of their face before the event.

2.  **Image Storage**  
   The images are saved locally in the `images/` folder.

3.  **Face Embedding Generation**  
   We run `EncodeGenerator.py` to extract face embeddings using **FaceNet**.  
   These are stored in `EncodedFile.p` — one encoding per authorized user.

4.  **Live Face Detection & Matching**  
   During the event, the webcam scans faces in real time.  
   If a match is found, the presence is recorded in **Firebase Realtime Database**.

5.  **One Entry per Day Rule**  
   A person can only validate their presence **once per day**.  
   (For demo purposes, we used a 30-second interval instead.)

6.  **Live Dashboard**  
   Presence data is displayed in real time via Firebase, making it easy to monitor attendance.

---

##  Tools & Technologies Used

-  **Firebase Realtime Database** – Cloud-based attendance logging
-  **Python**
-  **OpenCV** – Webcam face detection
-  `facenet_pytorch`
  - `MTCNN` – Face detection
  - `InceptionResnetV1` – Face embedding (feature extraction)

---

##  Skills Demonstrated

-  **Face Verification** from a database
-  **Face Embedding Generation**
-  **Cloud Integration** with Firebase
-  **Real-time face matching** and live database updates
-  **End-to-end pipeline design** for a computer vision system

---
