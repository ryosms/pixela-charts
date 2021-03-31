# pixela-charts

## Running locally

```console
$ docker-compose up
# or
$ docker-compose run --service-port streamlit streamlit run your_streamlit_app.py
```

## Deploy to Cloud Run

<https://cloud.google.com/run/docs/quickstarts/build-and-deploy>

1. Create a Google Cloud Project for `pixela-chart`
1. Enable billing
1. Install CloudSDK and initialize
1. Build Docker image
    ```console
    $ gcloud builds submit --tag gcr.io/<YOUR-PROJECT-ID-HERE>/pixela-chart:latest
    ```
1. Deploy to Cloud Run
    ```console
    $ gcloud run deploy --image gcr.io/<YOUR-PROJECT-ID-HERE>/pixela-chart:latest --platform managed
    ```
