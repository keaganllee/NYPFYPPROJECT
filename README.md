# Face & Voice Tracking Project (NYPFYPPROJECT)

This project combines 3D Face & Body Tracking with real-time Voice Conversion and AI Text-to-Speech.

## Features
- **3D Tracking:** Real-time face and full-body tracking using Mediapipe.
- **Voice Changer:** Real-time pitch shifting using Tone.js.
- **AI TTS:** Integration with Fish Audio for high-quality AI voice generation ("Elmo" voice).

## Prerequisites
1. **Python 3.13.9** installed.
2. **FFmpeg** installed and added to your system PATH (or configured in `backend/app.py`).
3. **Git** installed.
   - *PowerShell* (Windows): `winget install Git.Git`
   - *Verification:* Run `git --version` in your terminal.
4. **Internet Connection** (required for CDN scripts & Fish Audio API).

## Downloading the Project

Since this is a public repository, you can verify if you have the files by cloning it.

### Option A: With a GitHub Account (Recommended)
If you have a GitHub account and have set up your keys:
```bash
git clone https://github.com/keaganllee/NYPFYPPROJECT.git
```

### Option B: Without a GitHub Account (Public Access)
You can clone public repositories using HTTPS without needing to sign in:
```bash
git clone https://github.com/keaganllee/NYPFYPPROJECT.git
```
*Note: You will be able to download the code, but you cannot push changes back to the repository without an account and permissions.*

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

   #### Optional: Live Server Extension (VS Code)
   If you prefer not to use Python's built-in HTTP server, you can use the **Live Server** extension for VS Code.
   1. Open VS Code extensions (`Ctrl+Shift+X`).
   2. Search for **"Live Server"** (by Ritwick Dey).
   3. Install it.
   4. Right-click `index.html` in the file explorer and select **"Open with Live Server"**.
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
