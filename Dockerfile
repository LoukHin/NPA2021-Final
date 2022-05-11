FROM python:3.11.0b1-bullseye

WORKDIR /app

COPY requirement.txt .

RUN ["pip", "install", "-r", "requirement.txt"]

COPY 62070184-bot.py .

CMD ["python3", "62070184-bot.py"]
