import json
from firebase import firebase
import math
from firebase.firebase import FirebaseApplication
import geocoder
import pyrebase
import pandas as pd
import copy
g = geocoder.ip('me').latlng
config = {
  "apiKey": " AIzaSyAiAmAVCDmogWqXRb0X5pxe8-ZSKNvNQ14 ",
  "authDomain": "code-11-54-dispatcher.firebaseapp.com",
  "databaseURL": "https://code-11-54-dispatcher.firebaseio.com",
  "storageBucket": "code-11-54-dispatcher.appspot.com"
}
def connect_firebase():
    # add a way to encrypt those, I'm a starter myself and don't know how
    #username: ""
    #password: "passwordforaboveuser"

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth() 

    #authenticate a user > descobrir como não deixar hardcoded
    #user = auth.sign_in_with_email_and_password(username, password)

    #user['idToken']
    # At pyrebase's git the author said the token expires every 1 hour, so it's needed to refresh it
    #user = user.refresh(auth['refreshToken'])

    #set database
    db = firebase.database()

    return db
#firebase = FirebaseApplication(config)
#firebase = FirebaseApplication('https://console.firebase.google.com', None)
#result = firebase.get('/u/0/project/code-11-54-dispatcher/database/code-11-54-dispatcher/data/', 'KA')
#result = json.loads(result)
#print(result)
firebase = firebase.FirebaseApplication('https://code-11-54-dispatcher.firebaseio.com/')
fb = connect_firebase()
values = fb.get()
vlsl = dict(values.val())
        
with open("output2.txt.txt","r") as ip:
    vl = ip.readline()
    print(vl)
    tp = []
    net=0
    tps=""
    chk=0
    for i in range(len(vl)):
        if vl[i].isdigit():
            if net%2!=0 and net<=3:
                tps = tps+vl[i]
                if len(tps)==2 and net==1:
                    tp.append(copy.deepcopy(tps))
                    tps=""
                    net+=1
                elif len(tps)==4:
                    tp.append(copy.deepcopy(tps))
                    tps=""
                    net+=1
            #else:
            #    chk=1
            #    break
        if vl[i].isalpha():
            if net%2==0 and net<=3:
                tps = tps+vl[i]
                if len(tps)==2:
                    tp.append(copy.deepcopy(tps))
                    tps=""
                    net+=1
           # else:
            #    chk=1
             #   break
    #if chk==1:
     #   exit(0)
    values = fb.child(tp[0]).child(tp[1]).child(tp[2]).child(tp[3]).child("stolen").get().val()
    if values == None:
        stns = vlsl["stations"]
        print(stns)
        temp = stns.keys()
        nearest = ""
        d = -1
        for tpst in temp:
            lat = stns[tpst]["latitude"]
            longt = stns[tpst]["longitude"]
            print(g[0])
            dist = math.sqrt((lat-int(g[0]))**2+(longt-int(g[1]))**2)
            if d==-1 or dist<d:
                nearest = tpst
        data = {"".join(tp):{'latitude':g[0],'longitude':g[1]}}
        #data2 = {'longitude':g[1]}
        #print(data)
        #dic_tp = json.dumps("".join(tp))
        #data = json.dumps(data)
        #data2 = json.dumps(data2)
        fb.child("stations").child(nearest).child("alerts").set(data)
    #if values == 'stolen':
        
    #data = pd.DataFrame(values.val())
    #print(data)
