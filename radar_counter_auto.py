import os.path
import shutil
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *
from collections import defaultdict
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def apasa_q_si_salveaza(id_viteza, limita_viteza):
    print("Guardando el archivo velocidades_medias.txt")
    while True:
        key = cv2.waitKey(1)
        if key != -1 and key in [27, ord('q')]:
            fisier_iesire = "resultate"
            try:
                if not os.path.exists(fisier_iesire):
                    os.makedirs(fisier_iesire)
                with open(os.path.join(fisier_iesire, "viteze_medii.txt"), "w") as f:
                    for id_vehicul, viteze_inregistrate in id_viteza.items():
                        viteza_medie = calculeaza_viteza_medie(viteze_inregistrate)

                        if viteza_medie > limita_viteza:
                            f.write(f"ID: {id_vehicul}, Viteza medie: {viteza_medie} km/h\n")

                            # Save vehicle information to text file
                            diferenta_viteza = viteza_medie - limita_viteza
                            salveaza_info_vehicul(id_vehicul=id_vehicul, viteza=viteza_medie, diferenta_viteza=diferenta_viteza)
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")
            else:
                print("Archivo guardado exitosamente")
            break

def distanta_in_metri(pt1, pt2, scala):
    dx = (pt2[0] - pt1[0]) * scala
    dy = (pt2[1] - pt1[1]) * scala
    return math.sqrt(dx**2 + dy**2)

def calculeaza_viteza_medie(viteze_inregistrate):
    if len(viteze_inregistrate) != 0:

        return sum(viteze_inregistrate) / len(viteze_inregistrate)

def salveaza_info_vehicul(id_vehicul, viteza, diferenta_viteza):
    info_vehicul = f"ID: {id_vehicul}, Viteza: {viteza} km/h, Diferenta: {diferenta_viteza} km/h\n"
    with open("vehicle_info.txt", "a+",) as file:
        file.write(info_vehicul)
def salveaza_foto_vehicul(id_vehicul, img, img_copy, x1, y1, x2, y2):
    directory = "rezultate/auto"
    if not os.path.exists(directory):
        os.makedirs(directory)

    cropped_vehicle = img_copy[y1:y2, x1:x2]
    vehicle_image_path = os.path.join(directory, f"vehicle_{id_vehicul}.png")
    cv2.imwrite(vehicle_image_path, cropped_vehicle)

 #Código para crear y limpiar directorios
fisier_iesire = "rezultate"
dosar_foto = os.path.join(fisier_iesire, "auto")
def goleste_dosarul(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

fisier_iesire = "rezultate"

if not os.path.exists(fisier_iesire):
    os.makedirs(fisier_iesire)
else:
    goleste_dosarul(fisier_iesire)

if not os.path.exists(dosar_foto):
    os.makedirs(dosar_foto)
else:
    goleste_dosarul(dosar_foto)

'''cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)'''
cap = cv2.VideoCapture('../Video/traffic.mp4')
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
prev_frame = 0
new_frame = 0
limits = [181, 586, 1137, 586]
Numaratoare1 = []
start = {}
stop = {}
locatie_vehicul = {}
punct1 = (643, 457)
punct2 = (643, 553)
scala = 0.3
distanta= distanta_in_metri(punct1, punct2, scala)
print("Distanta in metri", distanta)
id_viteza = defaultdict(list)
limita_viteza = 80


while True:
    new_frame = time.time()
    success, img = cap.read()
    img_copy = img.copy()
    height = img.shape[0]
    width = img.shape[1]
    mask = np.zeros((height, width), dtype=np.uint8)
    pts = np.array([[[428, 225], [834, 225], [1197, 657], [126, 657]]])
    cv2.fillPoly(mask, pts, 255)
    imgRegion = cv2.bitwise_and(img, img, mask=mask)
    Grafica2 = cv2.imread("graphics2.png", cv2.IMREAD_UNCHANGED)
    img = cvzone.overlayPNG(img, Grafica2, (823, 0))
    rezultat= model(imgRegion, stream=True, conf=0.25)
    detectia = np.empty((0, 5))
    aria1 = [(217, 529), (1088, 529), (1107, 553), (199, 553)]
    aria2 = [(269, 457), (1031, 457), (1047, 476), (255, 476)]
    cv2.polylines(img, [np.array(aria1, np.int32)], True, (0, 255, 0), 2)
    cv2.polylines(img, [np.array(aria2, np.int32)], True, (0, 255, 0), 2)
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
        for rezultat in rezultatTraker:
            x1, y1, x2, y2, id = rezultat
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            lungime, inaltime = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, lungime, inaltime), l=8, t=4, rt=2, colorR=(255, 0, 0), colorC=(0, 0, 255) )
            cvzone.putTextRect(img, f'{int(id)}', (max(0, x1), max(25, y1)), scale=1, thickness=2, offset=6, colorR=(255, 0, 0))
            cx, cy = x1 + lungime // 2, y1 + inaltime // 2
            a1 = cv2.pointPolygonTest(np.array(aria1, np.int32), (cx, cy), False)
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED )

            if limits[0] < cx < limits[2] and limits[1] -15 < cy < limits[1] +15:
                if Numaratoare1.count(id) == 0:
                    Numaratoare1.append(id)
            if a1 >= 0:
                start[id] = time.process_time()
            if id in start:

                a2 = cv2.pointPolygonTest(np.array(aria2, np.int32), (cx, cy), False)
                if a2 >= 0:
                    timpul = time.process_time() - start[id]
                    if id not in stop:
                        stop[id] = timpul

                    if id in stop:
                        stop[id] = timpul
                        viteza = distanta_in_metri(punct1, punct2, scala) / stop[id]
                        viteza2 = int(viteza * 3.6)
                        id_viteza[id].append(viteza2)
                        if id not in id_viteza or len(id_viteza[id]) < 10:
                            id_viteza[id].append(viteza2)
                        else:
                            id_viteza[id].pop(0)
                            id_viteza[id].append(viteza2)
                            viteza_medie = calculeaza_viteza_medie(id_viteza[id])
                locatie_vehicul[id] = (cx, cy)

            if len(id_viteza[id]) > 1:
                viteza_medie = calculeaza_viteza_medie(id_viteza[id])
                print(str(id_viteza[id]))
                print(viteza_medie)
                cv2.putText(img, f"{int(viteza_medie)} km/h", (x1 +lungime + 5, y1 + inaltime // 2), cv2.FONT_HERSHEY_PLAIN,
                            2, (0, 0, 255), 2)
                if int(viteza_medie) > limita_viteza:
                    diferenta_viteza = viteza2 - limita_viteza
                    print(diferenta_viteza)
                    salveaza_info_vehicul(int(id), viteza2, diferenta_viteza)
                    salveaza_foto_vehicul(int(id), img, img_copy, x1, y1, x2, y2)

            locatie_vehicul[id] = (cx, cy)
    cv2.putText(img, str(len(Numaratoare1)), (933, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 6)


    cv2.imshow("Radar", img)
    key = cv2.waitKey(1)
    if key != -1 and key in [27, ord('q')]:
        apasa_q_si_salveaza(id_viteza, limita_viteza)
        break

cap.release()
cv2.destroyAllWindows()