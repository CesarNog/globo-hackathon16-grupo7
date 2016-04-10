import cv2
import socket

webcam = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier('base.xml')
width = webcam.get(3)

HOST = '192.168.1.35'  # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)


while cv2.waitKey(True) != 27:
     _, img = webcam.read()

     gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
     faces = face_cascade.detectMultiScale(gray, 1.3, 5)

     cv2.line(img, (int(width/2), 0), (int(width/2), int(webcam.get(4))), (0, 255, 0), 2)
     cv2.line(img, (int(width/2) - int(width/4), 0), (int(width/2) - int(width/4), int(webcam.get(4))), (0, 0, 255), 2)
     cv2.line(img, (int(width/2) + int(width/4), 0), (int(width/2) + int(width/4), int(webcam.get(4))), (0, 0, 255), 2)

     for x, y, w, h in faces:
         cx, cy = x+w/2, y+h/2
         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
         cv2.line(img, (cx, cy), (cx, cy), [0, 255, 255], 15)
         roi_gray = gray[y:y+h, x:x+w]
         roi_color = img[y:y+h, x:x+w]

         if (cx, cy) < (int(width/2) - int(width/4), 0):
             udp.sendto("esquerda", dest)
         elif (cx, cy) > (int(width/2) + int(width/4), 0):
             udp.sendto("direita", dest)

     cv2.imshow("Globo Ocular", img)

udp.close()

#Streaming

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.width = 640
        self.height = 480
        self.centre = None

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()