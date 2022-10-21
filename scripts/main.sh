
INPUT_DIR=$1
OUTPUT_DIR=$2

echo $INPUT_DIR
echo $OUTPUT_DIR

python3  /CODE/thigh_muscle_seg_main.py \
--dataroot $INPUT_DIR \
--netG unet_256 \
--gpu_ids 0 \
--eval \
--epoch latest \
--checkpoints_dir /MODEL \
--results_dir $OUTPUT_DIR 

# python3  /home/local/VANDERBILT/yangq6/myProject/BLSA_leg/code/python/TBME_2022/singularity/src/thigh_muscle/python/thigh_muscle_seg_main.py \
# --dataroot $INPUT_DIR \
# --netG unet_256 \
# --gpu_ids 0 \
# --eval \
# --epoch latest \
# --checkpoints_dir /nfs/masi/yangq6/BLSA_leg/experiment/IntraDA_v04/IntraDA_v04 \
# --results_dir $OUTPUT_DIR 
