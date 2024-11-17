# import cv2
# import torch
# from deep_sort_realtime.deepsort_tracker import DeepSort

# # Configuration parameters
# CONFIDENCE_THRESHOLD = 0.5  # Confidence threshold to filter out low-confidence detections
# FRAME_SKIP = 2              # Process every nth frame to improve speed
# frame_count = 0             # Initialize frame counter

# # Load YOLOv5 model (you may want to use yolov5s, yolov5n, etc., based on your performance needs)
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
# model.classes = [0]  # Set to detect only 'person' class

# # Initialize DeepSORT tracker
# object_tracker = DeepSort()

# # Load video file
# cap = cv2.VideoCapture("../h1.mp4")

# # Check if the video opened successfully
# if not cap.isOpened():
#     print("Error: Could not open video.")
# else:
#     print("Video opened successfully.")

# # Process each frame from the video
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         print("End of video stream.")
#         break  # Exit if no more frames are available

#     # Skip frames according to FRAME_SKIP setting
#     frame_count += 1
#     if frame_count % FRAME_SKIP != 0:
#         continue

#     # Perform inference with YOLOv5
#     results = model(frame)

#     # Initialize an empty list for detections
#     detections = []

#     # Parse results and filter by confidence
#     for *xyxy, conf, cls in results.xyxy[0]:  # Access detections in xyxy format
#         if conf < CONFIDENCE_THRESHOLD:
#             continue  # Skip detections below confidence threshold

#         # Extract bounding box coordinates
#         x1, y1, x2, y2 = map(int, xyxy)
#         w, h = x2 - x1, y2 - y1
#         coordinates = (x1, y1, w, h)

#         # Append detection to the list if it's a person
#         detections.append((coordinates, float(conf), 'person'))

#     # Update tracks with DeepSORT
#     tracks = object_tracker.update_tracks(detections, frame=frame)

#     # Draw bounding boxes and track IDs on the frame
#     for track in tracks:
#         if not track.is_confirmed():
#             continue

#         # Retrieve the track ID and bounding box for confirmed tracks
#         track_id = track.track_id
#         bbox = track.to_ltrb()  # Get bounding box in left-top-right-bottom format

#         # Draw bounding box around the detected person
#         cv2.rectangle(
#             frame,
#             (int(bbox[0]), int(bbox[1])),
#             (int(bbox[2]), int(bbox[3])),
#             color=(0, 0, 255),  # Red color for bounding box
#             thickness=2
#         )

#         # Display track ID above the bounding box
#         cv2.putText(
#             frame,
#             f"ID: {track_id}",
#             (int(bbox[0]), int(bbox[1]) - 10),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             1,
#             (0, 255, 0),  # Green color for text
#             2
#         )

#     # Show the processed frame with bounding boxes and IDs
#     cv2.imshow("Human Tracking", frame)

#     # Exit loop if 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# # Release the video capture object and close all OpenCV windows
# cap.release()
# cv2.destroyAllWindows()



import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Initialize object tracker with optimized settings
object_tracker = DeepSort(max_age=5, n_init=3)

cap = cv2.VideoCapture("../h1.mp4")
model = YOLO("yolov8s.pt")
classes = model.names
CONFIDENCE_THRESHOLD = 0.0
frame_skip = 2  # Process every 2nd frame
frame_count = 0

if not cap.isOpened():
    print("Error: Video file not opened.")
    exit()

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue  # Skip frames to improve performance

    results = model(image)

    for result in results:
        detections = []
        boxes = result.boxes
        for r in result.boxes.data.tolist():
            if len(r) < 6:
                continue  # Ensure detection has all required elements

            x1, y1, x2, y2 = r[:4]
            w, h = x2 - x1, y2 - y1
            coordinates = list((int(x1), int(y1), int(w), int(h)))
            conf = r[4]
            clsId = int(r[5])
            cls = classes[clsId]

            # Only track "person" class and above confidence threshold
            if cls == "person" and conf > CONFIDENCE_THRESHOLD:
                detections.append((coordinates, conf, cls))

        # Update tracker with detections
        tracks = object_tracker.update_tracks(detections, frame=image)

        # Draw tracking information
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            bbox = track.to_ltrb()

            cv2.rectangle(
                image,
                (int(bbox[0]), int(bbox[1])),
                (int(bbox[2]), int(bbox[3])),
                color=(0, 0, 255),
                thickness=2,  # Reduced thickness
            )
            cv2.putText(
                image,
                f"ID: {track_id}",
                (int(bbox[0]), int(bbox[1]) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,  # Smaller font size
                (0, 255, 0),
                2,
            )

    cv2.imshow("Image", image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
