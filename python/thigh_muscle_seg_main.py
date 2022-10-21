import os
from test_options import TestOptions
from test_seg_model import TestSegModel
from yqfakethigh_dataset import YQFakethighDataset
import nibabel as nib
import torch
from util import *
from report_pdf import MuscleReportGenerator

def create_dataset(opt):
    dataset = YQFakethighDataset(opt)
    dataloader = torch.utils.data.DataLoader(dataset,batch_size=opt.batch_size,shuffle=not opt.serial_batches,num_workers=int(opt.num_threads))
    return dataloader 

def create_model(opt):
    return TestSegModel(opt)

if __name__ == '__main__':
    opt = TestOptions().parse()  # get test options
    # hard-code some parameters for test
   
    dataset= create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)     # create a model given opt.model and other options
    model.setup(opt)                # load the model from save file path
    model.eval()

    for i, data in enumerate(dataset):
        if i >= opt.num_test:  # only apply our model to opt.num_test images.
            break
        model.set_input(data)  # unpack data from data loader
        model.test()           # run inference
        res,file = model.get_res() 
        basename = os.path.basename(file).split('.')[0]
        save_dir = os.path.join(opt.results_dir,basename)
        save_file = os.path.join(save_dir,basename + '_muscle_group.nii.gz')
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir) 
        save_nii = nib.Nifti1Image(res,nib.load(file).affine)
        nib.save(save_nii,save_file)
        cmd = f"cp {file} {os.path.dirname(save_file)}"
        os.system(cmd) 
        img_file = os.path.join(os.path.dirname(save_file),os.path.basename(file))
        print(f"we aleady save the {save_file}")
        print(f"we already copy the original file to {img_file}")

        vis_concat_img(img_file,save_file)
        case_info_dict = cal_stats(img_file,save_file)
        gen = MuscleReportGenerator(case_info_dict)
        gen.draw_report(img_file.replace('.nii.gz','.pdf'))
        print(f"we already generated the pdf {img_file.replace('.nii.gz','.pdf')}")
        


        

      
