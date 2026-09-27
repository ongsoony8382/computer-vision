import cv2 as cv #OpenCV 라이브러리 cv2를 불러온 뒤, cv로 지정 

imgfile = 'window.jpg' #읽어올 이미지 파일명 
img = cv.imread(imgfile, cv.IMREAD_COLOR) #컬러이미지로 읽어서 img변수에 저장

cv.imshow('img', img) #'img'는 뜨는 창의 이름, img는 띄울 이미지 
cv.waitKey(0) #키보드 입력이 들어올 때까지 창 유지 
cv.destroyAllWindows() # OpenCV 창 닫기 