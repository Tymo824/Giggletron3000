# Use an official Python image as the base
FROM python:3.11-slim

# Install ffmpeg and other helpful tools
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your code into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port Render expects (even if not used directly)
EXPOSE 10000

# Run your bot
CMD ["python", "bot.py"]
