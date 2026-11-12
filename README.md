# MediWatch
MediWatch is a patient monitoring system designed to support the early detection of health deterioration in hospitalized patients. It monitors vital signs, identifies abnormal patterns, and provides alerts to healthcare professionals to support timely clinical assessment and patient care.

## Key Features

- Patient Monitoring: Provides an overview of hospitalized patients and their current health status.
- Vital Signs Tracking: Monitors heart rate, oxygen saturation (SpO₂), respiratory rate, body temperature, and blood pressure.
- Early Warning System: Identifies abnormal vital sign readings using predefined clinical thresholds and classifies patient risk levels.
- Clinical Alerts: Highlights patients requiring attention and allows healthcare professionals to acknowledge alerts.
- Data Visualization: Displays vital sign trends through interactive charts to support patient assessment.
- Historical Records: Maintains historical readings for reviewing changes in patient conditions.
- Real-Time Dashboard Simulation: Provides periodically refreshed patient monitoring data through an interactive dashboard.

## Dashboard Overview

### 1. Patient Overview

![Patient Overview](Screenshots/Patient%20Overview.jpeg)

### 2. Clinical Alerts
![Clinical Alerts](Screenshots/Clinical%20Alerts.jpeg)

### 3. Clinical Analytics
![Clinical Analytics](Screenshots/Clinical%20Analytics.jpeg)

![Clinical Analytics - Additional View](Screenshots/Clinical%20Analytics2.jpeg)
  
## Technology Stack
- Python: Core programming language.

- Streamlit: Interactive dashboard development.

- Pandas & NumPy: Data processing and analysis.

- Plotly: Interactive data visualization.

## Demo & Data
The current prototype uses simulated patient monitoring data to demonstrate vital sign tracking, risk classification, clinical alerts, and dashboard functionality.
The current version does not require a physical wearable device.

## Project Status
MediWatch is currently under development as a hackathon prototype, with potential for future integration with wearable medical devices and hospital monitoring systems.


## Installation & Usage

### 1. Download the Project
Download the ZIP file containing the demo source code and dataset.

### 2. Extract the ZIP File
Extract the downloaded ZIP file into your preferred directory.

### 3. Install Dependencies

```bash
pip install streamlit pandas numpy plotly streamlit-autorefresh streamlit-option-menu
```

### 4. Run the Application

Navigate to the extracted project folder and run:

```bash
streamlit run PeDemo.py
```

### 5. Access the Dashboard

Open the local URL displayed in the terminal (usually `http://localhost:8501`) to access the MediWatch dashboard.
