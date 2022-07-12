## High-Level Technical Overview

There were several steps to the process of creating the POC:

**1. Train Custom Object Detector / Weights File**


([https://youtu.be/mmj3nxGT2YQ](https://youtu.be/mmj3nxGT2YQ))

For our POC, we took 3 types of starbucks coffee pods, and took about 300 photos per pod. The photos were taken with the same background / hand holding the pod that the POC would have when it was running live, and it was important to get the best model possible via this process.

We found it more time efficient to take video and then use ffmpeg to split the video into images rather than manually taking 300 photos....

The Labelimg library was used as a Python CLI tool to manually draw rectangles around each coffee pod within each image.

This dataset was then run in a Google Colab notebook, training for 4-6 hours.

**2. Take trained model .weights file, and serve via Flask App**

([https://youtu.be/1LCb1PVqzeY](https://youtu.be/1LCb1PVqzeY))

With the trained .weights file, we were able to then create a flask app the projected a black background with content showing next to each detected object, based on the object detected.

\*\*Note - The .weights and config files are not included in this repo, and needs to be downloaded and placed into your local repo:

.weights file: https://drive.google.com/file/d/1-1RtrG9SCgaoClp2YkjgiuRM-h3GT5bo/view?usp=sharing

config file (save as yolov4-obj_2000.cfg): https://drive.google.com/file/d/1_0vqjtWNgXbS_Fi-vsCSS7cUx2xdnul-/view

**3. Setup CV2 to display custom content next to detected object.**

When the app starts up, a webcam attached to the projector on the ceiling captures real time video. Then when a pod is detected, a CV2 image is rendered showing a box of information about the coffee pod.

It is worth noting, this project was cut a bit short. We left off setting up a projector on Austin’s ceiling in his garage, and are about to train our final dataset to test with this setup. Videos will be posted in the associated deck.

## Technical Architecture Overview

Currently the app is only run locally.

Setup steps:

1. Install Python, Flask (`pip3 install flask`), CV2 (`pip3 install opencv-python`)
2. Download the .weights and config files listed above and move them to the local repo
3. To start the application, run `python3 Object_Detection.py`. This starts the server, running the app on localhost:5000, where you should see the webcam view.
4. Use a physical pod (or an image of one) and move it in front of the web camera to view the associated image file (singleOriginInfo.png, vollutoInfo.png, pikesPlaceInfo.png) on the screen/projector. 

## Tech Stack

Flask  
Python  
CV2  
YoloV4  
Projector / Webcam

[Tech Documention](https://valtechcom.sharepoint.com/:w:/r/sites/AMER.CXPLAB/_layouts/15/Doc.aspx?action=view&sourcedoc=%7B4d3bd9eb-efc7-429c-b22c-66cf4b640c9c%7D&wdOrigin=TEAMS-ELECTRON.teamsSdk.openFilePreview&wdExp=TEAMS-CONTROL&wdhostclicktime=1657301402502)
