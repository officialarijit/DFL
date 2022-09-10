#================================================================================================
# Import important libraries
#================================================================================================
import os

import paho.mqtt.client as mqtt
import time, queue, sys, datetime, json, math, scipy, pywt, time
import pandas as pd
import numpy as np

from json import JSONEncoder
from statistics import mode
from scipy import stats
from sklearn import preprocessing
from collections import defaultdict, Counter
from window_slider import Slider

from dotenv import load_dotenv


from feature_extraction_utils import *
from data_reading_utils import *
from model_creation import *
from Numpy_to_JSON_utils import *
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
# from multi_label_performance_metrics_utils import *


load_dotenv('.env')


#=================================================================================================
all_emo = []
#=================================================================================================

#=================================================================================================
print('---------------------------------------------------------------')
n = sys.argv[1] #Reading the command line argument passed ['filename.py','passed value/client number']

client_name = 'LocalServer (User)'+n

print(client_name +':>>' +' ' +'Streaming Strated!')

p = int(n) #Person number


#=================================================================================================

#=================================================================================================
# All MQTT ones Here
#=================================================================================================
qLS = queue.Queue() #Queue to store the received message in on_message call back

def on_connect(client, userdata, flags, rc):
    if rc ==0:
        print("Local Server connected to broker successfylly ")
    else:
        print(f"Failed with code {rc}")

    for i in topic_list:
        val = client.subscribe(i)
        print(val)


def on_message(client, userdata, message): #On message callback from MQTT
    print('Global Model Received after FedAvg')
    qLS.put(message)


#=========================================================================
#reading all this configs from the config files
MQTTbrokerIP = os.environ.get("MQTT_SERVER_IP")
mqtt_port = os.environ.get("MQTT_PORT")
gm_topic = os.environ.get("MQTT_global_model_topic")
folderPath = os.environ.get("Local_model_performance_file")
segment_in_sec = os.environ.get('segment_in_sec')
#=========================================================================

mqttBroker = MQTTbrokerIP
client = mqtt.Client(client_name) #mqtt Client
client.on_connect = on_connect
client.connect(mqttBroker, mqtt_port) #mqtt broker connect





topic_list =[(gm_topic,0)] #Subscription topic list

client.loop_start()

#**********************************************************
time.sleep(5) #Wait for connection setup to complete
#**********************************************************

print('---------------------------------------------------------------')

#=================================================================================================

#------------------------------------
# Once file fetched data stored here
#------------------------------------
# grand_eeg = eeg_data(p)
grand_eda = eda_data(p)
grand_resp = resp_data(p)

#=================================================================================================


#=================================================================================================
# Sliding Window
#=================================================================================================
bucket_size = int((8064/60)*segment_in_sec)  #8064 is for 60 sec record
overlap_count = 0

#================================================
# Model name and other loop control parameters
#================================================
classifier = 'FFNN_Feature_Fusion'
init_m = 0
indx = 0
c=0
ccc =0
i =0
videos = 32 #Total Number of Videos
#=================================================================================================

print('-----------------------------------------')
print('Working with -->', classifier)
print('-----------------------------------------')
#=======================================
# MAIN Loop STARTS HERE
#=======================================
for jj in range(0,videos): #Video loop for each participants
    v = jj+1 #Video number
    print('=========================================================================')
    p_v = 'Person:'+ ' ' +str(p)+ ' ' +'Video:'+str(v)
    print(p_v)

    emotion_label =[]


    ##===================================================
    # Data read from files
    ##===================================================
    eda_sig = grand_eda.loc[grand_eda.iloc[:,1] == v]
    resp_sig = grand_resp.loc[grand_resp.iloc[:,1] == v]

    #=================================================
    #emotion labels (valence, arousal) mapping 0-1
    #=================================================
    val = eda_sig.iloc[0,8067]
    aro = eda_sig.iloc[0,8068]


    #==================================================================
    # Useful For classification
    #==================================================================

    if (val >0 and val <4.5):
        vl = 1 # low valence
    elif(val >=4.5 and val <=5.5):
        vl =  2 # mid valence
    else:
        vl = 3 #high valence

    #arousal emotion maping 0-> low arousal and 1-> high high arousal
    if (aro >0 and aro <4.5):
        al = 1 # low valence
    elif(aro >=4.5 and aro <=5.5):
        al =  2 # mid valence
    else:
        al = 3 #high valence


    if (vl ==1 and al ==1):
        y_act = np_utils.to_categorical(0, num_classes=9) #1
    elif(vl ==1 and al == 2):
        y_act = np_utils.to_categorical(1, num_classes=9) #2
    elif(vl ==1 and al == 3):
        y_act = np_utils.to_categorical(2, num_classes=9) #3
    elif(vl ==2 and al == 1):
        y_act = np_utils.to_categorical(3, num_classes=9) #4
    elif(vl ==2 and al == 2):
        y_act = np_utils.to_categorical(4, num_classes=9) #5
    elif(vl ==2 and al == 3):
        y_act = np_utils.to_categorical(5, num_classes=9) #6
    elif(vl ==3 and al == 1):
        y_act = np_utils.to_categorical(6, num_classes=9) #7
    elif(vl ==3 and al == 2):
        y_act = np_utils.to_categorical(7, num_classes=9) #8
    elif(vl ==3 and al == 3):
        y_act = np_utils.to_categorical(8, num_classes=9) #9

    y_act = np.array([y_act])

    discrete_emotion = {0:'Sad', 1:'Miserable',2:'Angry',3:'Sleepy',4:'Neurtal',5:'Tense',6:'Calm',7:'Happy',8:'Excited'} #emotion labels

    #==================================================================

    #==========================================================
    # Predicted Valence and Arousal labels list initialization
    #==========================================================


    #=========================================
    # Sliding window starts here
    #=========================================
    slider_eda = Slider(bucket_size,overlap_count)
    slider_resp = Slider(bucket_size,overlap_count)

    eda_sig = np.array(eda_sig.iloc[:,range(3,8067)]) #keeping only eda signals
    resp_sig = np.array(resp_sig.iloc[:,range(3,8067)]) #keeping only resp signals

    slider_eda.fit(eda_sig)
    slider_resp.fit(resp_sig)

    while True:
        window_data_eda = slider_eda.slide()
        window_data_resp = slider_resp.slide()


        #=================================================
        # Feature extraction from EDA
        #=================================================
        eda_features = extract_eda_features(np.array(window_data_eda))
        eda = np.array([eda_features]) #EDA raw feature vector
        x_eda = np.array(preprocessing.normalize(eda)) #EDA normalized features

        #=================================================
        # Feature extraction from Resp belt
        #=================================================

        resp_features = extract_resp_belt_features(np.array(window_data_resp))
        resp = np.array([resp_features]) #RESP BELT raw feature vector
        x_resp = np.array(preprocessing.normalize(resp)) #RESP BELT normalized features


        x_FF = np.array([np.concatenate([x_eda,x_resp], axis=None)]) #Fused Feature

        #===================================================
        # Model initialization
        #===================================================
        if init_m == 0:
            # print('EDA Feature shape{}:'.format(x_eda.shape))
            # print('RESP BELT Feature shape{}:'.format(x_resp.shape))
            print('Fused Feature shape{}:'.format(x_FF.shape))

            #==============================
            # Feature Fused Model
            #==============================
            fm_model = create_model(x_FF,'Fusion_Model')

            init_m = init_m+1


        #===============================================================
        # Emotion Classification --> Valence and Arousal
        #===============================================================

        if c == 0: #For the first time model will return 9 or None
            tmp_y = np.array([[9,9]])
            fm_model.fit(x_FF, y_act, epochs = 1, batch_size = 1, verbose=0)

            c=c+1

        else:
            tmp_y = fm_model.predict(x_FF)
            fm_model.fit(x_FF, y_act, epochs = 1, batch_size = 1, verbose=0)

        if slider_eda.reached_end_of_list():
            break


    #===========================================
    # Performance matric update
    #===========================================
    y_pred = np.array([np.argmax(tmp_y[0])])

    mc_y_act = np.array([np.argmax(y_act)])

    bac = accuracy_score(mc_y_act,y_pred)
    f1 = f1_score(mc_y_act,y_pred, average='micro')

    print('-------------------------------------------------------------------------------')
    print('Actual Class:',discrete_emotion[mc_y_act[0]])
    print('Fusion Model predicted:{}'.format(discrete_emotion[y_pred[0]]))


    print(client_name+'-->'+'Accuracy:{}'.format(bac))
    print(client_name+'-->'+'F1-score:{}'.format(f1))
    print('-------------------------------------------------------------------------------')

    all_emo.append([p,v, bac,f1, mc_y_act[0], y_pred[0]])

    #========================================================================================
    #Send the model performance from each to server for checking Global Model's performance
    #========================================================================================
    if i >0:
        model_performance = {'Local_Model':p,'Acc':bac,'F1_val':f1}
        encoded_model_performance = json.dumps(model_performance)
        client.publish("ModelPerformance", payload = encoded_model_performance)
        print("Local Model Performance Broadcasted for "+ p_v +" to Topic:-> ModelPerformance")



    #==========================================================
    # Model weight compress into JSON format
    #==========================================================

    #Message Generation and Encoding into JSON
    model_weights = fm_model.get_weights()
    encodedModelWeights = json.dumps(model_weights,cls=Numpy2JSONEncoder)

    #==========================================================
    # Broadcast (Publish) Local model weights to the mqttBroker
    #==========================================================

    client.publish("LocalModel", payload = encodedModelWeights)

    print("Local Model Broadcasted for "+ p_v +" to Topic:-> LocalModel")

    #**********************************************************
    time.sleep(70) #put the loca server in sleep for 60 sec
    #**********************************************************

    #===============================================================================
    # Receive Global model from the Subscriber end
    #===============================================================================

    # if i>0:
    #===============================================================================
    # Publisher as subscriber to receive results after operation at Subscriber end
    #===============================================================================
    client.on_message = on_message
    while not qLS.empty():
        message = qLS.get()

        if message is None:
            continue

        msg = message.payload.decode('utf-8')

        # Deserialization the encoded received JSON data
        global_weights = json2NumpyWeights(msg)

        fm_model.set_weights(global_weights) #Replacing the old model with the newley received model from Global Server


    if (i == videos): #if all the videos are done means no more data from User
        break

    i +=1


#===============================================================================
#Save all the results into CSV file
#===============================================================================
fname_fm = folderPath + client_name +'_person_FusionModel'+'_'+'_results.csv'
column_names = ['Person', 'Video', 'Acc','F1', 'y_act', 'y_pred']
all_emo = pd.DataFrame(all_emo,columns = column_names)
all_emo.to_csv(fname_fm)

print('All Done! Client Closed')
