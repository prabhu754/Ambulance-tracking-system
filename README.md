# Ambulance Tracking System

## Project Overview
This project is designed to provide efficient ambulance tracking and management services. It allows for real-time tracking of ambulances, ensuring that emergency services can respond quickly to incidents.

## Architecture
The system follows a microservices architecture that consists of several components communicating over network protocols. Key components include:
1. **Frontend:** A user-friendly interface for users to request ambulance services.
2. **Backend:** Handles requests, processes data, and interacts with the database.
3. **Database:** Stores user data, ambulance details, and tracking information.

## Features
- Real-time tracking of ambulances
- User registration and authentication
- Request for ambulance services
- Notifications for users about ambulance arrival
- Admin dashboard for managing ambulances and tracking incidents

## Technology Stack
- **Frontend:** React.js
- **Backend:** Node.js & Express.js
- **Database:** MongoDB
- **Geolocation API:** Google Maps API for tracking locations

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/prabhu754/Ambulance-tracking-system.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Ambulance-tracking-system
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Set up the environment variables as needed.
5. Start the development server:
   ```bash
   npm start
   ```

## System Design
The system is designed with scalability in mind, utilizing microservices for easy maintenance and updates. Each component can be scaled independently according to the load.

## Screenshots
![Ambulance Tracking System](./screenshots/screenshot1.png)
![Ambulance Dashboard](./screenshots/screenshot2.png)

---