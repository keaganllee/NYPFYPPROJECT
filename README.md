# Face & Voice Tracking Project (NYPFYPPROJECT)

This project combines 3D Face & Body Tracking with real-time Voice Conversion and AI Text-to-Speech.

## Features
- **3D Tracking:** Real-time face and full-body tracking using Mediapipe.
- **Voice Changer:** Real-time pitch shifting using Tone.js.
- **AI TTS:** Integration with Fish Audio for high-quality AI voice generation ("Elmo" voice).

## Prerequisites
1. **Python 3.13.9** installed.
2. **FFmpeg** installed and added to your system PATH (or configured in `backend/app.py`).
3. **Internet Connection** (required for CDN scripts & Fish Audio API).

## Setup & Running

### Backend
1. Open a terminal in the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app:app --reload
   ```
   The backend runs on `http://localhost:8000`.

### Frontend
1. Open a terminal in the `frontend` or root directory.
2. Run a simple HTTP server (or use VS Code Live Server):
   ```bash
   python -m http.server 3000
   ```
   *Note: If using VS Code Live Server, ensure it runs on port 3000 or update the backend CORS settings if needed.*
3. Open `http://localhost:3000` in your browser.

## Configuration (IMPORTANT)

This project requires specific API keys and Model IDs to function correctly. **Please refer to the exact file and line numbers below to make changes.**

### 1. Fish Audio API Key
To enable the AI voice features (Text-to-Speech), you must provide your Fish Audio API Key.

*   **Primary Configuration (Backend):**
    *   **File:** `backend/app.py`
    *   **Line:** **60**
    *   **Code:** `FISH_AUDIO_API_KEY = os.getenv("FISH_AUDIO_API_KEY")`
    *   **Action:** Ideally, set the `FISH_AUDIO_API_KEY` environment variable in your system. Alternatively, you can temporarily replace `os.getenv("FISH_AUDIO_API_KEY")` with your actual key string (e.g., `"your_key_here"`), but **do not commit this to version control**.

*   **Test Script:**
    *   **File:** `test_fish_api.py`
    *   **Line:** **11**
    *   **Code:** `'Authorization': 'Bearer (YOUR API KEY)',`
    *   **Action:** Update the string after `Bearer` with your actual API key to run `python test_fish_api.py` and verify your key works directly.

### 2. Model ID (Voice Reference)
The "Reference ID" determines which voice model is used for generation. Use this to change the character voice.

*   **Primary Configuration (Backend):**
    *   **File:** `backend/app.py`
    *   **Line:** **62**
    *   **Code:** `MODEL_ID = "193f7f8f649b418382885c5fb4fb7109"`
    *   **Action:** Replace the ID string `"193f7f8f..."` with your desired Fish Audio model reference ID.

*   **Test Script:**
    *   **File:** `test_fish_api.py`
    *   **Line:** **7**
    *   **Code:** `'reference_id': '193f7f8f649b418382885c5fb4fb7109',`
    *   **Action:** Update this ID if you want to test a different voice model using the test script.
