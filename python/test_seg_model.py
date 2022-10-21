from base_model import BaseModel
import networks
import torch
import os
import numpy as np


class TestSegModel(BaseModel):
   
    @staticmethod
    def modify_commandline_options(parser, is_train=True):
        """Add new dataset-specific options, and rewrite default values for existing options.

        Parameters:
            parser          -- original option parser
            is_train (bool) -- whether training phase or test phase. You can use this flag to add training-specific or test-specific options.

        Returns:
            the modified parser.

        The model can only be used during test time. It requires '--dataset_mode single'.
        You need to specify the network using the option '--model_suffix'.
        """
        assert not is_train, 'TestModel cannot be used during training time'
        parser.add_argument('--model_suffix', type=str, default='_A', help='In checkpoints_dir, [epoch]_net_G[model_suffix].pth will be loaded as the generator.')

        return parser

    def __init__(self, opt):
        """Initialize the segmentation model.

        """
        BaseModel.__init__(self, opt)
        self.netS = networks.define_G(int(opt.input_nc_seg), int(opt.output_nc_seg), opt.ngf, opt.netG,
                                      opt.norm, not opt.no_dropout, opt.init_type, opt.init_gain, self.gpu_ids)

        self.model_names = ['S' + opt.model_suffix]  # only generator is needed.

        # assigns the model to self.netG_[suffix] so that it can be loaded
        # please see <BaseModel.load_networks>
        setattr(self, 'netS' + opt.model_suffix, self.netS)  # store netG in self.


    def get_model(self):
        return self.netS
    
    def get_optimizer(self):
        return self.optimizer

    def set_input(self, input):
        """Unpack input data from the dataloader and perform necessary pre-processing steps.

        Parameters:
            input: a dictionary that contains the data itself and its metadata information.

        We need to use 'single_dataset' dataset mode. It only load images from one domain.
        """
        self.fake = input['A'].to(self.device)
        self.image_paths = input['A_paths']

    def forward(self):
        """Run forward pass."""
        self.real = self.netS(self.fake)  # S(img)
        _, self.real = torch.max(self.real.data,dim=1,keepdim=True)

    def optimize_parameters(self):
        """Calculate losses, gradients, and update network weights; called in every training iteration"""
        pass

    def test(self):
        with torch.no_grad():
            self.forward()

    def get_res(self):
        return np.squeeze(self.real.cpu().numpy()),self.image_paths[0]