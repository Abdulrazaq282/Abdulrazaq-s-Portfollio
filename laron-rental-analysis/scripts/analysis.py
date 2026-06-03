"""
Laron Rental Business Analysis
Author: Abdulrazaq SHOLA
Description: End-to-end analysis of a DVD rental business using the Sakila database.
             Covers revenue trends, customer behaviour, film performance, and store comparisons.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import os

# ── Style ──────────────────────────────────────────────────────────────────────
sns.set_theme(style="darkgrid", palette="deep")
plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor":   "#161b22",
    "axes.edgecolor":   "#30363d",
    "axes.labelcolor":  "#c9d1d9",
    "xtick.color":      "#8b949e",
    "ytick.color":      "#8b949e",
    "text.color":       "#c9d1d9",
    "grid.color":       "#21262d",
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   14,
    "axes.titleweight": "bold",
    "figure.titlesize": 16,
    "figure.titleweight": "bold",
})

ACCENT   = "#58a6ff"
ACCENT2  = "#3fb950"
ACCENT3  = "#f78166"
PALETTE  = [ACCENT, ACCENT2, ACCENT3, "#d2a8ff", "#ffa657", "#79c0ff", "#56d364"]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "visuals")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"  ✓ Saved → {path}")
    plt.close(fig)


# ── 1. Monthly Revenue Trend ───────────────────────────────────────────────────
revenue_data = {
    "month": ["Feb 2007", "Mar 2007", "Apr 2007"],
    "revenue": [80256.73, 96053.58, 2334.18],
    "transactions": [5644, 6754, 182],
}
df_rev = pd.DataFrame(revenue_data)

fig, ax1 = plt.subplots(figsize=(10, 5))
fig.suptitle("Monthly Revenue & Transaction Volume", y=1.01)

bars = ax1.bar(df_rev["month"], df_rev["revenue"], color=ACCENT, alpha=0.85, width=0.5, zorder=3)
ax1.set_ylabel("Revenue (USD)", color=ACCENT)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax1.tick_params(axis="y", labelcolor=ACCENT)

ax2 = ax1.twinx()
ax2.plot(df_rev["month"], df_rev["transactions"], color=ACCENT3, marker="o",
         linewidth=2.5, markersize=8, zorder=4)
ax2.set_ylabel("Transactions", color=ACCENT3)
ax2.tick_params(axis="y", labelcolor=ACCENT3)
ax2.set_facecolor("#161b22")

for bar, val in zip(bars, df_rev["revenue"]):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 800,
             f"${val:,.0f}", ha="center", va="bottom", fontsize=11, color="#c9d1d9", fontweight="bold")

ax1.set_title("Peak revenue of $96K in March 2007 | 6,754 transactions", fontsize=11,
              color="#8b949e", pad=8)
save(fig, "01_monthly_revenue.png")


# ── 2. Top 10 Customers by Spend ───────────────────────────────────────────────
customers = {
    "customer": ["Eleanor Hunt","Clara Shaw","Karl Seal","Rhonda Kennedy","Marion Snyder",
                 "Tommy Collazo","Tammy Sanders","Marcia Dean","Curtis Irby","Wesley Bull"],
    "total_spent": [641.55, 569.60, 568.58, 561.62, 524.61, 523.63, 519.61, 516.61, 507.62, 488.65],
}
df_cust = pd.DataFrame(customers).sort_values("total_spent")

fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle("Top 10 Customers by Lifetime Spend")
colors = [ACCENT if i == len(df_cust)-1 else "#30363d" for i in range(len(df_cust))]
bars = ax.barh(df_cust["customer"], df_cust["total_spent"], color=colors, edgecolor="none", zorder=3)

for bar, val in zip(bars, df_cust["total_spent"]):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
            f"${val:,.2f}", va="center", fontsize=10, color="#c9d1d9")

ax.set_xlabel("Total Spend (USD)")
ax.set_xlim(0, 720)
ax.set_title("Eleanor Hunt leads with $641.55 lifetime spend", fontsize=11, color="#8b949e", pad=8)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
save(fig, "02_top_customers.png")


# ── 3. Film Category Performance ──────────────────────────────────────────────
categories = {
    "category": ["Sports","Animation","Action","Sci-Fi","Family","Foreign",
                 "Drama","Documentary","Games","New","Children","Classics",
                 "Comedy","Horror","Travel","Music"],
    "rentals":  [1081,1065,1013,998,989,953,953,937,884,864,861,860,851,773,765,750],
    "revenue":  [14804,14014,13212,13503,12971,12613,12819,12344,11942,12013,
                 11232,11284,11926,10542,10177,9781],
}
df_cat = pd.DataFrame(categories).sort_values("rentals", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Film Category Performance: Rentals vs Revenue")

# Rentals
axes[0].barh(df_cat["category"][::-1], df_cat["rentals"][::-1],
             color=PALETTE[:len(df_cat)], edgecolor="none", zorder=3)
axes[0].set_xlabel("Total Rentals")
axes[0].set_title("Rentals by Category", fontsize=12)
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

# Revenue
axes[1].barh(df_cat.sort_values("revenue", ascending=False)["category"][::-1],
             df_cat.sort_values("revenue", ascending=False)["revenue"][::-1],
             color=PALETTE[:len(df_cat)], edgecolor="none", zorder=3)
axes[1].set_xlabel("Revenue (USD)")
axes[1].set_title("Revenue by Category", fontsize=12)
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.tight_layout()
save(fig, "03_category_performance.png")


# ── 4. Store Comparison ────────────────────────────────────────────────────────
stores = {
    "store": ["Store 1\nLethbridge, Canada", "Store 2\nWoodridge, Australia"],
    "customers": [326, 273],
    "revenue": [106647.76, 88530.62],
}
df_store = pd.DataFrame(stores)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle("Store Performance Comparison")

for ax, col, label, color, fmt in zip(
    axes,
    ["customers", "revenue"],
    ["Total Customers", "Total Revenue (USD)"],
    [ACCENT, ACCENT2],
    ["{:,.0f}", "${:,.0f}"],
):
    bars = ax.bar(df_store["store"], df_store[col], color=color, alpha=0.85, width=0.4, zorder=3)
    ax.set_ylabel(label)
    ax.set_title(label)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _, f=fmt: f.format(x)))
    for bar, val in zip(bars, df_store[col]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
                fmt.format(val), ha="center", fontsize=11, color="#c9d1d9", fontweight="bold")

plt.tight_layout()
save(fig, "04_store_comparison.png")


# ── 5. Top 10 Most Rented Films ────────────────────────────────────────────────
films = {
    "title": ["Bucket Brotherhood","Rocketeer Mother","Juggler Hardly","Ridgemont Submarine",
              "Grit Clockwork","Forward Temple","Scalawag Duck","Apache Divine",
              "Goodfellas Salute","Rush Goodfellas"],
    "rentals": [34, 33, 32, 32, 32, 32, 32, 31, 31, 31],
    "rate": [4.99, 0.99, 0.99, 0.99, 0.99, 2.99, 4.99, 4.99, 4.99, 0.99],
}
df_films = pd.DataFrame(films).sort_values("rentals")

fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle("Top 10 Most Rented Films")

norm = plt.Normalize(df_films["rate"].min(), df_films["rate"].max())
colors = plt.cm.Blues(norm(df_films["rate"]) * 0.7 + 0.3)

bars = ax.barh(df_films["title"], df_films["rentals"], color=colors, edgecolor="none", zorder=3)
for bar, val, rate in zip(bars, df_films["rentals"], df_films["rate"]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"{val} rentals  |  ${rate}", va="center", fontsize=9.5, color="#c9d1d9")

ax.set_xlabel("Total Rentals")
ax.set_xlim(0, 42)
ax.set_title("Bucket Brotherhood leads with 34 rentals | darker = higher rental rate",
             fontsize=10, color="#8b949e", pad=8)
save(fig, "05_top_films.png")


print("\n✅ All 5 visualisations generated successfully!")
print(f"   Saved to: {os.path.abspath(OUTPUT_DIR)}")
