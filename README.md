# PropAI – Smart Real Estate Intelligence Platform

Real estate platforms often lack reliable price estimation and fraud detection mechanisms. PropAI addresses these challenges by integrating predictive analytics and verification systems into a single platform.

PropAI is an AI-powered real estate platform designed to enhance property search and decision-making through data-driven insights, fraud detection, and intelligent automation. The system is built with a modular architecture integrating data processing, machine learning models, and real-time user interaction through a web-based interface.

## Key Features

* 🔍 **Property Search & Filtering**
  Allows users to browse and filter property listings based on location and preferences.

* 💰 **Price Prediction**
  Utilizes a machine learning regression model to estimate property prices based on features such as location, BHK, area, and amenities.

* ⚠️ **Fraud Detection**
  Implements rule-based anomaly detection to identify suspicious or inconsistent property listings.

* 🖼️ **Image Verification**
  Detects potentially edited or AI-generated property images using:

  * EXIF metadata analysis
  * Error Level Analysis (ELA)

* 🧠 **Image Classification**
  Uses a Convolutional Neural Network (CNN) to classify property types such as apartments, villas, offices, and plots.

* 🗺️ **Map Visualization**
  Displays property locations using interactive maps powered by Folium.

* 🤖 **Chatbot Assistance**
  Provides basic user support using a rule-based chatbot system.

## Tech Stack

* Python
* Streamlit (Frontend & App Interface)
* Scikit-learn (Machine Learning)
* PyTorch (CNN Model)
* Pandas & NumPy (Data Processing)
* PIL (Image Processing)
* Folium (Map Visualization)

## Key Concepts Used

* Machine Learning Regression
* Convolutional Neural Networks (CNN)
* Basic Image Analysis (EXIF metadata, Error Level Analysis)
* Rule-based Anomaly Detection
* Modular Application Design

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Run the application:
   streamlit run app.py



