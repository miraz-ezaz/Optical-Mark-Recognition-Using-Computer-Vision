import file_handeling as file
import helper
import OMR_main as omr
import os
import cv2

def live(ip):
    cap = cv2.VideoCapture(ip,cv2.CAP_FFMPEG)
    while True:
        sucees,img = cap.read()
        image,rl,mark = omr.main_check(img)
        imgs = image.copy()
        cv2.putText(imgs, f"Reg: {rl}", (410, 340), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        cv2.putText(image, "Press 'S' to save", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
        cv2.putText(image, "Press 'Esc' To exit", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
        cv2.putText(image, f"Reg: {rl}", (410, 340), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0),3)
        scale_percent = 50  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("ReS",resized)

        k = cv2.waitKey(1)
        if k & 0xFF == ord('s'):
            save_path = helper.r_path(os.getcwd())
            cv2.imwrite(f'Scanned_images/Reg-{rl}.jpg', imgs)
            r_m = helper.result_format(rl, mark)
            file.insert_ans("Result.csv", r_m)
        if k & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
#live("http://192.168.1.3:8080/video")
