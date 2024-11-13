 
# Financial Metrics Calculator

This project implements a financial analysis tool for calculating key metrics such as default probability, credit spreads, and recovery rates based on the Merton model. It provides functionality to analyze financial data for companies and portfolios, with interactive UI support via a Streamlit app.

---

## Features
- **Default Probability**: Measures the likelihood of a company defaulting on its debt.
- **Credit Spread**: Calculates the spread of corporate bonds over risk-free bonds.
- **Recovery Rate**: Estimates the proportion of debt recovered in case of default.
- Portfolio-level impact analysis using stressed scenarios.
- Interactive input and real-time calculations with a Streamlit interface.

---

## Directory Structure
```
/project
├── app.py                    # Streamlit app for interactive analysis
├── Main.py                   # Main script for portfolio analysis
├── Merton.py                 # Core Merton model implementation
├── Port_Exposure.py          # Portfolio impact calculations
├── Delta_Fin.py              # Delta calculation for financial companies
├── Delta_NonFin.py           # Delta calculation for non-financial companies
├── requirements.txt          # Required Python dependencies
├── Data.xlsx                 # Sample input data (if applicable)
└── README.txt                # Project documentation
```

---

## How to Use

### 1. Requirements
Install the following dependencies:
- Python 3.8 or higher
- Required Python libraries: `streamlit`, `pandas`, `numpy`, `scipy`, `xlwings`, `openpyxl`

Install dependencies using:
```
pip install -r requirements.txt
```

---

### 2. Running the Streamlit App
1. Run the app with the following command:
   ```
   streamlit run app.py
   ```

2. Open the URL provided by Streamlit (e.g., `http://localhost:8501`) in your browser.

3. Input financial data such as:
   - Risk-Free Rate
   - Time to Default
   - Market Cap
   - Total Debt
   - Company Volatility

4. View calculated metrics:
   - Default Probability
   - Credit Spread
   - Recovery Rate

---

### 3. Using the Portfolio Analysis Script
The `Main.py` script reads portfolio data from an Excel file (`Data.xlsx`) and performs detailed portfolio impact analysis, including stress testing for credit spreads and portfolio repricing. To run it:

1. Place your dataset in `Data.xlsx`.
2. Run the script:
   ```
   python Main.py
   ```
3. The output will be saved in a formatted Excel file.

---

## Key Components

### Merton Model (`Merton.py`)
- Implements the Merton model for credit risk analysis.
- Functions:
  - `default_proba`: Computes default probability.
  - `credit_spread`: Calculates credit spread.
  - `recovery_rate`: Estimates recovery rate.

### Portfolio Impact (`Port_Exposure.py`)
- Calculates portfolio-level impact under stressed scenarios.
- Uses delta multipliers for both financial and non-financial companies.

### Delta Calculations (`Delta_Fin.py` and `Delta_NonFin.py`)
- **`Delta_Fin.py`**: Handles delta calculations for financial companies.
- **`Delta_NonFin.py`**: Handles delta calculations for non-financial companies.

---

## Dependencies
The required dependencies are listed in `requirements.txt`. Install them using:
```
pip install -r requirements.txt
```

Key libraries include:
- `streamlit`: For interactive UI.
- `pandas`: For data manipulation.
- `numpy`: For numerical operations.
- `scipy`: For statistical computations.
- `xlwings` and `openpyxl`: For Excel file handling.

---

## Notes
- Ensure the dataset (`Data.xlsx`) is correctly formatted for portfolio analysis.
- Adjust parameters in `app.py` and `Main.py` as needed for your specific use case.

---

## Contact
For questions or feedback, please reach out to the project maintainer.

---

## License
This project is open-source and available under the MIT License.
