# -----------------------------
# 🐳 Base image: a lightweight Python environment
# -----------------------------
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# -----------------------------
# 🏠 Set the working directory inside the container
# -----------------------------
WORKDIR /app

# -----------------------------
# ⚙️ Install system dependencies (optional but useful for numpy, pillow, etc.)
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 📦 Install Python dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 📂 Copy project files into container
# -----------------------------
# Copy your app code and support folders
COPY app ./app
COPY src ./src
COPY assets ./assets
COPY .streamlit ./.streamlit
COPY README.md .

# -----------------------------
# 🌐 Expose Streamlit’s default port
# -----------------------------
EXPOSE 8501

# -----------------------------
# ⚙️ Environment settings for Streamlit
# -----------------------------
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false

# -----------------------------
# 🚀 Run your Streamlit app
# -----------------------------
CMD ["streamlit", "run", "app/main.py"]
