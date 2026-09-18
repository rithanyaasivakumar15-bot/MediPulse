# MediPulse Intelligence

## Healthcare Supply Intelligence & Smart Inventory Management System

MediPulse Intelligence is a web-based healthcare supply intelligence platform designed to help hospitals and healthcare organizations monitor medical inventory, analyze historical demand, identify stockout and expiry risks, and support data-driven procurement decisions.

The system combines current inventory information with historical usage data to provide meaningful insights into supply conditions and help users make informed inventory and procurement decisions.

---

## 📌 Project Overview

Managing medical supplies efficiently is important for hospitals because both stock shortages and excessive inventory can affect healthcare operations.

MediPulse Intelligence addresses this problem by providing a centralized platform for:

- Monitoring current inventory levels
- Tracking historical usage and demand
- Identifying stockout risks
- Identifying expiry risks
- Generating procurement recommendations
- Updating inventory through CSV files
- Preserving historical usage data during inventory updates
- Visualizing important supply information through a dashboard

The system is designed to support healthcare inventory teams in understanding supply conditions and planning procurement more effectively.

---

## ✨ Key Features

### 📊 Dashboard

The dashboard provides an overview of the healthcare supply system, including:

- Total inventory items
- Stock status
- Risk information
- Demand-related insights
- Procurement information
- Inventory distribution

---

### 📦 Inventory Management

The inventory module allows users to:

- View medical supply items
- View current stock levels
- View item details
- Search and filter inventory
- Monitor expiry information
- View supplier information
- Delete inventory items

Each inventory item is identified using a unique `item_code`.

---

### 📈 Demand & Historical Usage Analysis

MediPulse Intelligence maintains historical usage information separately from current inventory data.

This allows the system to:

- Analyze previous consumption
- Identify demand patterns
- Continue analysis after inventory updates
- Preserve historical usage records
- Avoid treating a stock update as historical demand

---

### ⚠️ Risk Detection

The system analyzes inventory conditions to identify potential risks such as:

- Stockout risk
- Low-stock conditions
- Expiry risk
- Excess inventory
- Supply-related concerns

These insights help users understand which items may require attention.

---

### 🛒 Procurement Recommendations

Based on inventory conditions and demand-related information, the system provides procurement recommendations.

Examples include:

- Items requiring procurement
- Items that may require monitoring
- Items with sufficient stock
- Items affected by expiry conditions

The recommendations are intended to support procurement planning rather than replace human decision-making.

---

### 📄 CSV Data Upload

Inventory information can be uploaded using CSV files.

The system supports updating existing inventory using the item's unique `item_code`.

If an uploaded CSV contains an existing `item_code`:

- The existing inventory item is updated
- Current stock information is updated
- Current item details are updated
- Historical usage records are preserved
- A duplicate inventory item is not created

This allows inventory information to be updated while maintaining historical demand information.

---

### 🔐 Login & Logout

The application includes a login system for accessing the platform.

#### Default Login

**Email**

```text
admin@medipulse.com
