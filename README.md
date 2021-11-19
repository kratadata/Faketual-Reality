### First Order Motion Model for Retargeting Videos Exhibition

### Installation
The code supports python3. 
I suggest to use a conda environment. This way, you would have all the packages needed into the same environment (Were you able to create it at the end?).


Install the dependencies by running
```
pip install -r requirements.txt
```

Install also pytorch and torchvision with 
```
conda install pytorch==1.0.0 torchvision==0.2.1 -c pytorch
```
You also need to clone the library for face alignment:
```
git clone https://github.com/1adrianb/face-alignment
cd face-alignment
pip install -r requirements.txt
python setup.py install
```

### Cuda and python version 
I am now using <br>
Python 3.7 <br>
Cuda 10.0 <br>
Cuda Drivers 410.48 <br>
Here https://forums.developer.nvidia.com/t/rtx-2080ti-and-cuda-version/83904 I read that CUDA 10.0 should be supported in the 2080Ti graphic card.

### Crop the videos
The script in scripts/preprocess_driving_video.py is responsible to detect and crop the driving videos in a preprocessing step (if needed). <br>
Just run it (change the paths accordingly) like
```
python scripts/preprocess_driving_video.py
```

### Crop the images
The script in scripts/preprocess_images.py is responsible to crop the images to squares in a preprocessing step (if needed). <br>
Just run it (change the paths accordingly) like
```
python scripts/preprocess_images.py
```

### Test the model 
Before testing the model, you need to download the weights that I put here because they were too heavy: <br> https://drive.google.com/file/d/1wjUDZP7rXRAF6hQ4TisZ1YvCRwn-ur5W/view?usp=sharing <br>
Just put the in the folder ```checkpoints``` of the repo. <br>
I wrote a script that selects randomly one video from a folder of many of them, and then synthesize the desired output video.  <br>
```
python scripts/exhibition_script.py
```
For now, the path of the image is hardcoded inside the code. <br>
But if you want I can make it so you just give the path of the image when you type the command. <br>
Something like
```
python scripts/exhibition_script.py
```

Just remember that the code requires that the object in the first frame of the video and in the source image have the same pose

### Enhancement
I added the code for enhancing the generated videos inside the script  <br>
```
python scripts/exhibition_script_enhance.py
```
In order to be able to use this however, some packages are needed. <br>
I installed them with conda: <br>
```
conda install tensorflow-gpu=1.13.1 
conda install keras-base
conda install keras 
```
If any problem about tensorflow is outputted, just install these ones too:
```
conda install tensorflow=1.13.1
conda install tensorflow-base=1.13.1
```
<br>
Moreover, before running the script, you need to download this (https://drive.google.com/file/d/1DSxNFCc9cyeb1tZHuvQTSza81_PCPh46/view?usp=sharing) folder, unzip it and put it inside the folder "Enhance" so you will have the path "Enhance/checkpoints"

### Flask

Copy the files and put them in the main main folder.

To run the server:<br>
```
cd exhibiton-code
export FLASK_APP=server.py
flask run
```

Running on the local server on port 5000. The resulting video is shown under http://127.0.0.1:5000/video





