# Grocery Computer Vision Project

This repository contains code and assets for grocery product classification, training, and data ingestion using computer vision and machine learning.

## Directory Structure

- `src/` - Source code for app, training, ingestion, and utilities
- `assets/` - Model files, label maps, images, and metadata
- `notebooks/` - Jupyter notebooks for data exploration, training, and inference
- `mlruns/` - MLflow runs and models
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container setup for running the app and scripts

## Getting Started

### Build Docker Image

```sh
docker build -t grocery-cv-app .
```

### Run Streamlit App

```sh
docker run -p 8000:8000 grocery-cv-app
```

### Run Training or Ingestion Scripts

Override the default command to run training or ingestion:

```sh
 docker run grocery-cv-app python src/train.py

 docker run grocery-cv-app python src/data_ingestion.py
```

## Customization

- Update `requirements.txt` to add/remove Python packages.
- Modify `src/app.py`, `src/train.py`, or `src/data_ingestion.py` as needed.

