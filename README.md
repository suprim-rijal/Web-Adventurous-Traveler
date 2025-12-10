# 🛫 Adventurous Traveler

> An immersive web-based adventure game where players explore Europe, hunt for ancient artifacts, and manage resources strategically across 20 thrilling flights.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 About

**Adventurous Traveler** is a strategic exploration game that combines geography, resource management, and puzzle-solving. Players embark on a quest to discover 10 hidden artifacts scattered across European airports, then deliver them to their designated destinations—all while managing limited fuel, money, and flight allowances.

### 🎮 Game Concept

- **Two-Phase Gameplay**: First find the hidden artifact airport, then deliver all artifacts to their destinations
- **Resource Management**: Balance fuel consumption, money spending, and limited travels (20 flights max)
- **Dynamic Clue System**: Discover hints about artifact locations through exploration
- **Interactive Map**: Navigate across real European airports using Leaflet.js
- **Shop & Upgrades**: Purchase fuel, travel passes, clue reveals, and power-ups
- **Random Events**: Encounter unexpected events that help or hinder your journey
- **Strategic Planning**: Every decision counts toward victory or defeat

## ✨ Key Features

### 🗺️ Interactive European Map
- Real airport locations with accurate coordinates
- Color-coded markers (current location, visited, revealed destinations)
- Clickable airports with detailed information popups
- Smooth navigation and zoom controls

### 🏺 Artifact Collection System
- 10 unique artifacts to find and deliver
- Two-phase gameplay: Finding → Delivering
- Each artifact has specific delivery airports
- Rewards for successful deliveries (money + fuel)

### 🛒 In-Game Shop
- **Fuel Items**: Refuel your plane
- **Travel Passes**: Free flights without fuel cost
- **Upgrades**: Permanent bonuses (better clues, higher reveal chances)
- **Services**: One-time boosts (reveal locations, instant clues)
- **Lootboxes**: Random rewards for the adventurous

### 🎲 Dynamic Events & Clues
- 70% chance of random events after each flight
- 40% base chance to discover clues
- Multiple clue types: directional, distance-based, regional, exact locations
- Events can provide resources or create challenges

### 📊 Resource Management
- **Fuel System**: Distance-based fuel consumption with efficiency bonuses
- **Money Economy**: Earn through deliveries, spend on upgrades
- **Travel Limit**: Strategic planning required with only 20 flights
- **Win/Lose Conditions**: Multiple paths to victory or defeat

## 🚀 Getting Started

### Prerequisites

```bash
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/adventurous-traveler.git
cd adventurous-traveler
```

2. **Install dependencies**
```bash
pip install flask flask-cors mysql-connector-python
```

3. **Set up the database**
```bash
mysql -u root -p
CREATE DATABASE adventurous_traveler_game;
USE adventurous_traveler_game;
SOURCE database/schema.sql;
SOURCE database/seed_data.sql;
```

4. **Configure database connection**
Edit `app.py` and update the database credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'adventurous_traveler_game',
    'autocommit': False
}
```

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
```
http://localhost:5000
```

## 🎯 How to Play

### Starting Your Journey
1. Enter your adventurer name
2. Read the story introduction
3. Begin at a random European airport

### Phase 1: Finding Artifacts
- Travel between airports to discover clues
- Clues will guide you to the hidden artifact airport
- Use the shop to buy clue reveals if you're stuck
- Once found, dig at the artifact airport to collect all 10 artifacts

### Phase 2: Delivering Artifacts
- Each artifact must be delivered to a specific airport
- Travel to delivery locations (marked with clues or shop reveals)
- Deliver artifacts to earn money and fuel rewards
- Complete all 10 deliveries to win!

### Strategy Tips
- 💰 **Manage Resources**: Don't run out of fuel or travels
- 🎫 **Use Fuel Passes**: Buy passes for free long-distance flights
- 🔍 **Collect Clues**: More clues = easier to find destinations
- 🛒 **Shop Wisely**: Invest in upgrades that match your playstyle
- 📍 **Plan Routes**: Minimize fuel consumption by planning efficient paths

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework for REST API
- **MySQL**: Relational database for game state and data
- **Python Libraries**: 
  - `mysql-connector-python`: Database connectivity
  - `flask-cors`: Cross-origin resource sharing
  - `math`: Distance calculations (Haversine formula)

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with transitions and animations
- **JavaScript (ES6)**: Game logic and interactivity
- **Leaflet.js**: Interactive map visualization
- **Font Awesome**: Icon library

### Architecture
- **RESTful API Design**: Clean endpoint structure
- **MVC Pattern**: Separation of concerns
- **Session Management**: Secure player state handling
- **Responsive Design**: Works on desktop and mobile devices

## 📂 Project Structure

```
adventurous-traveler/
│
├── app.py                      # Main Flask application & API endpoints
├── templates/                  # HTML templates
│   ├── index.html             # Home page
│   ├── welcome.html           # Player name & story intro
│   ├── game.html              # Main game interface
│   └── about.html             # About/Team page
│
├── static/
│   ├── css/
│   │   ├── style.css          # Global styles
│   │   ├── game.css           # Game interface styles
│   │   └── pages/             # Page-specific styles
│   │       ├── main.css
│   │       ├── welcome.css
│   │       └── about.css
│   │
│   └── js/
│       ├── game.js            # Main game logic
│       ├── welcome.js         # Intro & name entry
│       └── navigation.js      # Navigation transitions
│
├─Web-AdventurousTraveler.sql  #Database
│
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── LICENSE                    # MIT License

```

## 🎮 Game Systems Explained

### Distance Calculation
Uses the **Haversine formula** to calculate real-world distances between airports based on latitude/longitude coordinates:
```python
distance = 2 * R * arcsin(√(sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)))
```

### Fuel System
- Base fuel consumption = distance in kilometers
- Modified by fuel efficiency bonuses from upgrades
- Fuel passes allow free travel regardless of distance
- Maximum fuel capacity: 5000km

### Clue Generation
Clues adapt based on quality:
- **Low**: Approximate direction and rough distance
- **Medium**: Specific region and accurate distance
- **High**: Country and detailed hints
- **Exact**: Reveals precise airport location (purple marker)

### Random Events
- 70% trigger chance after each flight
- Types: Positive (bonuses) or Negative (setbacks)
- Effects: Money changes, fuel adjustments, extra travels
- Adds unpredictability and replayability

## 👥 Team

- **Suprim Rijal** - Project Handler (UI/UX, Database Design, Backend Development, Game Logic)
- **Dinuka Helkewela Mudiyanselage** - Assistance Handler (Game Logic, Backend Systems)
- **Nivin K M Handunsooriya Mudiyanselage** - Assistance Handler (Backend Logic, Database Connection)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- Map may load slowly on first visit (caching resolves this)
- Some clues may overlap if multiple artifacts share similar locations
- Modal scrolling on mobile devices could be improved

## 🔮 Future Enhancements

- [ ] Multiplayer mode with leaderboards
- [ ] More European airports (currently ~50)
- [ ] Achievement system
- [ ] Daily challenges
- [ ] Sound effects and background music
- [ ] Save game functionality
- [ ] Difficulty levels (Easy/Normal/Hard)
- [ ] Mobile app version

## 🙏 Acknowledgments

- OpenStreetMap for map tiles
- Leaflet.js for map functionality
- Font Awesome for icons
- Flask community for excellent documentation
- All contributors and testers

---

**Made with ❤️ for adventure lovers and geography enthusiasts**

⭐ Star this repo if you enjoyed the game!
