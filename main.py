import argparse
from data_analysis import cal_metrics
from data_synthesis import synthesis


class BaseOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.initialized = False

    def initialize(self):
        # experiment target
        self.parser.add_argument("--target", type=str,default='analysis',
                            help="Target of the task. Please choose between synthesis and analysis.")
        self.parser.add_argument('-d',"--data_dir", type=str,
                                 default='/workspace/data.csv',
                            help="File path for the reference dataset. CSV format is required. ")

        # synthesis parameter
        # data_dir,select_models,num_samples,output_dir
        self.parser.add_argument("--select_models", type=str, default='gaussian_copula,ctgan,copula_gan,tvae',
                            help="Models used for the synthesis. Available methods include aussian_copula, ctgan, copula_gan, and tvae. ")
        self.parser.add_argument("--num_samples", type=int, default=1000,
                            help="Number of samples to be synthesized. ")
        self.parser.add_argument("--output_dir", default='/home/chaimeleon/datasets',
                            help="The folder path to save synthetic outputs.")

        # analysis parameter
        # data_dir,syn_dir,metric,meta_dir,label_col=None,id_col=None,key_fields=None,sensitive_fields=None,numerical_match_tolerance=0.1
        self.parser.add_argument('-s',"--syn_dir", type=str,
                                 default='/workspace/tvae_data.csv',
                            help="File path for the synthetic dataset. CSV format is required.")

        self.parser.add_argument("--cross_validation", type=int,
                                 default=5,
                            help="The time for cross validations")
        self.parser.add_argument("--label_col", type=str,
                                 default='class',
                            help="The column name for label. ")
        self.parser.add_argument("--id_col", type=str,
                                 default='id',
                            help="The column name for patient IDs. Patient IDs should be removed for ml efficiency evaluation. ")


        self.initialized = True

    def parse(self):
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()
        args = vars(self.opt)
        print('------------ Options -------------')
        for k, v in sorted(args.items()):
            print('%s: %s' % (str(k), str(v)))
        print('-------------- End ----------------')



        return self.opt



if __name__ == '__main__':
    opt = BaseOptions().parse()
    if opt.target == 'synthesis':
        synthesis(opt.data_dir,opt.select_models,opt.num_samples,opt.output_dir)
    elif opt.target == 'analysis':
        cal_metrics(opt.data_dir, opt.syn_dir,
                    opt.label_col, opt.id_col, opt.cross_validation)

    else:
        raise ValueError('This function is not implemented. Try synthesis or analysis. ')