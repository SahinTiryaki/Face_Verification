# Face Verification


## Demo
<div align="center">
<img src="media/demo.gif" width="80%"/> 
</div>
<br>

## Method
<li>Detect Faces with MediaPipe</li>
<li>Extract embeddings with FaceNet</li>
<li>Compare faces with cosine similarity function</li>


## Description
I use pre-trained FaceNet network that is Siamese Network. After getting pre-processed face image, FaceNet extract 128x1 dimensional feature vector called embedding. After pre-process the incoming image and extract the embedding, I compare the embedding of incoming images . If I the threshold value is exceeded , I label the user is the correct person and verification is successful.

## Dependencies

<li>keras==2.7.0 </li>
<li> mediapipe==0.8.9</li>
<li>opencv-python==4.5</li>
<li>tensorflow==2.7.0 </li>
<li>flask</li>

## How to run?
### Conda
```

conda create -n face python=3.7 
conda activate face
pip install -r requirements.txt
python app.py
```

### Docker
```
sudo docker build --tag face-verification .
sudo docker run -it -d -p 8080:8080 --name face-verify --restart always  face-verification 

```
