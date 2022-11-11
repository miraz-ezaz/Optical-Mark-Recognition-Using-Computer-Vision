import file_handeling as file
import helper
import OMR_main as omr
import os
import cv2

def batch_scan(scan_path):

    files = os.listdir(scan_path);
    images = []
    #rolls = []
    for f in files:
        img = cv2.imread(f'{scan_path}/{f}')
        images.append(img)
        #rolls.append(int(os.path.splitext(f)[0]))

    for img in images:
        image , rl ,mark = omr.main_check(img)
        save_path = helper.r_path(os.getcwd())
        cv2.putText(image, f"Roll: {rl}", (410, 340), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        cv2.imwrite(f'Scanned_images/Reg-{rl}.jpg',image)
        r_m = helper.result_format(rl,mark)
        file.insert_ans("Result.csv",r_m)








