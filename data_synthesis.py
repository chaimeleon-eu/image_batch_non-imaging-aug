import os.path

from sdv.tabular import GaussianCopula,CTGAN,CopulaGAN,TVAE
import pandas as pd
import numpy as np

def gaussian_copula(data,n):
    ## gaussian copula
    model = GaussianCopula()
    model.fit(data)
    return model.sample(n)

def ctgan(data,n):
    model = CTGAN()
    model.fit(data)
    return model.sample(n)

def copula_gan(data,n):
    model = CopulaGAN()
    model.fit(data)
    return model.sample(n)

def tvae(data,n):
    model = TVAE()
    model.fit(data)
    return model.sample(n)

def synthesis(data_dir,select_models,num_samples,output_dir):

    models = {'gaussian_copula':gaussian_copula,
              'ctgan': ctgan,
              'copula_gan': gaussian_copula,
              'tvae': tvae,
              }

    data = pd.read_csv(data_dir)
    if 'Unnamed: 0' in data.columns:
        data = data.drop('Unnamed: 0',axis=1)

    print('Reference data loaded. %i Training Samples. '%data.shape[0])
    print('%i columns below will be synthesized: '%data.shape[1])
    print(data.columns)

    select_models = select_models.split(',')

    print('Synthesis algorithms include: %s. '%select_models)


    for model in select_models:
        model = model.strip()
        if model not in models.keys():
            raise ValueError('%s not in the available model list. Please select from gaussian_copula, ctgan, copula_gan and tvae',)
        print('Begin synthesis using %s'%model)
        synthetic_data = models[model](data,num_samples)
        # synthetic_data['id'] = ['syn%s'%(str(k).zfill(4)) for k in range(1000)]
        synthetic_data['id'] = np.arange(num_samples)
        output_name = os.path.join(output_dir,'%s.csv'%(model))
        synthetic_data.to_csv(output_name)
        print('End of synthesis using %s. Data are saved to %s' % (model,output_name))

