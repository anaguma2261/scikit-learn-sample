#coding:utf-8

import numpy
import sys
import pickle
from sklearn.linear_model import Ridge
from sklearn.cross_validation import cross_val_score

DELIMITOR=","


def load_data(data_path="data/YearPredictionMSD.txt"):
    '''
    �f�[�^�̓Ǎ�
    YearPredictionMSD
    https://archive.ics.uci.edu/ml/datasets/YearPredictionMSD
    '''
    
    f = open(	data_path)
    list_data = []
    list_target = []

    for line in f:
        line = line.strip("\n").split(",")
        data = line[1:]
        target = float(line[0])

        data = [float(ele) for ele in data]

        list_data.append(data)
        list_target.append(target)

    f.close()

    return list_target, list_data
    
    
def read_data_with_numpy(data_path="data/YearPredictionMSD.txt"):
    '''
    numpy���g�����Ǎ�
    YearPredictionMSD
    https://archive.ics.uci.edu/ml/datasets/YearPredictionMSD
    '''
    data = numpy.loadtxt(data_path, delimiter=DELIMITOR)
    target = data[:, 0]
    data = data[:, 1:]

    return target, data
    

    
def ridge_tuning_and_training(data, target, cv_number=10):
    '''
    ���b�W��A�̃O���b�h�T�[�`�{CV�{�ŗǃp�����[�^�ł̊w�K
    '''
    
    max_score = -1 * sys.maxint
    max_alpha = 0
    
    #�O���b�h�T�[�`
    for alpha in [10**i for i in xrange(-4,5)]:
    
        #���b�W��A�̃C���X�^���X����
        model = Ridge(alpha=alpha)
        
        #�������� n_jobs=-1�Ń}���`�R�A
        cv_scores = cross_val_score(model,
                           data,
                           target,
                           cv=cv_number,
                           scoring='mean_squared_error',
                           n_jobs=-1)
                           
        #��������̊e�w�K�̕��ϒl�v�Z
        score = numpy.mean(cv_scores)
        
        print "alpha:{} score:{}".format(alpha, score)
        
        #�X�R�A���ǂ�������p�����^���L��
        if score > max_score:
            max_score = score
            max_alpha = alpha
            
    print "best_alpha:{} best_score:{}".format(max_alpha, max_score)
    #�ŗǃp�����[�^�Ŋw�K
    model = Ridge(alpha=max_alpha)
    model.fit(data, target)
    
    return model
    
if __name__ == "__main__":

    target, data = load_data()
    ridge_model = ridge_tuning_and_training(data, target, cv_number=10)
    
    exit()
    
    with open("ridge_model", "w") as f:
        pickle.dump(ridge_model)