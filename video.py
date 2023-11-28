import cv2
import os

def images_to_video(image_folder, video_name, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")] #확장자 jpg인거 긁어모음
    frame = cv2.imread(os.path.join(image_folder, images[0])) #첫번째 이미지 가져와서 프레임 설정
    height, width, layers = frame.shape #프레임 설정

    #비디오 파일 생성, 코덱, mp4파일 생성
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    #이미지들을 비디오 파일에 하나씩 넣음
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

