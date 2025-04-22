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