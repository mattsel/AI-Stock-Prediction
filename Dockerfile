FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "gunicorn_entry_point:app"]
