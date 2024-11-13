# ISYE7406-US_Traffic
## Environment Setup
`poetry install`

Warning: this env is for GPU training and will install 10GB of CUDA related packages if you don't have them already.
Another env will be released for only running the pre-trained model on the app.

`cd ui && npm install` to install dependencies for the frontend

## Run App

### Flask

`flask run --port=5001`   # Starts the Flask app on port 5001

### React
`cd ui && npm start` to start an instance in your browser

## Look up all the data processing & training
Go to folder *experiment*.

