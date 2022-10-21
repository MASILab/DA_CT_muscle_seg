from unittest import case
import numpy as np
import cv2
import os
import nibabel as nib 
from PIL import Image

def cal_stats(img_file,res_file):
    case_info_dict = {}
    case_info_dict['snapshot'] = {}
    case_info_dict['result'] = {}
    case_info_dict['file_name'] = os.path.basename(img_file).split('.')[0]
    case_info_dict['snapshot']['img_pred'] = img_file.replace('.nii.gz','.png')
    case_info_dict['result']['mean_intensity_list'] = []
    case_info_dict['result']['std_list'] = []
    case_info_dict['result']['area_list'] = []

    img = nib.load(img_file).get_fdata()
    res = nib.load(res_file).get_fdata()

    sx,sy = nib.load(img_file).header.get_zooms()
    for label in [1,2,3,4]:
        area = np.sum(res == label)
        if area == 0:
            case_info_dict['result']['mean_intensity_list'].append(np.nan)
            case_info_dict['result']['std_list'].append(np.nan)
            case_info_dict['result']['area_list'].append(np.nan)
        else:
            case_info_dict['result']['mean_intensity_list'].append(np.nanmean(img[res == label]))
            case_info_dict['result']['std_list'].append(np.nanstd(img[res == label]))
            case_info_dict['result']['area_list'].append(np.sum(img[res == label]) * sx * sy)

    return case_info_dict


def vis_concat_img(img_file,res_file):
    img = nib.load(img_file).get_fdata()
    res = nib.load(res_file).get_fdata()

    img[img < -200] = -200
    img[img > 500] = 500
    img = ((img - np.min(img)) / (np.max(img) - np.min(img)) * 255).astype(np.uint8)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB).astype(np.uint8)

    overlay_res = vis_label(img,res)
    final_img = np.hstack([img,np.array(overlay_res)[:,:,::-1]])
    cv2.imwrite(img_file.replace('.nii.gz','.png'),final_img)

def vis_label(input_img, label_img):
    color_leg = [[255,30,30],[30,178,252],[255,81,255],[158,191,9],[40,0,242]]

    label_img_rgb = input_img.copy()
    input_img_rgb = input_img.copy()

    label_img = label_img.astype(np.uint8)

    for i, class_label in enumerate([1,2,3,4]):

        label_img_rgb[:,:,0][np.where(label_img == class_label)] = color_leg[i][0]
        label_img_rgb[:,:,1][np.where(label_img == class_label)] = color_leg[i][1]
        label_img_rgb[:,:,2][np.where(label_img == class_label)] = color_leg[i][2]

    # save_dir = os.path.join(vis_png_dir,res_folder)

    overlay_res = Image.blend(Image.fromarray(input_img_rgb.astype(np.uint8)), Image.fromarray(label_img_rgb.astype(np.uint8)), 0.6)

    return overlay_res





