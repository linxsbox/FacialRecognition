import cv2, time, datetime
import numpy as np

def video_work():
    # Camera object, Get it first camera.s
    camera = cv2.VideoCapture(0)
    # init background model, it's camera first frame.
    firstFrame = None

    time.sleep(0.25)

    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('size:'+repr(size))

    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
    kernel = np.ones((5, 5), np.uint8)

    while True:
        grabbed, frame = camera.read()

        # If camera can't grabbed frame, exit this app.
        if not grabbed:
            break

        # Color revised.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # GaussianBlur.
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray
            continue

        # different map
        frameDelta = cv2.absdiff(firstFrame, gray)
        # threshold to binary
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # Morphological dilation. 
        thresh = cv2.dilate(thresh, es, iterations = 2)
        _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 1500:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            # 计算轮廓的边界框，在当前帧中画出该框
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.putText(frame, "Room Status: {}".format("111"), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
        # show it camera current frame.
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        
        key = cv2.waitKey(1) & 0xFF
    
        # if key down is 'q', break loop.
        if key == ord("q"):
            break
    
    # clear camera object and close all the open windows.
    camera.release()
    cv2.destroyAllWindows()

video_work()
