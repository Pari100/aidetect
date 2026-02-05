#!/usr/bin/env python3
"""
Test voice_forensics_wrapper.py directly to see what error it's producing
"""
import sys
import json
import base64
import subprocess

print("=" * 80)
print("TESTING VOICE FORENSICS WRAPPER")
print("=" * 80)

# Read the sample file
sample_path = 'client/public/sample voice 1.mp3'
print(f"\nLoading sample from: {sample_path}")

try:
    with open(sample_path, 'rb') as f:
        audio_data = f.read()
    print(f"✓ Loaded {len(audio_data)} bytes")
except Exception as e:
    print(f"✗ Failed to load: {e}")
    exit(1)

# Convert to base64
audio_base64 = base64.b64encode(audio_data).decode('utf-8')
print(f"✓ Converted to base64 ({len(audio_base64)} chars)")

# Create input JSON
input_json = json.dumps({
    'audioBase64': audio_base64,
    'language': 'English'
})

print(f"✓ Created input JSON ({len(input_json)} bytes)")

# Run wrapper
print("\n" + "=" * 80)
print("RUNNING WRAPPER...")
print("=" * 80 + "\n")

try:
    result = subprocess.run(
        ['python', 'server/voice_forensics_wrapper.py'],
        input=input_json,
        capture_output=True,
        text=True,
        timeout=30,
        cwd='.'
    )
    
    print(f"Return code: {result.returncode}")
    
    if result.stdout:
        print(f"\nSTDOUT:\n{result.stdout}")
    
    if result.stderr:
        print(f"\nSTDERR:\n{result.stderr}")
    
    if result.stdout:
        try:
            output = json.loads(result.stdout.strip())
            print(f"\n✓ Valid JSON output")
            print(json.dumps(output, indent=2))
        except json.JSONDecodeError as e:
            print(f"\n✗ Invalid JSON: {e}")
            
except subprocess.TimeoutExpired:
    print("✗ Wrapper timed out after 30 seconds")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 80)
