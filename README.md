
# 🧠 AI Voice Assistant with Wake Word Activation

A Python-based voice assistant that activates with a wake word, listens to your voice commands, transcribes speech using Whisper, generates intelligent responses using Google's Gemini API, and replies using text-to-speech.

---

## 🔧 Features

- 🔊 Wake word detection with Porcupine
- 🎙️ Real-time speech detection using WebRTC VAD
- ✍️ Transcription using OpenAI Whisper
- 🤖 LLM integration with Gemini API (via Google Generative AI)
- 🗣️ Text-to-speech using pyttsx3
- 🔚 Clean shutdown via voice commands

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8 or above
- A working microphone
- Internet connection (for Gemini API)

### 📦 Installation

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

---

## 🔐 API Keys & Secrets

Create a `.env` file in the root directory with the following content:

```
ACCESS_KEY=your_porcupine_access_key
GEMINI_API_KEY=your_gemini_api_key
```


---

## 📁 Directory Structure

```
├── my_assistant.py             # Main assistant logic
├── launch_assistant.pyw        # Launcher (GUI-less)
├── .env                        # API keys (not tracked by Git)
├── requirements.txt            # All dependencies
├── command.wav                 # Temporary voice input file
├── stop_check.wav              # Optional sound file
├── chop-chop_en_windows_v3_0_0/  # Wake word model
├── assistant.log               # Optional log file
└── .gitignore                  # Prevents leaking secrets
```

---

## 🧪 Usage

Double-click `launch_assistant.pyw` (if you're on Windows), or run:

```bash
python my_assistant.py
```

Then say **"chop chop"** to activate the assistant and speak your command.

Say **"shut down"**, **"exit"**, or **"goodbye"** to stop the assistant.

---

## 🐞 Troubleshooting

- ❌ *Wake word not detected?*  
  Make sure your microphone is active and selected.

- ❌ *TTS not working?*  
  Check your system volume and Python `pyttsx3` voice settings.

- ❌ *Gemini error?*  
  Make sure your `.env` contains a valid `GEMINI_API_KEY`.

---

## 🙌 Acknowledgments

- [🐍 Porcupine by Picovoice](https://picovoice.ai/)
- [🧠 Whisper by OpenAI](https://github.com/openai/whisper)
- [🌐 Google Gemini](https://ai.google.dev/)
- [🔉 WebRTC VAD](https://github.com/wiseman/py-webrtcvad)
- [🔈 pyttsx3 for TTS](https://pyttsx3.readthedocs.io/en/latest/)

---

## 📃 License

This project is licensed under the MIT License. See `LICENSE` for details.
```

