# 이미지 처리와 색공간 변환을 위한 OpenCV 라이브러리
import cv2

# 프로그램 실행시간 측정을 위한 time 모듈 
import time 

# ========================
# 구현 1: OpenCV 사용 
# ========================

# OpenCV 방식의 실행시간 측정 시작
start_cv = time.perf_counter()

# 원본 이미지 불러오기
# OpenCV는 이미지를 BGR 순서로 읽음. 
img = cv2.imread("window.jpg")

# BGR 컬러 영상을 YCrCb 색공간으로 변환
# OpenCV에서는 Y, Cr, Cb 순서로 저장됨. 
YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

# YCrCb 영상을 각 채널로 분리
# Y: 밝기 정보
# Cr: Red 계열 색차 정보
# cB: Blue 계열 색차 정보
Y, Cr, Cb = cv2.split(YCrCb)

# YCrCb 영상을 다시 BGR 컬러 영상으로 복원 
restored = cv2.cvtColor(YCrCb, cv2.COLOR_YCrCb2BGR)

# OpenCV 방식의 실행시간 측정 종료
end_cv = time.perf_counter()

# 종료시간 - 시작시간으로 OpenCV 방식의 총 실행시간 계산
cv_time = end_cv - start_cv

# =======================================
# 구현 2: 수식을 이용하여 직접 구현  
# =======================================

# 직접 구현 방식의 실행시간 측정 시작
start_calc = time.perf_counter()

# 원본 이미지를 B, G, R 채널로 분리 
B, G, R = cv2. split(img)

# 수식 계산을 위해 실수형으로 변환 
B = B.astype(float)
G = G.astype(float)
R = R.astype(float)

# RGB -> YCbCr 직접 변환  
Y_calc = 0.257 * R + 0.504 * G + 0.098 * B + 16
Cb_calc = -0.148 * R - 0.291 * G + 0.439 * B + 128
Cr_calc = 0.439 * R - 0.368 * G - 0.071 * B + 128 

# Y채널 출력용 복사본 생성 
Y_show = Y_calc.clip(0, 255).astype("uint8")

# YCbCr -> RGB 직접 복원 
R_calc = 1.164 * (Y_calc - 16) + 1.596 * (Cr_calc - 128)
G_calc = 1.164 * (Y_calc - 16) - 0.813 * (Cr_calc - 128) - 0.391 * (Cb_calc - 128)
B_calc = 1.164 * (Y_calc - 16) + 2.018 * (Cb_calc - 128)

# 계산 결과가 이미지 범위를 벗어나지 않도록 0~255 범위로 제한
R_calc = R_calc.clip(0, 255)
G_calc = G_calc.clip(0, 255)
B_calc = B_calc.clip(0, 255)

# OpenCV에서 사용할 수 있도록 8비트 정수형으로 변환 
R_calc = R_calc.astype("uint8")
G_calc = G_calc.astype("uint8")
B_calc = B_calc.astype("uint8")

# OpenCV는 BGR 순서이므로 B, G, R 순서로 합침 
restored_calc = cv2.merge([B_calc, G_calc, R_calc])

# 직접 구현 방식의 실행시간 측정 종료
end_calc = time.perf_counter()

# 종료시간 - 시작시간으로 직접 구현 방식의 총 실행시간 계산
calc_time = end_calc - start_calc

# ========================
# 결과 출력
# ========================

# OpenCV 방식과 직접 구현 방식의 실행시간 출력 및 비교
print("OpenCV 실행시간:", cv_time, "초")
print("직접 구현 실행시간:", calc_time, "초")

# 원본 영상
cv2.imshow("Original img", img)

# OpenCV 방식으로 추출한 Y 채널
cv2.imshow("Y img", Y)

# OpenCV 방식으로 복원한 컬러 영상
cv2.imshow("Restored img", restored)

# 수식으로 직접 계산한 Y 채널
cv2.imshow("Y calc", Y_show)

# 수식으로 직접 복원한 컬러 영상
cv2.imshow("Restored calc", restored_calc)

# 아무 키나 누를 때까지 창 유지
cv2.waitKey(0)

# 모든 OpenCV 창 닫기
cv2.destroyAllWindows()

