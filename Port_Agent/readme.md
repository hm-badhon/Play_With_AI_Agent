
# 🚢 PortAgent: ASR + Agent AI for Port Logistics Automation

**PortAgent** is an intelligent system that automates transcription of port-related voice recordings and extracts structured data using a local Large Language Model (LLM). It integrates **Automatic Speech Recognition (ASR)** with **Agent AI** to deliver actionable insights for port logistics operations.

---

## 🔍 Features

- 🎙️ **Speech Recognition**: Transcribes audio files (MP3, WAV, etc.) into text using Google Speech Recognition.
- 🤖 **Agent AI with Local LLM**: Leverages a local LLM (e.g., **Mistral** or **LLaMA** via Ollama) to extract structured data from transcriptions.
- 📁 **Audio Format Support**: Converts unsupported audio formats to WAV using `pydub` and `ffmpeg`.
- 🧠 **Context-Aware Extraction**: Validates ship names, parses time, and extracts container and company data.
- 💾 **Structured Output**: Saves extracted data in a `.json` file for easy integration.

---

## 🧠 Domains

- **Automatic Speech Recognition (ASR)**: Converts spoken port logistics reports into structured text.
- **Agent AI**: Uses a local LLM (Mistral or LLaMA) to intelligently parse and structure data for logistics automation.

---

## 📦 Requirements

- Python 3.8+
- `ffmpeg` and `ffprobe` installed and available in the system path
- [Ollama](https://ollama.com/) installed locally with a supported LLM (e.g., `mistral` or `llama3.2:1b`)

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/port-agent.git
cd port-agent
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install `ffmpeg`:

```bash
# On Ubuntu/Debian
sudo apt install ffmpeg
# On macOS
brew install ffmpeg
```

4. Set up Ollama and pull a local LLM model:

```bash
# Install Ollama (follow instructions at https://ollama.com/)
ollama pull mistral
# or
ollama pull llama3.2:1b
```

5. Run Ollama with your chosen model:

```bash
ollama run mistral
# or
ollama run llama3.2:1b
```

> **Note**: The **Mistral** model is recommended for robust performance in structured data extraction. The **LLaMA 3.2 (1B)** model is suitable for lightweight deployments with lower resource requirements.

---

## ▶️ Usage

Run the main script to process an audio file:

```bash
python port_agent.py
```

By default, the script processes the sample audio file located at:

```python
datasets/ElevenLabs_Text_to_Speech_audio.mp3
```

The extracted data is saved to:

```json
extracted_data.json
```

---

## 📥 Input Format

The input audio should contain logistics-related phrases, such as:

> "This is a report from ship name: 94W4F32, which docked at 3:00 p.m. The vessel has flagged 10 containers designated for ABC Company."

---

## 📤 Output Format

The extracted data is saved as a JSON file, e.g.:

```json
{
  "ship_name": "94W4F32",
  "reach_time": "15:00",
  "containers_unloaded": 10,
  "company_name": "ABC Company"
}
```

---

## 🚧 To-Do

- [ ] Build a Streamlit web UI for audio uploads and real-time feedback
- [ ] Develop a FastAPI endpoint for API-based integration
- [ ] Add support for history/log export
- [ ] Implement multi-language support for ASR

---

## 📁 Project Structure

```
port-agent/
├── port_agent.py           # Main script for ASR and Agent AI
├── datasets/               # Sample audio files
├── extracted_data.json     # Output JSON file
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 👨‍💻 Author

Built by **H.M. Badhon**  
Domains: **ASR + Agent AI for Port Operations**

---

## 🛠 Notes on Local LLMs

- **Mistral**: A high-performance model optimized for structured data extraction, ideal for most use cases.
- **LLaMA 3.2 (1B)**: A lightweight model for resource-constrained environments, offering good accuracy with lower computational requirements.
- Both models run locally via [Ollama](https://ollama.com/), ensuring data privacy and offline capability.
