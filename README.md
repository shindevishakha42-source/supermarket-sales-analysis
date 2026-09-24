# Supermarket Sales Analysis

An internship-ready data analytics project that calculates sales from quantity and unit price, summarizes product and branch performance, compares customer/payment patterns, and presents the results in an interactive Streamlit dashboard.

> **Dataset note:** `data/supermarket_sales.csv` is generated demo data (500 example transactions), not the assignment's source dataset. Replace it with the provided dataset before submitting business findings. The screenshot's example answers are not hard-coded or claimed as results.

## Questions explored

- Which product category and branch generate the most sales?
- Which payment method appears most often?
- How do Member and Normal customers compare in average transaction value?
- What is the average customer rating?
- How do sales vary across branches and product categories?

## Quick start

Requires Python 3.10 or later.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

To print a reproducible summary in the terminal:

```bash
python analysis.py
```

## Use the assignment dataset

The dashboard accepts a CSV upload in its sidebar. The bundled [500-row generated demo dataset](https://raw.githubusercontent.com/shindevishakha42-source/supermarket-sales-analysis/main/data/supermarket_sales.csv) is for demonstrating the workflow only; it is not the assignment source dataset. Replace `data/supermarket_sales.csv` with your real CSV before reporting findings. The expected headers are:

`Product, Branch, City, Customer type, Quantity, Unit price, Payment, Rating`

If your source uses different header names, rename them or update the `REQUIRED` set and corresponding field references in `app.py` and `analysis.py`.

## Method

- **Sales per transaction** = `Quantity × Unit price` (as defined in the assignment brief).
- Missing/unparseable quantity and price rows are excluded from sales totals.
- Rankings use summed transaction sales; payment popularity uses transaction count.
- Rating is averaged over available numeric ratings. Verify the source's rating scale before interpreting the result.
- The simplified sales measure excludes tax, discounts, and other adjustments unless already included in the source unit price.

## Project structure

```text
├── app.py                         # Interactive Streamlit dashboard
├── analysis.py                    # Reproducible terminal summary
├── data/supermarket_sales.csv     # 500-row generated demo dataset
└── requirements.txt
```

## Business decision framework

After loading the real dataset, use the charts to identify best-selling products and branches. Consider adjusting replenishment to demand, investigate differences between branches, keep convenient payment methods available, and use customer ratings to target service improvements. Treat these as hypotheses to discuss with the business; sales summaries alone do not establish why performance differs.

## Limitations

This is descriptive analysis. It does not establish causation, account for operating costs, or measure profit. Results depend on the completeness and definitions in the source data.


