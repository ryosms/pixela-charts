FROM python:3.7-slim AS dev

EXPOSE 8501

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# --------------------
FROM dev

ENV PORT=8501

# Workaround for Cloud Run
# watching: https://github.com/streamlit/streamlit/issues/3028
RUN find /usr/local/lib/python3.7/site-packages/streamlit -type f \( -iname \*.py -o -iname \*.js \) -print0 | xargs -0 sed -i 's/healthz/health-check/g'

COPY src/ /app/
CMD streamlit run pixela_chart.py --server.port $PORT
