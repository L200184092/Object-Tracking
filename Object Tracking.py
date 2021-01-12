import cv2

#tracker = cv2.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerTLD_create()
#tracker = cv2.TrackerMedianFlow_create()
#tracker = cv2.TrackerCSRT_create()
tracker = cv2.TrackerMOSSE_create()

cap = cv2.VideoCapture(0)
bbox = None

def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (0, 0, 255), 3, 3 )
    cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

while True:
    timer = cv2.getTickCount()
    success, img = cap.read()
    if bbox is not None:
        success, bbox = tracker.update(img)
        if success:
            drawBox(img,bbox)
        else:
            cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.rectangle(img,(15,15),(200,90),(255,0,0),2)
    cv2.putText(img, "FPS:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2);
    cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2);

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    if fps>60:
        myColor = (0,255,0)
    elif fps>20:
        myColor = (255,0,0)
    else:
        myColor = (0,0,255)
    cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);

    cv2.imshow("Tracking", img)
    if cv2.waitKey(1) & 0xff == ord('s'):
        bbox = cv2.selectROI("Tracking", img, fromCenter=False, showCrosshair=True)
        tracker.init(img, bbox)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
       break

cap.release()
cv2.destroyAllWindows()
