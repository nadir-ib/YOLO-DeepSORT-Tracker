
# YOLO & DeepSORT Object Detection and Tracking Project
This project is designed to detect and track humans in video using YOLO for object detection and DeepSORT for tracking. It saves detected videos with timestamps and stores tracking information in a SQLite database. Additionally, if humans are detected at specific night hours, the system sends an alert email.


## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)


## Features

- **Object Detection & Tracking**: Detects and tracks humans, cats, and dogs using YOLOv5 and DeepSORT.
- **Database Logging**: Logs detection events in an SQLite database, including timestamp and video path.
- **Video Saving**: Saves video segments with tracked objects to a specified directory.
- **Email Alerts**: Sends alert emails if humans are detected at night.
- **Web Interface**: Displays database records and provides links to saved videos.

## Installation
### Clone the Repository

```bash
git clone https://github.com/nadir-ib/YOLO-DeepSORT-Tracker.git
cd YOLO-DeepSORT-Tracker
```

### Requirements

Install project dependencies by running:

```bash
pip install -r requirements.txt
```

##Configuration

Detection settings:
```bash
confidence_threshold: Minimum confidence for detections.

frame_skip: Skip frames for faster processing.
```
Tracking settings:
```bash
max_age, n_init: DeepSORT tracker settings.
```
Video recording:
```bash
output_directory: Folder to save videos.
```
Database settings:
```bash
SQLite database path.
```
Email alerts:
```bash
Configure email sender, recipients, and nighttime hours.
```

## Usage
### Run Object Detection and Tracking:
```bash
python src/main.py
```
### Start the Web Server:
For report database recorde in a webpage
```bash
python web_server.py
```
Open your browser and navigate to: http://127.0.0.1:5000




