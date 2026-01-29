"""
Quick test script to verify Speech-to-Text is working correctly.
This tests the SpeechRecognition library with Google's API.
"""
import speech_recognition as sr
import os

def test_stt_with_microphone():
    """Test STT by recording from microphone for 5 seconds"""
    recognizer = sr.Recognizer()
    
    print("Testing microphone input...")
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Say something (5 seconds)...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing...")
            text = recognizer.recognize_google(audio)
            print(f"SUCCESS - Transcribed: '{text}'")
            return True
        except sr.UnknownValueError:
            print("ERROR - Could not understand audio")
            return False
        except sr.RequestError as e:
            print(f"ERROR - Google API request failed: {e}")
            return False
        except sr.WaitTimeoutError:
            print("ERROR - No speech detected within timeout")
            return False

def test_stt_with_file(filepath):
    """Test STT with an audio file"""
    if not os.path.exists(filepath):
        print(f"ERROR - File not found: {filepath}")
        return False
    
    recognizer = sr.Recognizer()
    print(f"Testing with file: {filepath}")
    
    try:
        with sr.AudioFile(filepath) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(f"SUCCESS - Transcribed: '{text}'")
            return True
    except sr.UnknownValueError:
        print("ERROR - Could not understand audio (empty or unclear)")
        return False
    except sr.RequestError as e:
        print(f"ERROR - Google API request failed: {e}")
        return False
    except Exception as e:
        print(f"ERROR - {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Speech-to-Text Test")
    print("=" * 50)
    
    # Check if PyAudio is available for microphone test
    try:
        import pyaudio
        print("\n1. Testing with microphone...")
        test_stt_with_microphone()
    except ImportError:
        print("\n1. Skipping microphone test (PyAudio not installed)")
    
    # Test with a sample WAV file if one exists in the current directory
    print("\n2. Looking for test WAV files...")
    wav_files = [f for f in os.listdir('.') if f.endswith('.wav')]
    if wav_files:
        for wav in wav_files[:1]:  # Test just the first one
            test_stt_with_file(wav)
    else:
        print("   No WAV files found in current directory")
        print("   To test with a file, record something and save as test.wav")
    
    print("\n" + "=" * 50)
    print("Test complete!")
