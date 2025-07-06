# 🏠 Rent Fairness Analyzer

A Streamlit-based web app that helps renters estimate whether a property's rent is fair based on its location, area, BHK, and amenities.

---

## 🔍 Key Features

- 🧠 **ML Model**: Trained Random Forest to predict fair rent
- 🌐 **URL Scraping**: Auto-fill fields from MagicBricks or 99acres listings (stubbed)
- 📌 **Manual Entry**: Option to input rent listing details manually
- 🗺️ **Interactive Map**: Folium-based rent map with location pins
- ⚖️ **Fairness Verdict**: Know if rent is overpriced or fair

---

## 🚀 Try it Live 

👉 [https://Swayamchopda-rent-fairness-analyzer.streamlit.app](https://rent-fairness-analyzer-hkfiivcpkvefzpvccgmikw.streamlit.app/)

---

## 🛠️ How to Run Locally

```bash
git clone https://github.com/Swayamchopda/rent-fairness-analyzer.git
cd rent-fairness-analyzer
pip install -r requirements.txt
streamlit run app.py
