#!/usr/bin/env python3
"""
Test the API endpoint directly to see what it returns
"""
import requests
import base64
import json
import time

print("=" * 70)
print("TESTING API ENDPOINT DIRECTLY")
print("=" * 70)

# Read the sample audio file
sample_path = 'client/public/sample voice 1.mp3'
try:
    with open(sample_path, 'rb') as f:
        audio_data = f.read()
    print(f"\n✓ Loaded sample file: {sample_path}")
    print(f"  File size: {len(audio_data)} bytes")
except Exception as e:
    print(f"✗ Failed to load sample: {e}")
    exit(1)

# Convert to base64
audio_base64 = base64.b64encode(audio_data).decode('utf-8')
print(f"\n✓ Converted to base64")
print(f"  Base64 length: {len(audio_base64)} characters")

# Prepare API request
api_url = "http://localhost:3000/api/voiceDetection/detect"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "sk_test_123456789"
}

payload = {
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": audio_base64
}

print(f"\n✓ Prepared request to: {api_url}")
print(f"  Headers: {headers}")
print(f"  Payload size: {len(json.dumps(payload))} bytes")

# Test if server is running
print("\n" + "=" * 70)
print("CHECKING IF SERVER IS RUNNING...")
print("=" * 70)

try:
    response = requests.get("http://localhost:3000/", timeout=2)
    print("✓ Server is running on port 3000")
except requests.exceptions.ConnectionError:
    print("✗ Server is NOT running on port 3000")
    print("  Starting server...")
    time.sleep(2)
except Exception as e:
    print(f"⚠ Server check error: {e}")

# Make the request
print("\n" + "=" * 70)
print("SENDING API REQUEST...")
print("=" * 70)

try:
    print(f"\nPOST {api_url}")
    response = requests.post(api_url, json=payload, headers=headers, timeout=30)
    
    print(f"\n✓ Response Status: {response.status_code}")
    print(f"✓ Response Headers: {dict(response.headers)}")
    
    result = response.json()
    print(f"\n✓ Response Body:")
    print(json.dumps(result, indent=2))
    
    if response.status_code == 200:
        classification = result.get('classification')
        confidence = result.get('confidenceScore')
        explanation = result.get('explanation')
        
        print(f"\n" + "=" * 70)
        print("DETECTED RESULT:")
        print("=" * 70)
        print(f"Classification: {classification}")
        print(f"Confidence: {confidence}")
        print(f"Explanation: {explanation}")
        
        # Check if it matches expected
        if classification == 'AI_GENERATED' and confidence >= 0.9:
            print("\n✓ CORRECT! Sample correctly detected as AI")
        else:
            print(f"\n✗ UNEXPECTED! Expected AI_GENERATED with high confidence")
            print(f"  Got: {classification} ({confidence})")
    else:
        print(f"\n✗ Request failed with status {response.status_code}")
        print(f"  Error: {result}")
        
except requests.exceptions.ConnectionError as e:
    print(f"✗ Connection error - Server not running: {e}")
    print("\n  Please start the server with:")
    print("  npm run dev")
    
except requests.exceptions.Timeout:
    print(f"✗ Request timeout - Server may be slow or crashed")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
