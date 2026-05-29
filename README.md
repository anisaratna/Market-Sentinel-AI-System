# 🌐 Market Sentinel AI: End-to-End Automated Intelligence System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)](https://neon.tech/)
[![Docker](https://img.shields.io/badge/Container-Docker-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Overview
**Market Sentinel AI** is a production-grade data system designed to monitor and analyze global market sentiment across three strategic pillars: **Geopolitical Risks (Strait of Hormuz)**, **Technology Wars (AI Semiconductor)**, and **Macroeconomic Shifts (Global Inflation)**. This system automates the entire data lifecycle—from ingestion and AI-powered sentiment analysis to cloud storage, RESTful API delivery, and a Generative AI-integrated dashboard.

## System Architecture
The project implements a **Decoupled Microservices Architecture**, ensuring scalability and resilience:

1.  **Ingestion Layer (ETL):** An automated pipeline triggered every 6 hours via **GitHub Actions**. It extracts real-time news from the NewsAPI and performs sentiment inference using the **FinBERT** model.
2.  **Storage Layer:** High-performance **PostgreSQL (Neon.tech)** cloud database featuring a **Unique Constraint De-duplication Logic** to maintain data integrity across scheduled runs.
3.  **Intelligence Layer (GenAI):** Implements a **RAG-Lite (Retrieval-Augmented Generation)** workflow. It fetches historical context from PostgreSQL and utilizes **Llama 3.1 (via Groq API)** to generate executive briefings and answer user queries.
4.  **Delivery Layer (API):** A **FastAPI** backend containerized with **Docker**, providing standardized JSON access to processed market intelligence.
5.  **Presentation Layer:** A comprehensive **Streamlit Dashboard** featuring real-time metrics, time-series trend analysis, and interactive keyword clouds.

## Live Demos
*   **Interactive Dashboard:** https://huggingface.co/spaces/anisa04/market-sentinel-dashboard
*   **API Documentation (Swagger UI):** https://anisa04-intel-api.hf.space/docs#/default/get_history_history_get

## Tech Stack
*   **AI/ML:** Hugging Face Transformers (FinBERT), Llama 3.1 (Groq API).
*   **Data Engineering:** GitHub Actions (Cron Jobs), SQL (DML/DDL), Psycopg2.
*   **Backend:** FastAPI, Uvicorn, Pydantic, Docker.
*   **Frontend:** Streamlit, Plotly Express, WordCloud, Matplotlib.
*   **Cloud:** Neon.tech (PostgreSQL), Hugging Face Spaces.

## Dashboard Preview & Features
https://github.com/anisaratna/Market-Sentinel-AI-System/blob/main/preview.png?raw=true

### **Key Features:**
*   **Real-time Sentiment Tracking:** Visualize market "mood" swings with 4-hourly granularity.
*   **Hybrid Topic Modeling:** Combines statistical analysis (WordClouds/Bar Charts) with Generative AI (Llama 3.1) for deep contextual understanding.
*   **AI Intel-Chat:** An interactive Q&A feature allowing users to ask complex questions based on the latest 30 news records.
*   **Dynamic Filtering:** Instant analytics switching between geopolitical and technological data feeds.

## Repository Structure
*   `etl_ingestor/`: Python scripts for data crawling, AI sentiment tagging, and database loading.
*   `.github/workflows/`: YAML configuration for automated scheduled execution.
*   `api_service/`: FastAPI source code and Dockerfile for API deployment.
*   `dashboard_app/`: Streamlit source code for the visual interface.
*   `requirements.txt`: Environment dependencies.

## Engineering Highlights
*   **Resilience:** The system separates the "Worker" from the "Server," meaning the API/Dashboard remains live even if the data source (NewsAPI) is temporarily unavailable.
*   **Optimized Inference:** Uses `st.cache_data` and efficient SQL queries to minimize database overhead and maximize UI responsiveness.
*   **Security:** API Keys and Database Credentials are fully managed via **GitHub Secrets** and **Hugging Face Secrets**, following industry-standard security practices.

Developed by **Annisa Ratna Salsabilla** | [LinkedIn](https://linkedin.com/in/annisartna)
