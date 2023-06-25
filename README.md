# A Docker-Based Federated Learning Framework Design and Deployment for Multi-modal Data Stream Classification

## Publication link: https://link.springer.com/article/10.1007/s00607-023-01179-5

`ABSTRACT` 
  In the high-performance computing (HPC) domain, federated learning has gained immense popularity. Especially in emotional and physical health analytics and experimental facilities. Federated learning is one of the most promising distributed machine learning frameworks because it supports data privacy and security by not sharing the clients’ data but instead sharing their local models. In federated learning, many clients explicitly train their machine learning/deep learning models (local training) before aggregating them as a global model at the global server. However, the FL framework is difficult to build and deploy across multiple distributed clients due to its heterogeneous nature. We developed Docker-enabled federated learning (DFL) by utilizing client-agnostic technologies like Docker containers to simplify the deployment of FL frameworks for data stream processing on the heterogeneous client. In the DFL, the clients and global servers are written using TensorFlow and lightweight message queuing telemetry transport protocol to communicate between clients and global servers in the IoT environment. Furthermore, the DFL’s effectiveness, efficiency, and scalability are evaluated in the test case scenario where real-time emotion state classification is done from distributed multi-modal physiological data streams under various practical configurations.


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
  



## NOTE*: Please feel free to use the code by giving proper citation and star to this repository.

# Cite this work: 
    @article{
    }


## 📝 License

Copyright © [Arijit](https://github.com/officialarijit).
This project is MIT licensed.
