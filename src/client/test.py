import numpy as np
import cv2
from PIL import Image

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(len(gray))
    cv2.imshow('frame',gray)
    width_d, height_d = 280, 280  # Declare your own width and height
    face = cv2.resize(gray, (width_d, height_d))
    pil_image = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(pil_image).convert('L')
    numpy_array = np.array(pil_image, 'uint8')
    print(numpy_array.shape)
    numpy_array=numpy_array.tobytes()
    print(len(numpy_array))

    frame = np.frombuffer(numpy_array,dtype=np.uint8)
    # frame = np.array(list(frame))
    # frame = np.array(frame, dtype = np.uint8 )
    frame=frame.reshape(width_d, height_d)
    print(frame.shape)
    cv2.imshow('res',frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
