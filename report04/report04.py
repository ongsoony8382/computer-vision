# OpenCV 라이브러리: 이미지 읽기, 색 공간 변환, 
# Histogram Equalization 등에 사용
import cv2

# NumPy 라이브러리: 배열 및 수치 연산에 사용
import numpy as np

# 실행 시간 측정에 사용
import time

# 원본 컬러 이미지 읽기
# OpenCV는 이미지를 BGR 순서로 읽음
img = cv2.imread("cat.jpg")

# 이미지 파일을 정상적으로 읽지 못한 경우 프로그램 종료 
if img is None:
    print("이미지를 불러오지 못했습니다.")
    exit()

# BGR 컬러 영상을 YCrCb 색 공간으로 변환
# Y : 밝기 정보 
# Cr : Red 성분과 관련된 색차 정보
# Cb : Blue 성분과 관련된 색차 정보
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

# Y, Cr, Cb 채널을 각각 분리
# Histogram Equalization은 밝기 정보인 Y 채널에만 적용 
Y, Cr, Cb = cv2.split(ycrcb)

# =======================================
# 방법 1: OpenCV equalizeHist 함수 사용
# =======================================

# Histogram Equalization 실행시간 측정 시작
start = time.time()

# Y 채널에 Histogram Equalization 적용 
Y_opencv = cv2.equalizeHist(Y)

# 실행 시간 측정 종료 
end = time.time()

# OpenCV 방식의 실행시간 계산 
opencv_time = end - start

# 평활화된 Y 채널과 기존의 Cr, Cb 채널을 다시 결합
ycrcb_opencv = cv2.merge([Y_opencv, Cr, Cb])

# YCrCb 영상을 다시 BGR 컬러 영상으로 복원 
result_opencv = cv2.cvtColor(ycrcb_opencv, cv2.COLOR_YCrCb2BGR)

# =======================================
# PSNR 계산
# =======================================

# 원본 영상과 OpenCV Histogram Equalization 결과 영상의 PSNR 계산
psnr_opencv = cv2.PSNR(img, result_opencv)


# =======================================
# 결과 출력
# =======================================

# PSNR 및 OpenCV 방식 실행시간 출력
print("OpenCV PSNR:", psnr_opencv)
print("OpenCV 실행시간:", opencv_time, "초")

# 원본 이미지와 Histogram Equalization 적용 결과 이미지를
# 화면 출력용으로 가로/세로 30% 크기로 축소하여 출력
cv2.imshow("Original", cv2.resize(img, None, fx=0.3, fy=0.3))
cv2.imshow("OpenCV Equalized", cv2.resize(result_opencv, None, fx=0.3, fy=0.3))

# 키 입력이 있을 때까지 출력 창 유지
cv2.waitKey(0)
# 생성된 모든 OpenCV 창 닫기
cv2.destroyAllWindows()