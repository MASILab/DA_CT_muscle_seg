**Transferring Inter-modality Information for Thigh CT Slice Muscle group Segmentation with Self Training** 
---
#### Copyright
The contents covered by this repository, including code and pretrained models in the docker container, are free for noncommercial usage (CC BY-NC 4.0). Please check the LICENSE.md file for more details of the copyright information.

---
#### Citation
---
#### Quick start

##### Get the singularity image
- Please download the singularity from this [link](https://drive.google.com/file/d/1tPkFerhatzN9CwJk9nSU8dMh8_7XeR0c/view?usp=sharing)
- Prepare the data used for the singularity.
  - The data should have image dimensions 256 x 256 pixels
  - The data only include left/right mid-thigh image. Please check the paper for reference.
  - The data should be saved in .nii.gz
  - There is no restriction for the name of input data
  - Currently we only support GPU.
- Refer to following code snippets to prepare INPUTS and OUTPUTS directory and inference the muscle group segmentation in .
```
INPUTS=${HOME}/INPUTS
OUTPUTS=${HOME}/OUTPUTS
singularity_file=/path/to/download/singularity/file
mkdir ${INPUTS} ${OUTPUTS}
singularity run --contain --nv --bind ${INPUTS}:/INPUTS --bind ${OUTPUTS}:/OUTPUTS $singularity_file
```
---
##### Disclaimer
The code and data of this repository are provided to promote reproducible research. They are not intended for clinical care or commercial use.

The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.