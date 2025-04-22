
# B-AI_Agent_Chatbot 
# 🤖 B-AI Agent Chatbot (LangGraph + Groq + Tavily) — FastAPI + Streamlit + Docker

This project is an intelligent **AI Agent Chatbot** built using **LangGraph**, powered by **Groq API** for ultra-fast LLM responses, and enriched with **Tavily API** for web search capabilities. It features a **FastAPI** backend and **Streamlit** frontend, fully containerized with Docker for local or cloud deployment.

---

## 🧠 Features

- Conversational AI with **LangGraph**
- Ultra-fast inference with **Groq API**
- Real-time search via **Tavily API**
- FastAPI backend with Swagger UI
- Streamlit-powered UI for interaction
- Full Docker support
- API-first development
- Ready for local or cloud deployment


---

## 🧠 Features

- Conversational AI using LLMs
- FastAPI-powered backend with API endpoints
- Swagger UI for interactive API testing
- Streamlit frontend interface
- Dockerized backend & frontend
- Push and pull Docker images to/from Docker Hub
- Deploy locally or on cloud servers

---

## 📁 Project Structure

```
B-AI_Agent_Chatbot/
    ├── app.py
    ├── ui.py
    ├── Dockerfile
    ├── requirements.txt
    └── README.md
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com//ai-agent-chatbot.git
cd B-AI_Agent_Chatbot

```

---

## 🛠 Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Access Swagger UI: `http://127.0.0.1:8000/docs`

---

## 🎨 Frontend Setup (Streamlit)

```bash
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
```

Access Streamlit App: `http://localhost:8501`

---

## 🧪 Demo Workflow

1. Start the backend FastAPI app  
2. Launch the Streamlit frontend  
3. Enter your message and chat with the AI agent  
4. Watch the AI's response generated via backend API  

---

## 🐳 Docker Deployment

### 1. Build the Docker Image

```bash
docker build -t b-ai-agent-app .
```

### 2. Run the Docker Container

```bash
docker run -d -p 8000:8000 -p 8501:8501 b-ai-agent-app
```
<!-- 
### 3. Push Image to Docker Hub

```bash
docker tag ai-agent-app your-dockerhub-username/b-ai-agent-app
docker push your-dockerhub-username/ai-agent-app
```

### 4. Pull Image from Docker Hub

```bash
docker pull your-dockerhub-username/ai-agent-app
```

### 5. Deploy Locally via Docker Compose

```bash
docker-compose up --build
``` -->

---

## 🧾 Dockerfile Example

```dockerfile
# Use official Python runtime as a parent image
FROM python:3.9-slim
# Copy the application code
COPY . /app/
# Set the working directory to /app
WORKDIR /app
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Expose the ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501
# Start both FastAPI and Streamlit servers
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run ui.py --server.port 8501 --server.address 0.0.0.0"]
```

---

## 🧰 Technologies Used

- FastAPI
- Streamlit
- Python 3.10
- Docker / Docker Hub

---

## 🔍 Swagger UI

View and test API endpoints at:  
**`http://localhost:8000/docs`**

---

## 📺 Streamlit App

Chat with the AI bot at:  
**`http://localhost:8501`**

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Got ideas or improvements? Fork and submit a pull request!

---

## 📞 Contact

Developed by **H.M.Badhon**  
📧 Email: h.m.badhoneee@gmail.com  
🔗 GitHub: [hm-badhon](https://github.com/hm-badhon)

