FROM python:3.13-slim
WORKDIR /app
COPY app.py ./
COPY public/ ./public/
ENV PORT=8000
ENV AKUNTANSIKU_DB=/app/data/database.db
VOLUME ["/app/data", "/app/backup"]
EXPOSE 8000
CMD ["python", "app.py"]
