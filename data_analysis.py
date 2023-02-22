import pandas as pd
import numpy as np
from sdmetrics.reports.single_table import DiagnosticReport,QualityReport
import json
from sdmetrics.single_table import CategoricalKNN,NumericalMLP
from sklearn import  svm
from sklearn.metrics import classification_report,accuracy_score
from sdmetrics.single_table import NewRowSynthesis

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

def NumericalAnalysis(data,synthetic_data,key_fields,sensitive_fields,
                      ):
    score = NumericalMLP.compute(
        real_data=data,
        synthetic_data=synthetic_data,
        key_fields=key_fields,
        sensitive_fields=sensitive_fields
    )
    print('The attribute inference attack safe score is ',score)

def MIA(data,synthetic_data,metadata,numerical_match_tolerance=0.1,

        ):

    score = NewRowSynthesis.compute(
        real_data=data,
        synthetic_data=synthetic_data,
        metadata=metadata,
        numerical_match_tolerance=numerical_match_tolerance,
        synthetic_sample_size=10_000
    )
    print('The membership inference attack safe score is ',score)



def ML(data,synthetic_data,label_col='class',id_col=None,
       ):
    SVM = svm.SVC()
    synthetic_y = synthetic_data[label_col]
    synthetic_data = synthetic_data.drop([label_col],axis=1)
    y = data[label_col]
    data = data.drop([label_col],axis=1)

    if id_col is not None:
        synthetic_data = synthetic_data.drop([id_col],axis=1)
        data = data.drop([id_col],axis=1)

    classification_model = SVM.fit(synthetic_data,
                                   synthetic_y,)
    pred = classification_model.predict(data)
    print('The Train-on-Synthetic-Test-on-Real efficiency is',accuracy_score(y,pred))

def cal_metrics(data_dir,syn_dir,metric,meta_dir,
                label_col=None,id_col=None,key_fields=None,
                sensitive_fields=None,numerical_match_tolerance=0.1):
    data = pd.read_csv(data_dir)
    synthetic_data = pd.read_csv(syn_dir)

    with open(meta_dir) as fp:
        metadata = json.load(fp)
    if 'Unnamed: 0' in data.columns:
        data = data.drop('Unnamed: 0',axis=1)

    if 'Unnamed: 0' in synthetic_data.columns:
        synthetic_data = synthetic_data.drop('Unnamed: 0',axis=1)

    metrics = {'diagnostic_report':DiagnosticReport,
               'quality_report':QualityReport,
                'attribute_attack':NumericalAnalysis,
               'membership_attack':MIA,
               'ml_efficiency':ML}


    if metric not in metrics.keys():
        raise ValueError('%s not in the available metric list. Please select from diagnostic_report, quality report, attribute_attack, membership_attack, ml_efficiency',)
    if 'report' in metric:
        report = metrics[metric]()
        report.generate(data, synthetic_data, metadata)
    elif metric == 'attribute_attack':
        key_fields = [id_col]
        sensitive_fields = sensitive_fields.split(',')
        metrics[metric](data,synthetic_data,key_fields,sensitive_fields)
    elif metric == 'membership_attack':
        metrics[metric](data,synthetic_data,metadata,numerical_match_tolerance)
    elif metric == 'ml_efficiency':
        metrics[metric](data,synthetic_data,label_col,id_col)

