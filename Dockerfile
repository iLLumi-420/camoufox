FROM python:3.11-slim


RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates


# Install system dependencies required for Camoufox / Playwright
RUN apt-get update && \
    apt-get install -y wget unzip libgtk-3-0 libdbus-glib-1-2 libx11-xcb1 libxt6 \
    libxcomposite1 libxdamage1 libxrandr2 libasound2 libatk1.0-0 libatk-bridge2.0-0 \
    libnss3 libdrm2 libgbm1 libpangocairo-1.0-0 libpango-1.0-0 && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy pre-cache script and run it to download Camoufox binary at build time
COPY pre_cache_camoufox.py .
RUN python3 pre_cache_camoufox.py
RUN rm pre_cache_camoufox.py

# Copy the app code
COPY app ./app

# Expose port
EXPOSE 8000

# Start FastAPI using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
