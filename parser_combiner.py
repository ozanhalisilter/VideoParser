from moviepy.editor import *
import cv2
import os

def split_video(input_video_path, output_folder_path):
    # Create frames output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        os.makedirs(output_folder_path+"/frames")

    # Open the video file
    video = cv2.VideoCapture(input_video_path)
    frame_count = 0

    # Read frames until the video ends
    while True:
        # Read the current frame
        ret, frame = video.read()

        # Break the loop if no frames are retrieved
        if not ret:
            break

        # Save the frame as an image
        frame_name = f"frame_{frame_count:0=10}.jpg"
        frame_path = os.path.join(output_folder_path+"/frames", frame_name)
        cv2.imwrite(frame_path, frame)

        # Increment the frame count
        frame_count += 1

    # Release the video capture object
    video.release()

    # Extract audio
    video_clip = VideoFileClip(input_video_path)
    audio_clip = video_clip.audio.write_audiofile(output_folder_path+"/audio_output.mp3")

    print(f"Split {frame_count} frames and extracted audio successfully!")

def combine_frames_and_audio(input_folder, video_output_path, fps):
    # Get all image file paths to a list.
    frames_path =input_folder+ "/frames"
    audio_input_path = input_folder + "/" + [audio for audio in os.listdir(input_folder) if audio.endswith(".mp3")][0]
    images = [img for img in os.listdir(frames_path) if img.endswith(".jpg")]
    # Sort the images by name
    images.sort()

    # Read the first image to get the shape
    frame = cv2.imread(os.path.join(frames_path, images[0]))
    height, width, layers = frame.shape

    # Create the VideoWriter object
    without_audio_path = video_output_path.replace(".","_without_audio.")
    video = cv2.VideoWriter(without_audio_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Add frames to the video
    for image in images:
        video.write(cv2.imread(os.path.join(frames_path, image)))

    # Release the video object
    video.release()

    # Combine video and audio
    
    video_clip_without_audio = VideoFileClip(without_audio_path)
    audio_clip = AudioFileClip(audio_input_path)
    final_clip = video_clip_without_audio.set_audio(audio_clip)
    final_clip.write_videofile(video_output_path, codec='libx264', audio_codec='aac')
    

    print(f"Created video {video_output_path} from {len(images)} frames and audio!")



def main():
    # Provide the path to your video file and the output folder for frames
    input_video_path = "SDP_TEST_VIDEO.mp4"
    split_folder_path = "content/output_folder"
    output_video_path = "content/SDP_generated.mp4"
    fps = 30.0
    
    # Split the video into frames and audio
    print("----------STARTED-SPLITTING--------")
    split_video(input_video_path, split_folder_path)
    print("----------FINISHED-SPLITTING--------")

    

    # Combine the frames and audio back into a video
    print("----------STARTED-COMBINING--------")
    combine_frames_and_audio(split_folder_path, output_video_path, fps)
    print("----------FINISHED-COMBINING--------")


if __name__ == "__main__":
    main()