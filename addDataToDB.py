import firebase_admin
from firebase_admin import credentials ,db
import firebase_admin.db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://face-recog-attandance-default-rtdb.firebaseio.com/'})


#Create thereference 
ref = db.reference("Students")

data ={
    "Hedi":{
        "name" : "Hedi Bk",
        "major" : "Computer Science",
        "starting_year" : 2019,
        "total_attandance" : 5,
        "standing" : "G",
        "year" : 4,
        "last_attandance_time" : "2025-07-21 00:00:00"
    },
    "Zou":{
        "name" : "3am Zou",
        "major" : "ML and AI",
        "starting_year" : 2022,
        "total_attandance" : 5,
        "standing" : "G",
        "year" : 4,
        "last_attandance_time" : "2025-07-21 00:00:00"
    },
    "Tate":{
        "name" : "Abou Tate",
        "major" : "Web Developer",
        "starting_year" : 2019,
        "total_attandance" : 5,
        "standing" : "G",
        "year" : 4,
        "last_attandance_time" : "2025-07-21 00:00:00"
    }
}

for key,value in data.items() :
    # Send data to a specific Directory named "Students"
    ref.child(key).set(value)