# Weather Application - Module 6 Lab

## Student Information
- **Name**: John Paul Caldo
- **Student ID**: 231002310
- **Course**: CCCS 106
- **Section**: 3B

## Project Overview
So I created a clean and modern Weather App using Flet, and I added a 5-day forecast feature to make it more helpful. The app lets users search any city, shows real-time weather data, and even allows them to check the weather automatically using their location.

## Features Implemented
These are the core features of the app:

City search functionality

Current weather display

Temperature, humidity, wind speed

Weather icons from OpenWeatherMap

Error handling for wrong inputs

Clean and modern UI with Material Design
### Base Features
- [x] City search functionality
- [x] Current weather display
- [x] Temperature, humidity, wind speed
- [x] Weather icons
- [x] Error handling
- [x] Modern UI with Material Design

### Enhanced Features
1. Dynamic Theme Switcher (Light, Dark, and Pink Mode!)

What it does:
This feature lets the user switch between themes by clicking the icon beside the title. The whole UI changes colors—including the cards, borders, texts, and even the icons.

Why I chose it:
I wanted the app to feel more personal and fun. Sometimes users prefer dark mode, and others want something brighter. So I added a cute pink theme too.

Challenges I faced:
The hardest part was making every component update its colors instantly, even inside containers and forecast cards. I solved it by creating a function that updates the UI colors and calling it whenever the theme changes.

2. 5-Day Weather Forecast

What it does:
The app doesn’t just show today’s weather—it also analyzes OpenWeatherMap’s 3-hour data and groups it into five separate days. Each day shows the icon, weather description, and high/low temperatures.

Why I chose it:
I wanted the app to be more than “just another weather app.” Planning for the next few days makes it more useful, especially for travel or daily routines.

Challenges I faced:
OpenWeatherMap gives weather data every 3 hours, not daily. So I had to group all timestamps by date, compute min/max temp, and find the most common icon & description. After that, I created forecast cards and updated their colors based on the theme.

## Screenshots
PINKKKK
![alt text](<Screenshot (73).png>)
5 DAY WEATHER FORECAST
![alt text](<Screenshot (74).png>)
HISTORY SUGGESTION
![alt text](<Screenshot (75).png>)
## Installation
Python 3.8 or higher
flet app
dotvenv
pip package manager
### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/<username>/cccs106-projects.git
cd cccs106-projects/mod6_labs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your OpenWeatherMap API key to .env

