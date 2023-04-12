# Auto-counter-si-radar

Proiectul auto-counter este o aplicație care utilizează YOLOv8 pentru a detecta și a număra autovehiculele care trec prin două linii virtuale în timp real. În acest caz, se numără mașinile, camioanele și autobuzele care trec prin fiecare linie și se afișează numărul acestora pe ecran. Aplicația calculează și afișează numărul de cadre pe secundă (FPS) al secvenței video.

Proiectul radar auto  este, de asemenea, o aplicație care utilizează YOLOv8 pentru a detecta autovehiculele în timp real. Această aplicație urmărește și înregistrează viteza medie a fiecărui vehicul pe baza distanței parcurse în metri între două zone (aria1 și aria2) și timpul necesar pentru a parcurge această distanță. Aplicația stochează informațiile despre viteza vehiculelor într-un fișier text numit "viteze_medii.txt". Dacă viteza medie a vehiculului depășește limita de viteză prestabilită (80 km/h în acest caz), aplicația salvează informațiile despre vehicul într-un alt fișier text numit "vehicle_info.txt" și salvează o fotografie a vehiculului într-un director numit "rezultate/auto".

SORT (Simple Online and Realtime Tracking) pentru a urmări obiectele în timp real. Acest algoritm este bazat pe filtre Kalman și își propune să urmărească obiectele într-un videoclip pe baza detecțiilor obținute dintr-un algoritm de detecție a obiectelor, cum ar fi YOLO sau Faster R-CNN.

În esență, algoritmul urmărește obiectele din cadrele video și le atribuie un identificator unic pentru a le putea distinge. Acest lucru este util în aplicații precum analiza traficului, urmărirea jucătorilor în sport sau monitorizarea persoanelor în spații publice.

În codul furnizat, se utilizează filtre Kalman pentru a estima starea și poziția obiectelor urmărite în fiecare cadru. Algoritmul calculează suprapunerea între detecțiile curente și cele anterioare (IoU) pentru a decide dacă un obiect detectat într-un cadru se potrivește cu unul deja urmărit. Dacă suprapunerea este peste un prag prestabilit, obiectul este considerat a fi același și filtrul Kalman este actualizat cu noile măsurători.

În acest cod, se definește o clasă KalmanBoxTracker care reprezintă starea internă a unui obiect urmărit, iar clasa Sort se ocupă cu gestionarea tuturor obiectelor și actualizarea lor pe baza detecțiilor noi. În cele din urmă, codul procesează o secvență de imagini și salvează rezultatele într-un fișier text.

Principalele parametri ai algoritmului sunt max_age, care reprezintă numărul maxim de cadre în care un obiect poate fi menținut în urmărire fără a fi detectat, min_hits, care reprezintă numărul minim de detecții asociate înainte ca urmărirea să fie inițializată, și iou_threshold, care este pragul minim de suprapunere necesar pentru a considera că o detecție se potrivește cu un obiect urmărit.
