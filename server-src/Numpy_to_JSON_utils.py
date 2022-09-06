import numpy as np
import codecs, json
from json import JSONEncoder


class Numpy2JSONEncoder(json.JSONEncoder):
    '''
    This class is to convert the Numpy format Tensorflow Model Weights into JSON format
    to send it to the server for Federated Averaging
    '''
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)



def json2NumpyWeights(data):
    '''
    This function is to decode the JSON format Model weights to Tensorflow model suitable
    Numpy for mat so that , model.set_weights(name_variable) can be used properly to set model weights
    '''
    decodedGlobalWeights = list()
    decodedGlobalWeights = json.loads(data)

    FinalWeight= list()
    for i in range(len(decodedGlobalWeights)):
        FinalWeight.append(np.array(decodedGlobalWeights[i]))

    return FinalWeight


def EagerTensor2Numpy(data):
    '''
    This Function is to convert Eager Tensor to Numpy ndarray
    After that this is used for JSON serializable to send it to the Global and local Server
    '''
    npWeightsMat = list()
    for i in range(len(data)):
        val = data[i].numpy()
        npWeightsMat.append(val)

    return npWeightsMat


def global_weights_mul_lr(data, learning_rate):
    '''
    This function multiplies the averaged weights with the learning rate after FedAvg of locall models weights
    '''
    tmp_global_weights = list()
    for i in range(len(data)):
        val = data[i]*learning_rate
        tmp_global_weights.append(val)
    return tmp_global_weights
