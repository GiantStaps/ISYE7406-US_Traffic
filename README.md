# ISYE7406-US_Traffic
## Setup
`poetry install`
Warning: this will install 10GB of CUDA related packages if you don't have them already.

## Data Preping & Cleaning
`preprocessing.ipynb`

## Model Training
if you have have CUDA toolkit installed:
`train_svm.ipynb`
if you don't have a GPU accessible:
`train_per_zipcode.ipynb`

## Read about Why We Drop Zipcode
Checkout `geolocation_experiement` branch. 