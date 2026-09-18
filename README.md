# 🏥 MediPulse — Healthcare Inventory Intelligence

**MediPulse** is a healthcare inventory intelligence and decision-support platform that helps hospitals monitor medical supplies, identify inventory risks, estimate demand from historical usage, and plan procurement more effectively.

The system transforms inventory and consumption data into actionable insights through an interactive dashboard.

---

## 🚀 Features

### 📦 Inventory Management

* Track medical inventory and stock levels
* Monitor reorder levels and maximum stock levels
* Manage expiry dates, suppliers, categories, and unit costs
* Add, update, and delete inventory items

### 📊 Demand & Usage Analysis

* Analyze historical consumption patterns
* Estimate daily demand using recent usage trends
* Calculate days of available stock

### ⚠️ Risk Detection

MediPulse identifies several inventory risks:

* **Stockout Risk** — items that may run out soon
* **Expiry Risk** — items approaching expiration
* **Abnormal Usage** — unusual consumption patterns
* **Emergency Reserve Risk** — insufficient reserve stock
* **Overall Risk** — consolidated inventory risk status

### 🛒 Procurement Recommendations

* Identify items requiring replenishment
* Calculate recommended procurement quantities
* Support inventory planning using demand and stock information

### 📁 CSV Data Upload

* Upload inventory data through CSV files
* Add new inventory records
* Update existing inventory information
* Preserve historical usage data when inventory records are updated

### 📈 Interactive Dashboard

The dashboard provides a centralized view of:

* Inventory status
* Risk levels
* Stock availability
* Demand trends
* Procurement requirements

---

## 🧠 How It Works

```text
Inventory Data
      │
      ▼
Historical Usage
      │
      ▼
Demand Estimation
      │
      ▼
Inventory Analysis
      │
      ├── Stockout Risk
      ├── Expiry Risk
      ├── Abnormal Usage
      └── Reserve Risk
      │
      ▼
Risk Assessment
      │
      ▼
Procurement Recommendation
```

MediPulse uses historical consumption data and current inventory levels to estimate demand and identify potential supply risks.

> **Note:** The current forecasting implementation uses a weighted historical-usage approach. It is a statistical/heuristic demand estimation method rather than a trained machine-learning model.

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* React Router
* Recharts
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite

### Data

* Historical usage records
* Inventory data
* CSV import

---

## 🏗️ Architecture

```text
┌─────────────────────────────┐
│       React Frontend        │
│                             │
│ Dashboard • Inventory       │
│ Risk Monitor • Procurement  │
└──────────────┬──────────────┘
               │
             REST API
               │
┌──────────────▼──────────────┐
│       FastAPI Backend       │
│                             │
│ Inventory Management        │
│ Demand Estimation           │
│ Risk Analysis               │
│ Procurement Logic           │
│ CSV Processing               │
└──────────────┬──────────────┘
               │
           SQLAlchemy
               │
┌──────────────▼──────────────┐
│          SQLite             │
│                             │
│ Inventory + Usage History   │
└─────────────────────────────┘
```

---

## 📂 Project Structure

```text
MediPulse/
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rithanyaasivakumar15-bot/MediPulse.git
cd MediPulse
```

### 2. Start the Backend

```bash
cd backend
```

Create a virtual environment:

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

### 3. Start the Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🔐 Authentication

The current version includes a **demo login flow** for the prototype.

Production deployment would require secure authentication and authorization, including proper password handling, token validation, role-based access control, and session management.

---

## 📊 Demo Data

MediPulse includes sample inventory and historical usage data for development and demonstration.

The sample data allows the application to be run without connecting to an external hospital inventory system.

> Sample data is for demonstration purposes and does not represent real hospital or patient data.

---

## 🔮 Future Enhancements

* Advanced machine-learning demand forecasting
* Multi-hospital and multi-department inventory management
* Role-based access control
* Real-time inventory integration
* Automated low-stock and expiry alerts
* Supplier performance analytics
* Inventory cost optimization
* Barcode/QR-based inventory tracking
* Advanced reporting and analytics

---

## 🎯 Project Objective

MediPulse aims to demonstrate how healthcare inventory and historical consumption data can be converted into useful operational insights.

The project focuses on:

* Improving inventory visibility
* Detecting supply risks early
* Estimating future demand
* Supporting procurement decisions
* Reducing manual inventory analysis

---

## ⚠️ Disclaimer

MediPulse is a **prototype and decision-support application** developed for educational, demonstration, and development purposes.

It is not a medical device and should not be used as the sole basis for clinical, procurement, or patient-care decisions without appropriate human review and validation.

---

## 👩‍💻 Author

**Rithanyaa Sivakumar**

GitHub:
https://github.com/rithanyaasivakumar15-bot

---

## 📜 License

This project does not currently specify a license.

If you plan to distribute the project as open source, consider adding an appropriate license such as the MIT License.
