import cv2
import yaml
import asyncio
from datetime import datetime
from detector import YOLODetector
from tracker import DeepSortTracker
from video_writer import VideoWriter
from email_alert import EmailAlert
from database import DetectionDatabase
from concurrent.futures import ThreadPoolExecutor

def load_config(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

async def send_alert_async(email_alert, subject, message):
    loop = asyncio.get_running_loop()
    # Run the send_alert method in a separate thread
    await loop.run_in_executor(None, email_alert.send_alert, subject, message)


def is_within_time_range(start, end, current):
    """Check if the current time is within the specified range."""
    if start <= end:
        return start <= current <= end
    else:
        # Over midnight
        return current >= start or current <= end


async def main():
    config = load_config("../config/config.yaml")
    detector = YOLODetector(config)
    tracker = DeepSortTracker(config)
    video_writer = VideoWriter(output_dir=config['output']['video_dir'])
    email_alert = EmailAlert(config)
    database = DetectionDatabase(config['output']['db_path'])

    cap = cv2.VideoCapture(config['input']['video_path'])
    frame_count = 0

    # Load email alert time range from config
    start_time = datetime.strptime(config['alert']['night_hour_start'], "%H:%M").time()
    end_time = datetime.strptime(config['alert']['night_hour_end'], "%H:%M").time()


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % config['processing']['frame_skip'] != 0:
            continue

        detections = detector.detect(frame)
        tracks = tracker.update_tracks(detections, frame=frame)

        current_hour = datetime.now().hour
        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            bbox = track.to_ltrb()
            object_type = track.get_det_class()

            # Start or continue saving video for each unique track ID
            video_path = video_writer.start_writing(track_id, frame)
            video_writer.write_frame(track_id, frame)

            # Insert detection into database for each saved video
            if video_path:  # Only insert if a new video file was started
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                database.insert_detection(object_type, timestamp, video_path)
                current_time = datetime.now().time()

                print("***************************************************************")
                print(start_time)
                print(end_time)
                print(current_time)
                print(is_within_time_range(start_time, end_time, current_time))
                # Check if the current time is within the alert range
                if is_within_time_range(start_time, end_time, current_time):
                    # Schedule the email alert to be sent in the background
                            # Compose HTML message
                    message = f"""
                    <html>
                    <body>
                        <p><strong>Human detected at night.</strong></p>
                        <p><strong>Time:</strong> {current_time}</p>
                        <p><strong>Video Path:</strong> <a href="{video_path}">{video_path}</a></p>
                    </body>
                    </html>
                    """
                    asyncio.create_task(send_alert_async(email_alert, "Night Detection Alert", message))
                    print("Scheduled email for video:", video_path)

            # Draw tracking info on the frame
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 0, 255), 2)
            cv2.putText(frame, f"ID: {track_id}", (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Stop all active video writers at the end of the video
    video_writer.stop_all()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())



# import cv2
# import yaml
# from datetime import datetime
# from detector import YOLODetector
# from tracker import DeepSortTracker
# from video_writer import VideoWriter
# from email_alert import EmailAlert
# from database import DetectionDatabase

# def load_config(path):
#     with open(path, 'r') as file:
#         return yaml.safe_load(file)

# def main():
#     config = load_config("../config/config.yaml")
#     detector = YOLODetector(config)
#     tracker = DeepSortTracker(config)
#     video_writer = VideoWriter(output_dir=config['output']['video_dir'])
#     email_alert = EmailAlert(config)
#     database = DetectionDatabase(config['output']['db_path'])

#     cap = cv2.VideoCapture(config['input']['video_path'])
#     frame_count = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_count += 1
#         if frame_count % config['processing']['frame_skip'] != 0:
#             continue

#         detections = detector.detect(frame)
#         tracks = tracker.update_tracks(detections, frame=frame)

#         current_hour = datetime.now().hour
#         for track in tracks:
#             if not track.is_confirmed():
#                 continue

#             track_id = track.track_id
#             bbox = track.to_ltrb()
#             object_type = track.get_det_class()

#             # Start or continue saving video for each unique track ID
#             video_path = video_writer.start_writing(track_id, frame)
#             video_writer.write_frame(track_id, frame)

#             # Insert detection into database for each saved video
#             if video_path:  # Only insert if a new video file was started
#                 timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 database.insert_detection(object_type, timestamp, video_path)
#                 email_alert.send_alert("Night Detection Alert", "Human detected at night ========.")
#                 print("sended email ", video_path)


#             # # Check for nighttime human detection to trigger email alert
#             # if object_type == "person" and current_hour == config['alert']['night_hour']:
#             #     email_alert.send_alert("Night Detection Alert", "Human detected at night.")

#             # Draw tracking info on the frame
#             cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 0, 255), 2)
#             cv2.putText(frame, f"ID: {track_id}", (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#         cv2.imshow("Tracking", frame)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

#     # Stop all active video writers at the end of the video
#     video_writer.stop_all()
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()
