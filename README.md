# OceanIntel

**OceanIntel** is a Python-based surf forecasting tool that retrieves live ocean conditions — including swell, wind, wave height, and tide data — and displays them in a simple web interface. The app allows users to rate surf sessions and uses that feedback to learn and predict personalized surf conditions over time.

---

## Features

- Pulls live surf and tide data using the Stormglass.io API
- Simple Streamlit web interface for checking conditions
- Location picker with several Southern California surf spots
- Displays swell height, direction, wind speed, wave height, and upcoming tide changes
- Modular Python structure for easy extension
- Session logging system (in progress) to enable machine learning on user preferences
- Optional AI model that predicts future surf quality based on past ratings

---

## Current Surf Spots

- Huntington Beach
- Trestles (San Clemente)
- Cardiff Reef
- Blacks Beach (San Diego)
- Rincon (Santa Barbara)

More regions can be added by editing the `SPOTS` dictionary in `app/ui.py`.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/OceanIntel.git
cd OceanIntel
2. Set Up a Virtual Environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Add Your API Key
Create a file called config.py in the project root:

python
Copy
Edit
# config.py
STORMGLASS_API_KEY = "your-api-key-here"
You can get a free API key at https://stormglass.io.

Running the App
Once your environment is set up:

bash
Copy
Edit
streamlit run main.py
The app will launch in your browser at http://localhost:8501.

Project Structure
bash
Copy
Edit
OceanIntel/
├── app/                 # Streamlit UI
│   └── ui.py
├── api/                 # Stormglass API interface
│   └── stormglass.py
├── ai/                  # (In progress) ML model and training scripts
├── data/                # CSV logs and training data
├── utils/               # Shared helper functions
├── config.py            # API key config
├── main.py              # Launches the app
├── requirements.txt     # Python dependencies
└── README.md            # Project overview

