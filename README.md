# 🌍 EcoScan - Clothing Carbon Footprint Scanner

## 📜 Overview
EcoScan is a full-stack web application designed to help users understand the environmental impact of their clothing choices. By leveraging advanced AI and intuitive design, users can upload images of clothing items, view estimated carbon scores, earn eco-reward points, and redeem sustainability-focused offers.

This project utilizes:
- **Frontend**: React.js
- **Backend**: FastAPI
- **Image Recognition**: GPT-4 Vision API for clothing detection and analysis.

---

## 🔧 Tech Stack
- **Frontend**: React.js (hosted on Vercel)
- **Backend**: FastAPI (hosted on Render)
- **Image Recognition**: GPT-4 Vision API
- **Testing**: Pytest for backend testing

---

## 🚀 Project URLs
- **Frontend URL**: [EcoScan Client](https://eco-scan-challenge-ten.vercel.app/)
- **Backend API (with Docs)**: [EcoScan Backend API Docs](https://eco-scan-challenge.onrender.com/docs)
- **Video Demo**: [EcoScan Challenge Demo](https://youtu.be/R8LphAtXGgU)

---

## 🚀 Setup Instructions

### Prerequisites
- Node.js (for frontend)
- Python 3.8+ (for backend)
- Git

### Clone the Repository
```bash
git clone https://github.com/vivek-c-shah/eco-scan-challenge.git
cd eco-scan-challenge
```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd eco-scan-client
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
4. Access the application at [http://localhost:3000](http://localhost:3000).

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd eco-scan-backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
5. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🛠 Features

### Frontend
- **Image Upload**: Upload images from files or capture using a camera.
- **Carbon Score Display**: View identified clothing items with their carbon scores.
- **Eco-Reward Points**: See the total eco-reward points earned.
- **Offers Display**: Redeem offers based on eco-reward points.

### Backend
- **Image Analysis API**: Uses GPT-4 Vision API to identify clothing items and their carbon scores.
- **Eco-Reward Calculation**: Calculates eco-reward points based on carbon scores.
- **Offers API**: Fetches redeemable offers based on user points.

---

## 🌍 Carbon Score Assumptions

To estimate the environmental impact, the following carbon scores (in grams of CO₂) are assigned to clothing items:

| Clothing Item | Carbon Score (g CO₂) |
|---------------|-----------------------|
| T-shirt       | 5000                 |
| Jeans         | 10000                |
| Jacket        | 15000                |
| Shoes         | 8000                 |
| Dress         | 12000                |
| Sweater       | 7000                 |
| Shirt         | 6000                 |
| Shorts        | 4000                 |
| Skirt         | 5000                 |
| Coat          | 20000                |

These values are stored in the backend (`carbon_scores.py`) for quick access.

---

## 🎁 Redeemable Offers

Users can redeem the following offers based on their eco-reward points:

| Points Required | Offer                            |
|------------------|----------------------------------|
| 15               | 10% off next purchase           |
| 30               | Free eco-friendly keychain      |
| 50               | 5% off on eco-friendly products |
| 70               | Free digital guide to sustainability |
| 100              | Free eco-friendly tote bag      |
| 150              | Plant a tree in your name       |
| 200              | 20% off sustainable clothing    |

These offers are managed in the backend (`offers.py`).

---

## 🧪 Testing

### Backend Testing
To run unit tests for the backend:
```bash
pytest
```

Tests cover:
- API endpoints for image analysis
- Eco-score calculations
- Offer retrieval logic

---

## 🌟 Product & Technical Enhancements

### Proposed Enhancements

1. **Scaling Backend**:
   - Introduce a caching mechanism (e.g., Redis) to handle frequently accessed data.
   - Use a database (e.g., PostgreSQL) for storing user data and transaction history.
   - Deploy using serverless platforms for auto-scaling.

2. **Improved Carbon Scoring**:
   - Incorporate detailed material data and production practices.
   - Integrate external APIs for real-time carbon footprint data.

3. **Enhanced User Experience**:
   - Add sustainability tips based on detected items.
   - Provide visual comparisons (e.g., CO₂ saved vs. industry average).

4. **Advanced Integrations**:
   - Partner with brands to fetch real-world carbon data.
   - Add social sharing features for eco-savings achievements.

---

## 📲 Deployment

The project is deployed on:
- **Frontend**: Vercel ([EcoScan Client](https://eco-scan-challenge-ten.vercel.app/))
- **Backend**: Render ([EcoScan API](https://eco-scan-challenge.onrender.com/docs))

---

### Thank you for exploring EcoScan! Together, we can make sustainable fashion choices and reduce our carbon footprint. 🌱