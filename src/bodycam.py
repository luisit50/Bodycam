#!/usr/bin/env python3
"""
LEO Bodycam Application
A Law Enforcement Officer bodycam recording system with metadata tracking
and evidence management capabilities.
"""

import cv2
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path


class LEOBodycam:
    """Main bodycam controller class."""
    
    def __init__(self, config_path="config.json"):
        """
        Initialize the bodycam system.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.recording = False
        self.video_writer = None
        self.camera = None
        self.current_filename = None
        self.metadata = {}
        
    def _load_config(self, config_path):
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_path}' not found.")
            print("Using default configuration.")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            print("Using default configuration.")
            return self._get_default_config()
    
    def _get_default_config(self):
        """Return default configuration."""
        return {
            "camera_index": 0,
            "resolution": {"width": 1920, "height": 1080},
            "fps": 30,
            "output_directory": "./recordings",
            "video_codec": "mp4v",
            "file_format": "mp4",
            "officer_id": "OFFICER_001",
            "department": "Sample Police Department"
        }
    
    def start_recording(self):
        """Start video recording."""
        if self.recording:
            print("Recording is already in progress.")
            return False
        
        # Initialize camera
        self.camera = cv2.VideoCapture(self.config["camera_index"])
        if not self.camera.isOpened():
            print("Error: Could not open camera.")
            return False
        
        # Set camera resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["resolution"]["width"])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["resolution"]["height"])
        self.camera.set(cv2.CAP_PROP_FPS, self.config["fps"])
        
        # Create output directory if it doesn't exist
        output_dir = Path(self.config["output_directory"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        officer_id = self.config.get("officer_id", "UNKNOWN")
        self.current_filename = output_dir / f"{officer_id}_{timestamp}.{self.config['file_format']}"
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*self.config["video_codec"])
        self.video_writer = cv2.VideoWriter(
            str(self.current_filename),
            fourcc,
            self.config["fps"],
            (self.config["resolution"]["width"], self.config["resolution"]["height"])
        )
        
        if not self.video_writer.isOpened():
            print("Error: Could not initialize video writer.")
            self.camera.release()
            return False
        
        # Initialize metadata
        self.metadata = {
            "officer_id": self.config.get("officer_id", "UNKNOWN"),
            "department": self.config.get("department", "Unknown Department"),
            "start_time": datetime.now().isoformat(),
            "filename": str(self.current_filename),
            "resolution": f"{self.config['resolution']['width']}x{self.config['resolution']['height']}",
            "fps": self.config["fps"]
        }
        
        self.recording = True
        print(f"Recording started: {self.current_filename}")
        print(f"Officer: {self.metadata['officer_id']}")
        print(f"Start time: {self.metadata['start_time']}")
        return True
    
    def stop_recording(self):
        """Stop video recording and save metadata."""
        if not self.recording:
            print("No recording in progress.")
            return False
        
        self.recording = False
        
        # Update metadata with end time
        self.metadata["end_time"] = datetime.now().isoformat()
        
        # Release resources
        if self.video_writer:
            self.video_writer.release()
        if self.camera:
            self.camera.release()
        
        # Save metadata to JSON file
        metadata_filename = str(self.current_filename).replace(
            f".{self.config['file_format']}", 
            "_metadata.json"
        )
        try:
            with open(metadata_filename, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            print(f"Recording stopped: {self.current_filename}")
            print(f"Metadata saved: {metadata_filename}")
        except Exception as e:
            print(f"Error saving metadata: {e}")
        
        return True
    
    def record_frame(self):
        """Capture and write a single frame."""
        if not self.recording:
            return False
        
        ret, frame = self.camera.read()
        if ret:
            # Add timestamp overlay to frame
            timestamp_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(
                frame,
                timestamp_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )
            
            # Add officer ID overlay
            officer_text = f"Officer: {self.config.get('officer_id', 'UNKNOWN')}"
            cv2.putText(
                frame,
                officer_text,
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )
            
            self.video_writer.write(frame)
            return True
        return False
    
    def run(self, duration=None):
        """
        Run the recording loop.
        
        Args:
            duration: Optional recording duration in seconds. If None, records until interrupted.
        """
        if not self.start_recording():
            return
        
        try:
            start_time = time.time()
            
            print("Recording... Press Ctrl+C to stop.")
            while self.recording:
                if not self.record_frame():
                    print("Error capturing frame.")
                    break
                
                # Check duration limit if specified
                if duration and (time.time() - start_time) >= duration:
                    print(f"\nReached duration limit of {duration} seconds.")
                    break
                
        except KeyboardInterrupt:
            print("\nRecording interrupted by user.")
        finally:
            self.stop_recording()
    
    def get_status(self):
        """Get current recording status."""
        if self.recording:
            return {
                "status": "recording",
                "filename": str(self.current_filename),
                "officer_id": self.metadata.get("officer_id"),
                "start_time": self.metadata.get("start_time")
            }
        else:
            return {
                "status": "stopped"
            }


def main():
    """Main entry point for the bodycam application."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="LEO Bodycam - Law Enforcement Officer Bodycam Recording System"
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        help='Recording duration in seconds (default: unlimited)'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Display system status and exit'
    )
    
    args = parser.parse_args()
    
    bodycam = LEOBodycam(config_path=args.config)
    
    if args.status:
        status = bodycam.get_status()
        print(json.dumps(status, indent=2))
        return
    
    # Run recording
    bodycam.run(duration=args.duration)


if __name__ == "__main__":
    main()
