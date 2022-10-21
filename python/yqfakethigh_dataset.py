import os
from base_dataset import BaseDataset, get_transform
import random
from glob import glob
import nibabel as nib
import numpy as np
import torchvision.transforms as transforms
import torch


class YQFakethighDataset(BaseDataset):
    """
    """
    @staticmethod
    def modify_commandline_options(parser, is_train):
        """Add new dataset-specific options, and rewrite default values for existing options.

        Parameters:
            parser          -- original option parser
            is_train (bool) -- whether training phase or test phase. You can use this flag to add training-specific or test-specific options.

        Returns:
            the modified parser.

        By default, the input channel and output are both 1
        """
        parser.set_defaults(input_nc=1, output_nc=1)
        return parser

    def __init__(self, opt):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseDataset.__init__(self, opt)


        self.A_dir = opt.dataroot
        input_nc  = opt.input_nc

        self.A_paths = sorted(glob(os.path.join(self.A_dir,'*.nii.gz')))

        self.A_size = len(self.A_paths)

        self.transform_A = get_transform(self.opt, grayscale=(input_nc == 1))

    def preProc_CT(self,img):
        img[img < -200] = -200
        img[img > 500] = 500

        img = np.squeeze(img)

        # return (img - np.min(img)) / (np.max(img) - np.min(img))

        return (img - np.min(img)) / (np.max(img) - np.min(img))


    def __getitem__(self, index):
        """
        """
        A_path = self.A_paths[index % self.A_size]  # make sure index is within then range
        A_img = nib.load(A_path).get_fdata()
        A_img = self.preProc_CT(A_img)
        A = torch.from_numpy(A_img)
        A = A * 2 - 1 

        # # apply image transformation
        # A = self.transform_A(A_img)
        A = torch.unsqueeze(A,0).float()

        return {'A': A, 'A_paths': A_path}

    def __len__(self):
        """
        Return the total number of images in the dataset.
        """
        return self.A_size

