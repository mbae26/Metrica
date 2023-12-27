# EVALEDGE

## Introduction

Welcome to **EVALEDGE** - an innovative platform designed to streamline the evaluation and benchmarking of machine learning (ML) models. Our service automates the rigorous process of ML model assessment, pivotal in both academic research and practical applications. EVALEDGE allows users to submit their pre-trained ML models (currently supporting `joblib` format, with more formats coming soon) along with training and testing datasets for comprehensive evaluation.

## Key Features

- **Automated Model Benchmarking**: Submit pre-trained ML models for evaluation using user-provided datasets.
- **Traditional ML Model Support**: Compatibility with various traditional ML models for benchmarking.
- **Comparative Analysis**: Generate detailed comparative tables showcasing the performance of submitted models against traditional ML models.
- **Insightful Visualizations**: Graphical representations to elucidate model performance and behavior, aiding in deeper understanding and analysis.

## Project Structure

EVALEDGE is meticulously structured for efficiency and scalability:

EVALEDGE/
│
├── app/
│ ├── main/ # Core application routes and utilities
│ ├── templates/ # HTML templates for the web interface
│ ├── static/ # Static files like CSS, JS, and images
│ ├── model_evaluation/ # Evaluation metrics and model processing logic
│ └── data_management/ # Database interaction components
│
├── instance/ # SQLite database files
│
├── tests/ # Test suite for the application
│
└── (configuration and system files)