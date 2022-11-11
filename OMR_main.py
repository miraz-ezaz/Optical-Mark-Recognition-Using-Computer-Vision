import cv2
import numpy as np
import utlis
#import gui
import file_handeling as file
import heapq

################################################
path = "test4.jpg"
widthImg = 1000
heightImg = 1500
#question = gui.number_of_qusns
#choices = gui.number_of_optios
question=30
choices=4

#ans = [0,1,2,3,2,0,1,2,3,2,0,1,2,3,2,0,1,2,3,2,0,1,2,3,2,0,1,2,3,2]
#ans = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ans = [0, 1, 0, 2, 3, 0, 2, 1, 3, 2, 2, 0, 3, 3, 0, 2, 3, 1, 2, 3, 0, 1, 1, 2, 3, 3, 1, 1, 2, 3]


webCamFeed = True
cameraNo = 0

################################################
#cap = cv2.VideoCapture(0)
#cap.set(10,250)
def set_q(x):
    global question
    question = x

def set_c(x):
    global choices
    choices = x
def set_ans():
    global ans
    ans = file.return_answer("Answers.txt")

def main_check(img):
    score = 0
    roll =""
    #if webCamFeed: success ,img = cap.read()
    #else:
    #img = cv2.imread(path)


    #PreProcessing
    img = cv2.resize(img,(widthImg,heightImg))
    imgContours = img.copy()
    imgFinal = img.copy()
    imgBiggestContours = img.copy()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,10,50)
    try:
        #Finding all Contours
        countours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContours,countours,-1,(0,255,0),10 )
        # Find Recttangle
        rectCon = utlis.rectContour(countours)
        biggestContour = utlis.getCornerPoints(rectCon[0])
        gradePoints = utlis.getCornerPoints(rectCon[2])
        regPoints = utlis.getCornerPoints(rectCon[1])
        #print(biggestContour)

        if biggestContour.size != 0 and gradePoints.size != 0:
            cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,255,0),20)
            cv2.drawContours(imgBiggestContours, gradePoints, -1, (255, 0, 0), 20)
            cv2.drawContours(imgBiggestContours, regPoints, -1, (255, 0, 0), 20)
            biggestContour = utlis.reorder(biggestContour)
            regPoints = utlis.reorder(regPoints)
            gradePoints = utlis.reorder(gradePoints)

            #mcq

            pt1 = np.float32(biggestContour)
            pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgwrapcolored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
            #cv2.imshow("Grade", imgwrapcolored)

            #reg no

            ptR1 = np.float32(regPoints)
            ptR2 = np.float32([[0, 0], [320, 0], [0, 320], [320, 320]])
            matrixR = cv2.getPerspectiveTransform(ptR1, ptR2)
            imgRegDisplay = cv2.warpPerspective(img, matrixR, (320, 320))
            #cv2.imshow("Reg",imgRegDisplay)
            roll = reg(imgRegDisplay)

            #grade points

            ptG1 = np.float32(gradePoints)
            ptG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
            matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
            imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150))
            #cv2.imshow("Grade", imgGradeDisplay)




            ##apply threshold
            imgWrapGray = cv2.cvtColor(imgwrapcolored,cv2.COLOR_BGR2GRAY)
            imgBlurMCQ = cv2.GaussianBlur(imgWrapGray, (5, 5), 1)
            imgThresh = cv2.threshold(imgWrapGray,125,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
            #imgThresh = cv2.adaptiveThreshold(imgBlurMCQ,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,2)
            #cv2.imshow("test",imgThresh)
            boxes = utlis.splitBoxes(imgThresh,question,choices)
            #cv2.imshow("test",boxes[0])

            #Getting Non Zero Pixel
            myPixelVal = np.zeros((question,choices))
            countC = 0
            countR = 0
            # print(question)
            # print(choices)
            # print(ans)
            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC] = totalPixels
                countC +=1
                if (countC == choices):countR +=1 ;countC=0
            #print("XX")
            #print(myPixelVal)

            #Findings index value of the markings
            myIndex = []
            #print("xxxxx")
            for x in range(0,question):
                arr = myPixelVal[x]
                test_arr = heapq.nlargest(2,arr);
                #print("arr",arr)
                dif = test_arr[0]-test_arr[1]
                #print(dif)
                if(test_arr[0]>2100 and dif>100):
                    myIndexVal = np.where(arr ==np.amax(arr))
                    #print(myPixelVal[0])
                    myIndex.append(myIndexVal[0][0])
                else:
                    myIndex.append(5)
            #print(myIndex)

            #Grading
            grading = []
            #print(ans)
            for x in range (0,question):
                if ans[x] == myIndex[x]:
                    grading.append(1)
                else: grading.append(0)
            #print(grading)
            #print(grading)
            score = sum(grading)
            #print(score)

            #Dispaly Answers
            imgResults = imgwrapcolored.copy()
            imgResults = utlis.showAnswers(imgResults,myIndex,grading,ans,question,choices)
            imgRawDrawing = np.zeros_like(imgwrapcolored)
            imgRawDrawing = utlis.showAnswers(imgRawDrawing,myIndex,grading,ans,question,choices)
            invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
            imgInvWrap = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))
            #cv2.imshow("res",imgResults)
            imgRawGrade = np.zeros_like(imgGradeDisplay)
            cv2.putText(imgRawGrade,str(int(score)),(100,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,255),3)
            invMatrixG = cv2.getPerspectiveTransform(ptG2, ptG1)
            imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg))

            imgFinal = cv2.addWeighted(imgFinal,1,imgInvWrap,1,0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)





        # imgBlank = np.zeros_like(img)
        # imgArray = ([img, imgGray, imgBlur, imgCanny],
        #             [imgBlank, imgBiggestContours, imgwrapcolored, imgThresh],
        #             [imgResults, imgRawDrawing, imgInvWrap, imgFinal])
    except:
        pass
        # #imgBlank = np.zeros_like(img)
        # #imgArray = ([img, imgGray, imgBlur, imgCanny],
        #             [imgContours, imgBlank, imgBlank, imgBlank],
        #             [imgBlank, imgBlank, imgBlank, imgBlank])


    # #lables = [["Original","Gray","Blur","Canny"],
    #           ["Contours","Biggest Con","Wrap","Threshols"],
    #           ["Result","Raw Drawing","Inv Wrap","Final"]]
    #imgStacked = utlis.stackImages(imgArray,0.25)
    # #cv2.imshow("Final Result",imgFinal)
    #cv2.imshow("Stacked",imgStacked)
    # # if cv2.waitKey(1) & 0xFF == ord('s'):
    # #     cv2.imwrite("FinalResult.jpg",imgFinal)
    # #     cv2.waitKey(300)

    return imgFinal,roll,score

def reg(img):
    #print("x")
    ##apply threshold
    imgWrapGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    imgThresh = cv2.threshold(imgWrapGray, 125, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    #print(imgThresh.shape)

    cols = np.hsplit(imgThresh,10)
    #print(cols)
    #cv2.imshow("rb1", cols[0])

    boxes = []
    for c in cols:
        rows = np.vsplit(c, 10)
        for box in rows:
            boxes.append(box)
    #cv2.imshow("rb1",boxes[2])
    myPixelVal = np.zeros((10, 10))
    countC = 0
    countR = 0
    for image in boxes:
        totalPixels = cv2.countNonZero(image)
        myPixelVal[countR][countC] = totalPixels
        countC += 1
        if (countC == 10): countR += 1;countC = 0
    #print(myPixelVal)
    myIndex = []
    for x in range(0, 10):
        arr = myPixelVal[x]
        # print("arr",arr)
        myIndexVal = np.where(arr == np.amax(arr))
        # print(myPixelVal[0])
        myIndex.append(myIndexVal[0][0])
    reg = ""
    for d in myIndex:
        reg=reg+str(d)
    #print(reg)


    return reg
