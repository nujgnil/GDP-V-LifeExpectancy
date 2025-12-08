# GDP vs Life Expectancy — A Global Data Science Analysis

Understanding how economic development influences public health is a core question in global policy.  
This project investigates the relationship between **GDP per capita** and **Life Expectancy at birth** across countries using data from **Our World in Data (OWID)**.

The goal is to:
- Explore global patterns and disparities
- Quantify the GDP–health relationship
- Identify clusters of countries with similar socio-economic profiles

---

## Key Insights (Summary)

- Strong **positive relationship**: higher GDP per capita generally corresponds to longer life expectancy.
- **Diminishing returns**: improvements taper off once countries reach high-income levels.
- Clustering reveals **distinct groups** of countries experiencing:
  - rapid economic development
  - stagnant health outcomes
  - high-standard living but slow growth

---

## Methods & Techniques

| Stage | Tools/Methods |
|-------|--------------|
| Data Cleaning | Pandas: type conversions, column renaming, filtering invalid entries |
| Data Merging | Inner join on `Entity`, `Code`, `Year` |
| Exploratory Analysis | Correlation metrics, descriptive stats |
| Visualisation | Matplotlib / Seaborn |
| Unsupervised Learning | KMeans clustering (elbow method) |

---

## Project Structure

```bash
GDP-V-LifeExpectancy/
│
├── data/
│   ├── raw/                        # Original OWID data (not uploaded)
│   └── processed/                  # Cleaned combined dataset
│
├── notebooks/
│   └── GDP_vs_LE_Analysis.ipynb    # Full analysis workflow
│
├── images/                         # (To add plots here)
│
└── README.md
```
## Data Source

Data retrieved from:

Our World in Data (OWID)
https://ourworldindata.org/life-expectancy

https://ourworldindata.org/grapher/gdp-per-capita-worldbank
