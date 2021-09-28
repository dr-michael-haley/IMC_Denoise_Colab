# -*- coding: utf-8 -*-
"""
python scripts/Predict_IMC_Denoise_script.py --Raw_img_name 'D:\IMC analysis\Raw_IMC_dataset\H1527528\141Pr-CD38_Pr141.tiff' 
                                             --Denoised_img_name 'D:\IMC analysis\Denoised_IMC_dataset\141Pr-CD38_Pr141.tiff' 
                                             --weights_name "weights_CD38.hdf5"   
                                             --neighbours '4' --n_lambda '5' --slide_window_size '3' 
"""

import tifffile as tp
from IMC_Denoise.IMC_Denoise_main.DeepSNF import DeepSNF
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--Raw_img_name", help = "the raw IMC image. tiff format")
parser.add_argument("--Denoised_img_name", help = "the denoised IMC image. tiff format")
parser.add_argument("--weights_name", help = "trained network weights. hdf5 format")
parser.add_argument("--weights_save_directory", help = "location where 'weights_name' and 'loss_name' saved. If the \
                    value is None, the files will be saved in the current file folder.", default = None)
parser.add_argument("--n_neighbours", help = "DIMR algorithm parameter", default = 4, type = int)
parser.add_argument("--n_lambda", help = "DIMR algorithm parameter", default = 5)
parser.add_argument("--slide_window_size", help = "DIMR algorithm parameter", default=3, type = int)
                    
args = parser.parse_args()
print(args)

deepsnf = DeepSNF(weights_name = args.weights_name,
                  weights_dir = args.weights_save_directory,
                  is_load_weights = True) # in prediction, this parameter should be set as true so that the trained weights can be loaded.  

Img_raw = tp.imread(args.Raw_img_name)
Img_DIMR_DeepSNF = deepsnf.perform_IMC_Denoise(Img_raw, n_neighbours = args.n_neighbours, n_lambda = args.n_lambda, window_size = args.slide_window_size)

if tp.imsave(args.Denoised_img_name, Img_DIMR_DeepSNF.astype('float32')):
    print('The denoised image has been saved!')