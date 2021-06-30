import cv2
pause = False
play = True
cap= cv2.VideoCapture(0)

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
filename = input("What is this name of the file? ")

writer= cv2.VideoWriter(filename + ".mp4", cv2.VideoWriter_fourcc('M','J','P','G'), 20, (width,height))
while play & pause == False:
    if 0xFF==ord("p") & pause==False:
        pause= True
    elif 0xFF == ord("p") & pause==True:
        ret,frame= cap.read()

        writer.write(frame)

        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
writer.release()
cv2.destroyAllWindows()
