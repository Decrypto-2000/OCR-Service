import cv2
import pytesseract
import os

def extract_text_from_video(video_path: str, output_txt_path: str, time_interval: int = 1):
    """
    Extract text from video frames using Tesseract OCR and write it to a text file.

    Args:
        video_path (str): Path to the video file.
        output_txt_path (str): Path to save the extracted text.
        time_interval (int): Time interval (in seconds) between frames to process.
    """
    # Initialize video capture
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    # Get frames per second (fps) of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = int(fps * time_interval)
    frame_count = 0

    print("Processing video...")

    # Open the output text file
    with open(output_txt_path, 'w', encoding='utf-8') as text_file:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Process the frame only at specified intervals
            if frame_count % frame_interval == 0:
                # Perform OCR on the frame
                text = pytesseract.image_to_string(frame, config='--psm 6')
                timestamp = frame_count // fps
                if text.strip():  # Write only if there's meaningful text
                    text_file.write(f"Timestamp {timestamp} seconds:\n{text.strip()}\n\n")

            frame_count += 1

    cap.release()
    print(f"Video processing completed. Text saved to '{output_txt_path}'.")

def process_video_to_txt(video_folder: str, txt_folder: str, time_interval: int=1):
    for i in os.listdir(video_folder):
        txt_name = i.split(".")[0] +".txt"
        video_path = os.path.join(video_folder, i)
        txt_path = os.path.join(txt_folder, txt_name)
        print(f"video path --> {video_path}")
        print(f"txt path --> {txt_path}")
        extract_text_from_video(video_path=video_path, output_txt_path=txt_path, time_interval=time_interval)


if __name__ == "__main__":
    txt_folder = "temp/text"
    video_folder ="temp/VIdeos"
    time_interval = 1
    process_video_to_txt(video_folder=video_folder, txt_folder=txt_folder, time_interval=time_interval)