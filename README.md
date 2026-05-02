# Insight Dashboard

An interactive sales analytics dashboard built with **Streamlit**, **Pandas**, and **Plotly**. Designed for business intelligence use cases, the dashboard transforms raw transactional data into actionable insights through dynamic filtering and rich visualizations.

---

## Features

### Key Performance Indicators
- **Total Revenue** — aggregate revenue for the selected period, with growth delta vs. the prior half of the window
- **Total Units Sold** — volume of units moved across all transactions
- **Average Order Value** — mean revenue per transaction
- **Period Growth Rate** — percentage change between the first and second halves of the selected date range

### Interactive Filters (sidebar)
| Filter | Type | Description |
|---|---|---|
| Date Range | Date picker | Narrow analysis to any start/end window |
| Category | Multi-select | Filter by one or more product categories |
| Region | Multi-select | Filter by one or more geographic regions |

All charts and KPIs update instantly on every filter change.

### Charts
| Chart | Purpose |
|---|---|
| **Line chart** — Revenue Trend Over Time | Monthly revenue by category; reveals seasonality and growth trajectories |
| **Donut / Pie chart** — Revenue by Category | Share of wallet per category at a glance |
| **Grouped bar chart** — Category × Region | Side-by-side revenue comparison across regions per category |

### Monthly Summary Table
Sortable breakdown of Revenue, Order Count, Units Sold, and Average Order Value — one row per month in the selected window.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Dashboard framework | [Streamlit](https://streamlit.io/) |
| Data manipulation | [Pandas](https://pandas.pydata.org/) |
| Visualizations | [Plotly Express](https://plotly.com/python/plotly-express/) |
| Numerical computing | [NumPy](https://numpy.org/) |
| Language | Python 3.11 |

---

## Project Structure

```
insight-dashboard/
├── app.py                  # Main Streamlit application
├── .streamlit/
│   └── config.toml         # Server configuration (port, headless mode)
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10 or 3.11
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/LAzzawi/Insight-Dashboard.git
cd Insight-Dashboard

# Install dependencies
pip install streamlit pandas plotly numpy

# Run the dashboard
streamlit run app.py
```

The app will be available at `http://localhost:8501` by default.

### Custom Port

```bash
streamlit run app.py --server.port 5000
```

---

## Data

The dashboard ships with a built-in synthetic sales dataset of **1,000 transactions** spanning **2023–2024** across five product categories and four regions. The dataset is generated deterministically (seeded) so results are reproducible.

| Field | Description |
|---|---|
| `date` | Transaction date (2023-01-01 → 2024-12-31) |
| `category` | Electronics · Clothing · Food & Beverage · Home & Garden · Sports |
| `region` | North · South · East · West |
| `revenue` | Transaction revenue in USD |
| `units` | Number of units sold |

To plug in real data, replace the `load_data()` function in `app.py` with a CSV reader, database query, or API call. The rest of the dashboard adapts automatically.

---

## Configuration

Edit `.streamlit/config.toml` to change server behaviour:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

---

## Author

**Laith Al-Azzawi**  
Data Scientist & Software Engineer  
[github.com/LAzzawi](https://github.com/LAzzawi)
