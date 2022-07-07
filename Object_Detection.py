## For reference: https://www.youtube.com/watch?v=1LCb1PVqzeY
import cv2
import cvzone
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

net = cv2.dnn.readNet('yolov4-obj_2000.weights', 'yolov4-obj_2000.cfg')

classes = []
with open("classes.txt", "r") as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

def img_overlay(background, overlay, x_offset, y_offset):
    y1, y2 = y_offset, y_offset + overlay.shape[0]
    x1, x2 = x_offset, x_offset + overlay.shape[1]

    alpha_s = overlay[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s
    

    for c in range(0, 3):
        background[y1:y2, x1:x2, c] = (alpha_s * overlay[:, :, c] +
                                   alpha_l * background[y1:y2, x1:x2, c])

    return background

def gen_frames():  # generate frame by frame from camera
    while True:
        _, img = cap.read()                
        black_img = cv2.imread('tableImage.png', -1)
        # black_img = img

        width = 1280
        height = 780
        dim = (width, height)
        black_img = cv2.resize(black_img, dim, interpolation = cv2.INTER_AREA)        
        

        height, width, _ = black_img.shape
        
        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)
        
        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.7:                
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.7, 0.4)
        

        if len(indexes)>0:
            image_front = cv2.imread('pikesPlaceInfo.png', -1)
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i],2))
                color = colors[i]                      
                # cv2.rectangle(black_img, (x,y), (x+w, y+h), color, 2)
                # cv2.putText(black_img, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)            
                
                # First step                
                x_offset = x
                y_offset = y
                
                
                if label=='SingleOriginColumbia':
                    image_front = cv2.imread('singleOriginInfo.png', -1)
                elif label=='Volluto':
                    image_front = cv2.imread('vollutoInfo.png', -1)
                elif label=='PikePlaceRoast':
                    image_front = cv2.imread('pikesPlaceInfo.png', -1)
                
                image_front = cv2.resize(image_front, (200, 200), interpolation = cv2.INTER_AREA)        

                print(color)

                if y>80 and y<570 and x>100 and x<1050:
                    black_img = img_overlay(black_img, image_front, x_offset + 100, y_offset)
                

        
        
        alpha = 1
        # added_image = cv2.addWeighted(black_img[150:250,150:250,:], 1, source1[0:100,0:100,:], 1, 0)
        # black_img[150:250,150:250] = added_image

        key = cv2.waitKey(1)
        ret, buffer = cv2.imencode('.jpg', black_img)
        black_img = buffer.tobytes()
        
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + black_img + b'\r\n')  # concat frame one by one and show result
        if key==27:
            break


    


@app.route('/video_feed')
def video_feed():
    
        #Video streaming route. Put this in the src attribute of an img tag
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)



## Section below utilizes built in native video viewer rather than Flask. 
# while True:
#     _, img = cap.read()
#     height, width, _ = img.shape

#     blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
#     net.setInput(blob)
#     output_layers_names = net.getUnconnectedOutLayersNames()
#     layerOutputs = net.forward(output_layers_names)

#     boxes = []
#     confidences = []
#     class_ids = []

#     for output in layerOutputs:
#         for detection in output:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.7:                
#                 center_x = int(detection[0]*width)
#                 center_y = int(detection[1]*height)
#                 w = int(detection[2]*width)
#                 h = int(detection[3]*height)

#                 x = int(center_x - w/2)
#                 y = int(center_y - h/2)

#                 boxes.append([x, y, w, h])
#                 confidences.append((float(confidence)))
#                 class_ids.append(class_id)

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.7, 0.4)

#     if len(indexes)>0:
#         for i in indexes.flatten():
#             x, y, w, h = boxes[i]
#             label = str(classes[class_ids[i]])
#             confidence = str(round(confidences[i],2))
#             color = colors[i]            
#             cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
#             cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)

#     cv2.imshow('Image', img)
#     key = cv2.waitKey(1)
#     if key==27:
#         break

# cap.release()
# cv2.destroyAllWindows()