
# OpenCV 라이브러리: 동영상 읽기, 영상 처리 및 화면 출력에 사용
import cv2

# =======================================
# 동영상 파일 불러오기
# =======================================

# 동영상 파일을 읽기 위한 VideoCapture 객체 생성
cap = cv2.VideoCapture("coins.mp4")

# 동영상 파일이 정상적으로 열리지 않은 경우 프로그램 종료
if not cap.isOpened():
    print("동영상을 열 수 없습니다.")
    exit()

# 동영상의 초당 프레임 수(FPS) 확인
fps = cap.get(cv2.CAP_PROP_FPS)

# FPS를 기준으로 프레임 간 대기 시간 계산
delay = max(1, round(1000 / fps)) if fps > 0 else 33

# 사용자가 q 키를 눌렀는지 확인하기 위한 변수
quit_requested = False

# 스페이스바를 눌렀을 때 일시정지 상태를 저장할 변수
paused = False

# =======================================
# 출력 창 크기 및 위치 설정
# =======================================

# 원본 영상 출력 창 생성 및 위치 설정
cv2.namedWindow("Original Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Original Video", 480, 320)
cv2.moveWindow("Original Video", 0, 0)

# Y 채널 영상 출력 창 생성 및 위치 설정
cv2.namedWindow("Y Channel", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Y Channel", 480, 320)
cv2.moveWindow("Y Channel", 490, 0)

# 이진화 영상 출력 창 생성 및 위치 설정
cv2.namedWindow("Binary Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Binary Image", 480, 320)
cv2.moveWindow("Binary Image", 980, 0)

# 모폴로지 처리 영상 출력 창 생성 및 위치 설정
cv2.namedWindow("Morphology Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Morphology Image", 480, 320)
cv2.moveWindow("Morphology Image", 245, 370)

# 최종 동전 검출 결과 출력 창 생성 및 위치 설정
cv2.namedWindow("Coin Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Coin Detection", 480, 320)
cv2.moveWindow("Coin Detection", 735, 370)

# =======================================
# 동영상 프레임 읽기 및 출력
# =======================================

# 동영상의 프레임을 순서대로 읽기 위해 반복문 실행
while True:

    # 동영상에서 프레임 한 장 읽기
    # ret : 프레임 읽기 성공 여부
    # frame : 읽어 온 영상 프레임
    ret, frame = cap.read()

    # 동영상이 끝나거나 프레임을 읽지 못한 경우 반복문 종료
    if not ret:
        break

    # 현재 프레임을 화면에 출력
    cv2.imshow("Original Video", frame)

    # =======================================
    # Y 채널 추출
    # =======================================

    # BGR 영상을 YCrCb 색 공간으로 변환
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    # YCrCb 영상에서 밝기 정보인 Y 채널 추출
    y_channel = ycrcb[:, :, 0]

    # 추출한 Y 채널 영상을 화면에 출력
    cv2.imshow("Y Channel", y_channel)

    # =======================================
    # Otsu 이진화
    # =======================================

    # Otsu 알고리즘으로 최적의 임계값을 자동 계산하여 이진화
    threshold_value, binary = cv2.threshold(
        y_channel, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # 이진화된 영상을 화면에 출력
    cv2.imshow("Binary Image", binary)
   
    # =======================================
    # 모폴로지 연산
    # =======================================

    # Closing에 사용할 11x11 타원형 구조 요소 생성
    closing_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (11, 11)
    )

    # Opening에 사용할 3x3 타원형 구조 요소 생성
    opening_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (3, 3)
    )

    # Closing 연산으로 동전 내부의 검은색 빈 부분 메우기
    closed = cv2.morphologyEx(
        binary, cv2.MORPH_CLOSE, closing_kernel
    )

    # Opening 연산으로 작은 흰색 잡음 제거
    opened = cv2.morphologyEx(
        closed, cv2.MORPH_OPEN, opening_kernel
    )

    # 모폴로지 연산 결과를 화면에 출력
    cv2.imshow("Morphology Image", opened)

    # =======================================
    # 연결 요소 분석 및 동전 검출
    # =======================================

    # 흰색으로 연결된 영역을 찾아 개수, 레이블, 통계 정보, 중심 좌표 반환
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opened)

    # 너무 작은 영역을 제외하기 위한 최소 면적 설정
    min_area = 900

    # 책상 배경처럼 지나치게 큰 영역을 제외하기 위한 최대 면적 설정
    max_area = 10000

    # 원본 프레임을 복사하여 검출 결과 표시
    result = frame.copy()

    # 검출된 동전 개수를 저장할 변수
    coin_count = 0

    # 0번 배경을 제외하고 각 연결 영역 검사
    for i in range(1, num_labels):

        # 현재 영역의 위치, 크기, 면적 정보 가져오기
        x, y, w, h, area = stats[i]

        # 각 연결 영역의 번호와 면적 출력
        print(f"영역 {i}: 면적 = {area}")

        # 너무 작거나 큰 영역은 동전이 아닌 것으로 판단하여 제외
        if area < min_area or area > max_area:
            continue

        # 동전 개수 증가
        coin_count += 1

        # 검출된 영역에 초록색 Bounding Box 표시
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Bounding Box 위에 동전 번호 표시
        cv2.putText(
            result, str(coin_count), (x, max(20, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
        )

    # 화면 왼쪽 위에 최종 동전 개수 표시
    cv2.putText(
        result, f"Coin Count: {coin_count}", (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2
    )

    # 동전 검출 결과를 화면에 출력
    cv2.imshow("Coin Detection", result)

    # =======================================
    # 키 입력 및 일시정지 처리
    # =======================================

    # 프레임 간 대기 시간 동안 키 입력 확인
    key = cv2.waitKey(delay) & 0xFF

    # q 키를 누르면 동영상 재생 종료
    if key == ord('q'):
        quit_requested = True
        break

    # 스페이스바를 누르면 일시정지
    if key == ord(' '):
        paused = True

    # 일시정지 상태에서는 다음 프레임을 읽지 않고 대기
    while paused:

        # 키 입력 확인
        key = cv2.waitKey(30) & 0xFF

        # 스페이스바를 다시 누르면 재생
        if key == ord(' '):
            paused = False

        # q 키를 누르면 프로그램 종료
        elif key == ord('q'):
            quit_requested = True
            break

    # 일시정지 중 q 키를 눌렀다면 바깥 반복문도 종료
    if quit_requested:
        break

# =======================================
# 마지막 프레임 출력 유지
# =======================================

# 동영상이 정상적으로 끝난 경우 q 키 입력까지 창 유지
if not quit_requested:
    while True:
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

# =======================================
# 프로그램 종료
# =======================================

# 동영상 파일과 관련된 자원 해제
cap.release()

# 생성된 모든 OpenCV 창 닫기
cv2.destroyAllWindows()
