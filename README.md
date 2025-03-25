# Web Analytics Lite

A lightweight Flask-based web analytics system for tracking visitor behavior and engagement metrics.

## Features

- Real-time session tracking
- Location detection (IP-based)
- Visit duration monitoring
- Device and browser detection
- Screen resolution tracking
- Referrer tracking
- Privacy-focused data collection
- GDPR-compliant location tracking

## Tech Stack

- Python 3.x
- Flask
- SQLAlchemy
- SQLite
- JavaScript (Frontend)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask server:
```bash
python app.py
```

3. Access the application:
- Demo page: http://127.0.0.1:5000
- Analytics dashboard: http://127.0.0.1:5000/dashboard

## Data Collection

The system collects:
- Session duration
- Page visits
- Browser information
- Operating system
- Device type
- Screen resolution
- Geographic location (city/country)
- Referrer URLs

## Database Schema

- ID (Primary Key)
- Session Hash
- Timestamp
- Exit Time
- Device Type
- Browser
- OS
- Country
- City
- URL Path
- Referrer
- Screen Resolution
- Session Duration

## Privacy Features

- IP address anonymization
- GDPR-compliant location tracking
- No personal data collection
- Session-based tracking instead of user tracking

## License

Private repository - All rights reserved

## Author

[dias-2008](https://github.com/dias-2008)
