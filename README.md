# A Federated Learning Method for Real-time Emotion State Classification from Multi-modal Streaming

## Piblication link: https://www.sciencedirect.com/science/article/pii/S104620232200072X

`ABSTRACT:` Emotional and physical health are strongly connected and should be taken care of simultaneously to ensure completely healthy persons. A person’s emotional health can be determined by detecting emotional states from various physiological measurements (EDA, RB, EEG, etc.). Affective Computing has become the field of interest, which uses software and hardware to detect emotional states. In the IoT era, wearable sensor-based real-time multi-modal emotion state classification has become one of the hottest topics. In such setting, a data stream is generated from wearable-sensor devices, data accessibility is restricted to those devices only and usually a high data generation rate should be processed to achieve real-time emotion state responses. Additionally, protecting the users’ data privacy makes the processing of such data even more challenging. Traditional classifiers have limitations to achieve high accuracy of emotional state detection under demanding requirements of decentralized data and protecting users’ privacy of sensitive information as such classifiers need to see all data. Here comes the federated learning, whose main idea is to create a global classifier without accessing the users’ local data. Therefore, we have developed a federated learning framework for real-time emotion state classification using multi-modal physiological data streams from wearable sensors, called Fed-ReMECS. The main findings of our Fed-ReMECS framework are the development of an efficient and scalable real-time emotion classification system from distributed multimodal physiological data streams, where the global classifier is built without accessing (privacy protection) the users’ data in an IoT environment. The experimental study is conducted using the popularly used multi-modal benchmark DEAP dataset for emotion classification. The results show the effectiveness of our developed approach in terms of accuracy, efficiency, scalability and users’ data privacy protection.

**DATASET** : `DEAP dataset` is required. The experiment is conducted using the `Electrodermal activity(EDA) + Respitory Belt (RB) measurements taken from DEAP dataset`. To download `DEAP dataset` click on : https://www.eecs.qmul.ac.uk/mmv/datasets/deap/download.html


## Installation: 
- Programming language
  - `Python 3.6`

- Operating system
  - `Ubuntu 18.04 (64 bit)` 

- Required packages
  - `Keras` 
  - `Tensorflow` &#8592; for developing the `neural network`.
  - `Scikit-Learn` &#8592; for model's performance matrics. 
  - `paho-mqtt` &#8592; for `MQTT` protocol implementations. 
  - `Konsole - KDE's Terminal Emulator` &#8592; Terminal emulator.
  -  `Mosquitto MQTT Broker`
  
- Installation steps:
  - Step 1: Install `Anaconda`. 
  - Step 2: Create a `virtual environment` in Anaconnda using the given `yml` environment file.
  - Step 3: Install `mosquitto broker`
      - `sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa`
      - `sudo apt-get update`
      - `sudo apt-get install mosquitto`
      - `sudo apt-get install mosquitto-clients`
      - `sudo apt clean`
  - Step 4: Open `terminal`, and `activate environment`.
  - Step 5: Run `bash trigger-clients.sh`
  - Step 6: Enter the number of `clients` you want. 
  - Step 7: Enjoy the visuals :wink:.


## NOTE*: Please feel free to use the code by giving proper citation and star to this repository.

# Cite this work: 
    @article{NANDI2022,
    title = {A federated learning method for real-time emotion state classification from multi-modal streaming},
    journal = {Methods},
    year = {2022},
    issn = {1046-2023},
    doi = {https://doi.org/10.1016/j.ymeth.2022.03.005},
    url = {https://www.sciencedirect.com/science/article/pii/S104620232200072X},
    author = {Arijit Nandi and Fatos Xhafa}
    }


## 📝 License

Copyright © [Arijit](https://github.com/officialarijit).
This project is MIT licensed.
