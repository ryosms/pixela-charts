FROM python:3.7-slim AS dev

EXPOSE 8501
WORKDIR /app

RUN pip install streamlit==0.79.0

# --------------------
FROM dev

COPY src/ /app/
CMD ["streamlit", "run", "pixela_chart.py"]
