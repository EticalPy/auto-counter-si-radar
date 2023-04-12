from ultralytics import YOLO
import cv2
import cvzone
import math
import time
from sort import *


'''cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)'''
cap = cv2.VideoCapture('../Video/caretera_proba4.mp4')
model = YOLO('../Yolo-Weights/yolov8s.pt')
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
traker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

limits = [0, 550, 580, 550]
limits1 = [640, 520, 1120, 520]
Numaratoare = []
Numaratoare1 = []
prev_frame = 0
new_frame = 0


while True:
    new_frame = time.time()
    success, img = cap.read()
    height = img.shape[0]
    width = img.shape[1]
    mask = np.zeros((height, width), dtype=np.uint8)
    pts = np.array([[[465, 367], [1000, 367], [1280, 720], [0, 720], [0, 553]]])
    cv2.fillPoly(mask, pts, 255)
    imgRegion = cv2.bitwise_and(img, img, mask=mask)
    Grafica = cv2.imread("graphics1.png", cv2.IMREAD_UNCHANGED)
    Grafica2 = cv2.imread("graphics2.png", cv2.IMREAD_UNCHANGED)
    img = cvzone.overlayPNG(img, Grafica, (0, 0))
    img = cvzone.overlayPNG(img, Grafica2, (823, 0))
    rezultat= model(imgRegion, stream=True, conf=0.25)
    detectia = np.empty((0, 5))
    for r in rezultat:
        boxes = r.boxes
        for box in boxes:
            #Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            lungime, inaltime = x2 - x1, y2 - y1

            conf = math.ceil((box.conf[0] * 100)) / 100
            clasa = int(box.cls[0])
            clasa_de_interes = classNames[clasa]

            if clasa_de_interes == "car" or clasa_de_interes == "truck" or clasa_de_interes == "bus" \
                and conf > 0.25:
                currentArray = np.array([x1, y1, x2, y2, conf])
                detectia= np.vstack((detectia, currentArray))

    rezultatTraker = traker.update(detectia)
    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 3)
    cv2.line(img, (limits1[0], limits1[1]), (limits1[2], limits1[3]), (0, 255, 0), 3)
    for rezultat in rezultatTraker:
        x1, y1, x2, y2, id = rezultat
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        lungime, inaltime = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, lungime, inaltime), l=8, t=4, rt=2, colorR=(255, 0, 0), colorC=(0, 0, 255) )
        cvzone.putTextRect(img, f'{int(id)}', (max(0, x1), max(25, y1)), scale=1, thickness=2, offset=6, colorR=(255, 0, 0))
        cx, cy = x1 + lungime // 2, y1 + inaltime // 2
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED )

        if limits[0] < cx < limits[2] and limits[1] -15 < cy < limits[1] +15:
            if Numaratoare.count(id) == 0:
                Numaratoare.append(id)
        if limits1[0] < cx < limits1[2] and limits1[1] -15 < cy < limits1[1] +15:
            if Numaratoare1.count(id) == 0:
                Numaratoare1.append(id)


    cv2.putText(img, str(len(Numaratoare)), (270, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 6)
    cv2.putText(img, str(len(Numaratoare1)), (933, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 6)
    fps = 1 / (new_frame - prev_frame)
    prev_frame = new_frame
    print(int(fps))

    cv2.imshow("Imagine", img)
    #cv2.imshow("Masca", mask)
    cv2.waitKey(1)