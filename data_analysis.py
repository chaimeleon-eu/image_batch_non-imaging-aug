import pandas as pd
import numpy as np

import json
from tqdm import tqdm
from sklearn import  svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scipy.stats import  wilcoxon

def show_figure(f):
    '''
    Decorator to change fig.show() behavior.
    '''
    def wrapper():
        import matplotlib.pyplot as plt
        f()  # call the original fig.show(), remove this line if there is no need to run fig.show()
        plt.show()

    return wrapper

def plot_foobar():
    # fancy plotting routing in a package
    import matplotlib.pyplot as plt

    fig = plt.figure()
    plt.plot([1, 2], [3, 4])

    fig.show = show_figure(fig.show)  # assign a decorator

    return fig

# def NumericalAnalysis(data,synthetic_data,key_fields,sensitive_fields,
#                       ):
#     score = NumericalMLP.compute(
#         real_data=data,
#         synthetic_data=synthetic_data,
#         key_fields=key_fields,
#         sensitive_fields=sensitive_fields
#     )
#     print('The attribute inference attack safe score is ',score)
#
# def MIA(data,synthetic_data,metadata,numerical_match_tolerance=0.1,
#
#         ):
#
#     score = NewRowSynthesis.compute(
#         real_data=data,
#         synthetic_data=synthetic_data,
#         metadata=metadata,
#         numerical_match_tolerance=numerical_match_tolerance,
#         synthetic_sample_size=10_000
#     )
#     print('The membership inference attack safe score is ',score)



def ML(data,synthetic_data,label_col='class',id_col=None,cross_validation=5
       ):
    SVM = svm.SVC()
    synthetic_y = synthetic_data[label_col]
    synthetic_data = synthetic_data.drop([label_col], axis=1)
    y = data[label_col]
    data = data.drop([label_col], axis=1)

    if id_col is not None:
        synthetic_data = synthetic_data.drop([id_col], axis=1)
        data = data.drop([id_col], axis=1)
    print('--------%i fold cross validation begins--------'%cross_validation)
    acc_avg = 0
    acc_avg_aug = 0
    count = 0
    for i in tqdm(range(cross_validation)):


        X_train, X_test, y_train, y_test = train_test_split(data, y, test_size = 0.5)


        classification_model = SVM.fit(X_train,
                                       y_train,)
        pred = classification_model.predict(X_test)

        classification_model = SVM.fit(np.concatenate([X_train,synthetic_data]),
                                       np.concatenate([y_train,synthetic_y]),)
        pred2 = classification_model.predict(X_test)

        acc1 = accuracy_score(y_test, pred)
        acc2 = accuracy_score(y_test, pred2)

        acc_avg += acc1
        acc_avg_aug += acc2

        ##ttest
        correct_values = np.array(y_test==pred,dtype='int')
        correct_values_aug = np.array(y_test == pred2,dtype='int')
        t, p = wilcoxon(correct_values,correct_values_aug)
        if acc2 > acc1 and p <=0.05:
            count += 1

    print('--------%i fold cross validation is finished--------'%cross_validation)
    print('--------Average classification accuracy is %0.2f--------' % (acc_avg/cross_validation))
    print('--------Average classification accuracy after '
          'synthetic data augmentation is %0.2f--------' % (acc_avg_aug/cross_validation))

    print('--------In %i out of %i repeated cross validations, \n'
          'the synthetic data improved the classification performance significantly--------'%(count,cross_validation))

def cal_metrics(data_dir,syn_dir,
                label_col=None,id_col=None,cross_validation=6):
    data = pd.read_csv(data_dir)
    synthetic_data = pd.read_csv(syn_dir)


    if 'Unnamed: 0' in data.columns:
        data = data.drop('Unnamed: 0',axis=1)

    if 'Unnamed: 0' in synthetic_data.columns:
        synthetic_data = synthetic_data.drop('Unnamed: 0',axis=1)

    ML(data,synthetic_data,label_col,id_col,cross_validation)

