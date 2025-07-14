🏏 IPL Fantasy Score Predictor – MLOps Pipeline
  Welcome to the IPL Fantasy Score Predictor, an MLOps-based project designed to forecast IPL player performance using a robust and automated machine learning pipeline. The project leverages both structured statistical data and unstructured pitch commentary to deliver high-confidence fantasy team predictions.

📌 Table of Contents
  🔍 Project Overview
  
  📦 Features
  
  🧱 Architecture
  
  📊 Data Collection & Preprocessing
  
  📈 Models Used
  
  ⚙️ Usage Guide
  
  🧠 Team Insights

🔍 Project Overview
  This project predicts fantasy points for IPL matches using historical player statistics, match dynamics, and pitch conditions. It combines the strengths of ensemble learning, NLP, and Monte Carlo simulations to create a reliable match-day forecasting engine. The project is designed with MLOps best practices for automation, reproducibility, and scalability.

📦 Features
  🏏 Predicts individual player performance & total fantasy score
  
  ⚙️ Fully automated ML pipeline with one command execution
  
  🤖 Quantile Regression + Monte Carlo Simulation for uncertainty modeling
  
  🗣️ NLP classification of pitch commentary using DistilBERT
  
  📦 Delivered in a Docker container for easy deployment
  
  🔄 Reproducible outputs, no need to retrain on every match

🧱 Architecture
          ┌────────────┐
          │ Match Info │
          └─────┬──────┘
                ↓
       ┌────────────────┐
       │  Data Pipeline │◄─────────────┐
       └─────┬──────────┘              │
             ↓                         │
      ┌────────────┐        ┌──────────────────┐
      │ Toss & 11s │        │ Pitch Report NLP │
      └─────┬──────┘        └──────────────────┘
            ↓                         ↓
       ┌────────────┐        ┌────────────────────┐
       │  Feature    │        │ DistilBERT Classifier│
       │ Engineering │        └────────────────────┘
       └─────┬──────┘
             ↓
       ┌───────────────┐
       │ Quantile Model│
       └─────┬─────────┘
             ↓
  ┌──────────────────────┐
  │ Monte Carlo Simulator│
  └────────┬─────────────┘
           ↓
   ┌────────────────────────┐
   │ Fantasy Team Prediction│
   └────────────────────────┘
📊 Data Collection & Preprocessing
  Sources:
  Player stats: ESPNcricinfo's Statsguru, Cricbuzz
  
  Ground info: Manually compiled
  
  Match history: Unique match records across careers
  
  Pitch reports: Scraped from Sportskeeda and other sources
  
  Preprocessing Highlights:
  Normalized team name variations (e.g., Delhi Daredevils → Delhi Capitals)
  
  Deduplicated match records to avoid overlapping stats
  
  Separated batting and bowling stats for clarity
  
  Added rolling statistics for form (last 5 matches)

📈 Models Used
  🎯 Final Model:
  Quantile Regression + Monte Carlo Simulation
  
  Models uncertainty with predicted means and standard deviations
  
  Assumes normal distribution for simplicity and interpretability
  
  🧠 NLP Classifier:
  DistilBERT fine-tuned to classify pitch reports into:
  
  Batting-friendly
  
  Bowling-friendly
  
  🧪 Other Models Explored:
  XGBoost Classifier & Regressor with engineered features
  
  KDE-based probabilistic models (discarded due to poor fit)

⚙️ Usage Guide
  Input: Match number, playing 22 (including impact subs)
  Output: Predicted fantasy points and recommended team
  
  Fetch the upcoming match schedule
  
  Input match number via Docker CLI
  
  Automatically fetch toss and team info
  
  Run data preprocessing and feature generation
  
  Model predicts performance → Monte Carlo simulates outcome
  
  Suggests optimal fantasy team (>850 points expected)

🧠 Team Insights
  This project reflects a blend of domain knowledge, model experimentation, and engineering practicality. The use of NLP to quantify pitch commentary and the adoption of quantile-based uncertainty models make this a comprehensive MLOps case study in sports analytics.
