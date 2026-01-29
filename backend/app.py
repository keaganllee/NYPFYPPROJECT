import os
import shutil
import glob
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
from pydub import AudioSegment
import httpx
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure FFmpeg path for pydub (fix for Windows where FFmpeg may not be in PATH)
def find_ffmpeg():
    """Find FFmpeg in common Windows installation locations"""
    # Check WinGet installation
    winget_pattern = os.path.expanduser(
        r"~\AppData\Local\Microsoft\WinGet\Packages\*ffmpeg*\**\bin"
    )
    for path in glob.glob(winget_pattern, recursive=True):
        ffmpeg_exe = os.path.join(path, "ffmpeg.exe")
        if os.path.exists(ffmpeg_exe):
            return path
    
    # Check common installation paths
    common_paths = [
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
    ]
    for path in common_paths:
        if os.path.exists(os.path.join(path, "ffmpeg.exe")):
            return path
    return None

ffmpeg_path = find_ffmpeg()
if ffmpeg_path:
    logger.info(f"Found FFmpeg at: {ffmpeg_path}")
    AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
    AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
    AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
else:
    logger.warning("FFmpeg not found! Audio conversion may fail.")

app = FastAPI()

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FISH_AUDIO_API_KEY = os.getenv("FISH_AUDIO_API_KEY")
# Default model ID if not provided - using the one user gave
MODEL_ID = "193f7f8f649b418382885c5fb4fb7109"

@app.get("/")
def read_root():
    return {"message": "RVC Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/fish")
async def fish_audio_tts(file: UploadFile = File(...)):
    if not FISH_AUDIO_API_KEY:
        logger.error("Fish Audio API Key missing")
        raise HTTPException(status_code=500, detail="Fish Audio API Key not set")

    # 1. Save temp file
    # Use system temp directory to avoid triggering Live Server reloads
    temp_dir = tempfile.gettempdir()
    temp_filename = os.path.join(temp_dir, f"temp_{file.filename}")
    wav_filename = f"{temp_filename}.wav"
    
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Received file: {temp_filename}, size: {os.path.getsize(temp_filename)}")

        # 2. Convert to WAV for SpeechRecognition
        # pydub handles format detection automatically usually
        audio = AudioSegment.from_file(temp_filename)
        audio.export(wav_filename, format="wav")
        
        # 3. Transcribe
        recognizer = sr.Recognizer()
        text = ""
        with sr.AudioFile(wav_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                logger.info(f"Transcribed text: {text}")
            except sr.UnknownValueError:
                logger.warning("Speech Recognition could not understand audio")
                return Response(content="Could not understand audio", status_code=400)
            except sr.RequestError as e:
                logger.error(f"Speech Recognition error: {e}")
                return Response(content=f"Speech Recognition error: {e}", status_code=500)

        if not text:
             return Response(content="No speech detected", status_code=400)

        # 4. Call Fish Audio (TTS)
        # Using the https://api.fish.audio/v1/tts endpoint convention
        url = "https://api.fish.audio/v1/tts"
        headers = {
            "Authorization": f"Bearer {FISH_AUDIO_API_KEY}",
            "Content-Type": "application/json" 
        }
        
        payload = {
            "text": text,
            "reference_id": MODEL_ID,
            "format": "wav"
        }

        logger.info(f"Calling Fish Audio with text: '{text}'...")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=60.0)
            
            if response.status_code != 200:
                logger.error(f"Fish Audio Error: {response.status_code} - {response.text}")
                return Response(content=f"Fish Audio API Error: {response.text}", status_code=response.status_code)
            
            logger.info("Fish Audio success")
            return Response(content=response.content, media_type="audio/wav")

    except Exception as e:
        logger.error(f"General Error: {str(e)}")
        return Response(content=f"Server Error: {str(e)}", status_code=500)
    
    finally:
        # Cleanup
        if os.path.exists(temp_filename): os.remove(temp_filename)
        if os.path.exists(wav_filename): os.remove(wav_filename)
