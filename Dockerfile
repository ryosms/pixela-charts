FROM python:3.7-slim

EXPOSE 8501
WORKDIR /app

RUN pip install streamlit
