FROM python:3.7-slim AS dev

EXPOSE 8501

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# --------------------
FROM dev

ENV PORT=8501

COPY src/ /app/
CMD streamlit run pixela_chart.py --server.port $PORT
