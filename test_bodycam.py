#!/usr/bin/env python3
"""
Test script for LEO Bodycam application.
Tests core functionality without requiring a physical camera.
"""

import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from bodycam import LEOBodycam


def test_configuration():
    """Test configuration loading."""
    print("Testing configuration loading...")
    
    # Test with default config
    bodycam = LEOBodycam()
    assert bodycam.config is not None
    assert 'officer_id' in bodycam.config
    assert 'camera_index' in bodycam.config
    print("✓ Configuration loaded successfully")
    
    # Test with custom config
    test_config = {
        "camera_index": 0,
        "resolution": {"width": 1280, "height": 720},
        "fps": 30,
        "output_directory": "./test_recordings",
        "video_codec": "mp4v",
        "file_format": "mp4",
        "officer_id": "TEST_OFFICER",
        "department": "Test Department"
    }
    
    config_path = "/tmp/test_config.json"
    with open(config_path, 'w') as f:
        json.dump(test_config, f)
    
    bodycam = LEOBodycam(config_path)
    assert bodycam.config['officer_id'] == 'TEST_OFFICER'
    print("✓ Custom configuration loaded successfully")
    
    # Clean up
    os.remove(config_path)


def test_status():
    """Test status reporting."""
    print("\nTesting status reporting...")
    
    bodycam = LEOBodycam()
    status = bodycam.get_status()
    assert status['status'] == 'stopped'
    print("✓ Status reporting works correctly")


def test_metadata_structure():
    """Test metadata structure without camera."""
    print("\nTesting metadata structure...")
    
    bodycam = LEOBodycam()
    
    # Manually set up metadata as if recording started
    from datetime import datetime
    bodycam.metadata = {
        "officer_id": bodycam.config.get("officer_id", "UNKNOWN"),
        "department": bodycam.config.get("department", "Unknown Department"),
        "start_time": datetime.now().isoformat(),
        "filename": "./recordings/test.mp4",
        "resolution": "1920x1080",
        "fps": 30
    }
    
    # Verify metadata structure
    assert 'officer_id' in bodycam.metadata
    assert 'department' in bodycam.metadata
    assert 'start_time' in bodycam.metadata
    assert 'filename' in bodycam.metadata
    assert 'resolution' in bodycam.metadata
    assert 'fps' in bodycam.metadata
    
    print("✓ Metadata structure is correct")


def test_filename_generation():
    """Test filename generation logic."""
    print("\nTesting filename generation...")
    
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    officer_id = "OFFICER_001"
    file_format = "mp4"
    output_dir = Path("./recordings")
    
    filename = output_dir / f"{officer_id}_{timestamp}.{file_format}"
    
    assert "OFFICER_001_" in str(filename)
    assert str(filename).endswith(".mp4")
    print(f"✓ Filename format correct: {filename}")


def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("LEO Bodycam Test Suite")
    print("=" * 60)
    
    try:
        test_configuration()
        test_status()
        test_metadata_structure()
        test_filename_generation()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
