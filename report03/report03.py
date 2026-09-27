import cv2 # 이미지 처리와 OpenCV PSNR 함수 사용 
import time # 실행 시간 측정용 
import math # log10 계산 

# 원본 이미지 불러오기 
img = cv2.imread("window.jpg")

# 원본 이미지를 B, G, R 채널로 분리 
B, G, R = cv2.split(img)

# 수식 계산을 위해 실수형으로 변환 
B = B.astype(float)
G = G.astype(float)
R = R.astype(float)

# RGB -> YCbCr 직접 변환 
Y = 0.257 * R + 0.504 * G + 0.098 * B + 16
Cb = -0.148 * R - 0.291 * G + 0.439 * B + 128
Cr = 0.439 * R - 0.368 * G - 0.071 * B + 128

# YCbCr -> RGB 직접 복원
R2 = 1.164 * (Y - 16) + 1.596 * (Cr - 128)
G2 = 1.164 * (Y - 16) - 0.813 * (Cr - 128) - 0.391 * (Cb - 128)
B2 = 1.164 * (Y - 16) + 2.018 * (Cb - 128)

# 값 범위를 0~255로 제한
R2 = R2.clip(0, 255)
G2 = G2.clip(0, 255)
B2 = B2.clip(0, 255)

# 이미지 자료형으로 변환
R2 = R2.astype("uint8")
G2 = G2.astype("uint8")
B2 = B2.astype("uint8")

# OpenCV는 BGR 순서이므로 B, G, R 순서로 합쳐 복원 영상 생성
restored = cv2.merge([B2, G2, R2])

# =======================================
# 구현 1: OpenCV 함수를 이용한 PSNR 계산
# =======================================

# OpenCV PSNR 계산 시작 시간 
start_cv = time.perf_counter()

# 원본 영상과 복원 영상의 PSNR 계산 
psnr_cv = cv2.PSNR(img, restored)

# OpenCV PSNR 계산 종료 시간
end_cv = time.perf_counter()

# OpenCV 방식의 PSNR 계산 시간
cv_psnr_time = end_cv - start_cv

# =======================================
# 구현 2: 수식을 이용한 PSNR 직접 계산
# =======================================

def getPSNR(original, restored):

    # 두 이미지의 차이를 계산하기 위해 실수형 변환 
    original = original.astype(float)
    restored = restored.astype(float)

    # 원본과 복원 영상의 차이를 제곱
    diff = ( original - restored ) ** 2 

    # 모든 픽셀과 3개 채널의 평균 제곱 오차(MSE) 계산 
    mse = diff.mean()

    # 두 이미지가 완전히 같으면 MSE가 0이므로 PSNR을 무한대로 처리
    if mse == 0:
        return float("inf")

    # PSNR 계산
    psnr = 10 * math.log10((255 ** 2) / mse)

    return psnr

# 직접 구현 방식의 PSNR 계산 시작 시간
start_calc = time.perf_counter()

# 직접 구현한 PSNR 함수 호출
psnr_calc = getPSNR(img, restored)

# 직접 구현 방식의 PSNR 계산 종료 시간
end_calc = time.perf_counter()

# 직접 구현 방식의 PSNR 계산 시간
calc_psnr_time = end_calc - start_calc

# =======================================
# 결과 출력
# =======================================

# 두 방식으로 계산한 PSNR 출력 
print("OpenCV PSNR:", round(psnr_cv, 2))
print("직접 계산 PSNR:", round(psnr_calc, 2))

# 두 방식의 실행시간 출력 
print("OpenCV PSNR 실행시간:", round(cv_psnr_time, 6), "초")
print("직접 계산 PSNR 실행시간:", round(calc_psnr_time, 6), "초")