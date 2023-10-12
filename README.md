### First Order Motion Model for Retargeting Videos Exhibition
Creators : @alessiapacca 

### Prequisities
Ubuntu 18.04 Kernel 5.4.0<br>
Python 3.7 <br>
Cuda 10.2 <br>
Cuda Drivers 440.33.01

### Installation
Use Conda environment:

Install packages by running
```
conda install pyqt
sudo apt install ffmpeg
sudo apt-get install libportaudio2
```

Install the dependencies by running
```
pip install -r requirements.txt
```

Install also pytorch and torchvision with 
```
conda install pytorch==1.1.0 mkl==2018 torchvision==0.2.1 cudatoolkit=10.0 -c pytorch
```

Clone the library for face alignment:
```
git clone https://github.com/1adrianb/face-alignment
cd face-alignment
pip install -r requirements.txt
python setup.py install
```

All paths are hard-coded inside of the scripts, make sure you change them before running.

### Crop the videos
The script in scripts/preprocess_driving_video.py is responsible to detect and crop the driving videos in a preprocessing step (if needed). Just run it (change the paths accordingly)
```
python scripts/preprocess_driving_video.py
```

### Crop the images
The script in scripts/preprocess_images.py is responsible to crop the images to squares in a preprocessing step (if needed). Just run it (change the paths accordingly)
```
python scripts/preprocess_images.py
```

### Test the model 
Before testing the model, you need to download the weights: <br> https://drive.google.com/file/d/1wjUDZP7rXRAF6hQ4TisZ1YvCRwn-ur5W/view?usp=sharing <br>
After downloading put the in the folder ```checkpoints``` of the repo. Just remember that the code requires that the object in the first frame of the video and in the source image have the same pose. <br>

```
python scripts/exhibition_script.py
```

### Enhancement
Added the code for enhancing the generated videos inside the script. <br>
```
python scripts/exhibition_script_enhance.py
```
In order to be able to use this however, some packages are needed. <br>
Install them with conda: <br>
```
conda install tensorflow-gpu=1.13.1 
conda install keras-base
conda install keras 
```
If any problem about tensorflow is outputted, just install these ones too:
```
pip install dask==1.2.0
```
<br>
Moreover, before running the script, you need to download this (https://drive.google.com/file/d/1DSxNFCc9cyeb1tZHuvQTSza81_PCPh46/view?usp=sharing) folder, unzip it and put it inside the folder "Enhance" so you will have the path "Enhance/checkpoints"

### Real-Time-Voice-Cloning
Audio generation is heavily based on Corentin Jemine's repository https://github.com/CorentinJ/Real-Time-Voice-Cloning <br>

### Running

```
python /scripts/deep_vocoder.py
```

### Flask

Copy the files and put them in the main main folder.

To run the server:<br>
```
cd exhibiton-code
export FLASK_APP=server.py
flask run
```

Running on the local server http://127.0.0.1:5000/.
