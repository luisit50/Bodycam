# LEO Bodycam

A Law Enforcement Officer (LEO) bodycam recording system with metadata tracking and evidence management capabilities.

## Features

- **Video Recording**: High-quality video recording with configurable resolution and frame rate
- **Metadata Tracking**: Automatic tracking of officer ID, department, timestamps, and recording details
- **Evidence Management**: Secure file storage with chain of custody metadata
- **Timestamp Overlay**: Real-time timestamp and officer ID displayed on video
- **Configuration**: JSON-based configuration for easy customization
- **Command-Line Interface**: Simple CLI for starting/stopping recordings

## Installation

1. Clone the repository:
```bash
git clone https://github.com/luisit50/Bodycam.git
cd Bodycam
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.json` to customize settings:

```json
{
  "camera_index": 0,
  "resolution": {
    "width": 1920,
    "height": 1080
  },
  "fps": 30,
  "output_directory": "./recordings",
  "video_codec": "mp4v",
  "file_format": "mp4",
  "officer_id": "OFFICER_001",
  "department": "Sample Police Department"
}
```

## Usage

### Start Recording

```bash
python src/bodycam.py
```

The recording will continue until you press `Ctrl+C`.

### Record for Specific Duration

```bash
python src/bodycam.py --duration 60
```

This will record for 60 seconds and then automatically stop.

### Check Status

```bash
python src/bodycam.py --status
```

### Custom Configuration

```bash
python src/bodycam.py --config /path/to/custom_config.json
```

## Output

Recordings are saved to the `recordings/` directory (configurable) with the following naming convention:

```
{OFFICER_ID}_{TIMESTAMP}.mp4
{OFFICER_ID}_{TIMESTAMP}_metadata.json
```

### Metadata File

Each recording includes a metadata JSON file with:
- Officer ID
- Department
- Start and end timestamps
- Resolution and frame rate
- Filename

Example metadata:
```json
{
  "officer_id": "OFFICER_001",
  "department": "Sample Police Department",
  "start_time": "2026-02-14T05:15:30.123456",
  "end_time": "2026-02-14T05:16:30.456789",
  "filename": "./recordings/OFFICER_001_20260214_051530.mp4",
  "resolution": "1920x1080",
  "fps": 30
}
```

## Requirements

- Python 3.7+
- OpenCV (opencv-python)
- NumPy
- Webcam or video capture device

## License

This project is provided as-is for law enforcement and security applications.