# Bilingual Text-to-Speech (Amharic & English) 🇪🇹🇺🇸

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Open in Spaces](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue.svg)](https://huggingface.co/spaces/your-username/amharic-english-tts)

<div align="center">
  <img src="assets/demo.png" alt="Bilingual TTS Interface" width="800">
  <br>
  <em>Convert text to natural speech in Amharic and English</em>
</div>

## Features ✨
- 🌍 Bilingual interface (Amharic/English)
- 🗣️ Four natural-sounding voices:
  - Amharic: Ameha (Male) & Mekdes (Female)
  - English: Ryan (Male) & Clara (Female)
- ⚡ Real-time audio generation
- 🎧 In-browser audio playback
- 🎨 Gradient-themed UI
- ⏱️ 30-second timeout protection
- 🔄 Dynamic voice selection based on language

## Supported Voices 🎶
| Language  | Name   | Gender | Voice ID           |
|-----------|--------|--------|--------------------|
| Amharic 🇪🇹 | Ameha  | Male   | `am-ET-AmehaNeural`|
| Amharic 🇪🇹 | Mekdes | Female | `am-ET-MekdesNeural`|
| English 🇺🇸 | Ryan   | Male   | `en-GB-RyanNeural` |
| English 🇺🇸 | Clara  | Female | `en-CA-ClaraNeural` |

## Installation 💻
```bash
git clone https://github.com/snackshell/bilingual-tts.git
cd bilingual-tts
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
