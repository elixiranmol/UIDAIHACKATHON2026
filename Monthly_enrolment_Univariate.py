print("="*60)
print("📊 UNIVARIATE ANALYSIS: MONTHLY ENROLLMENT TREND")
print("="*60)

# Monthly aggregation
monthly_enrol = enrol.groupby('year_month').agg({
    'total_enrol': 'sum',
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum'
}).sort_index()

print("\n📅 MONTHLY ENROLLMENT DATA:")
display(monthly_enrol)

# Calculate month-over-month growth
monthly_enrol['mom_growth'] = monthly_enrol['total_enrol'].pct_change() * 100
monthly_enrol['mom_growth'] = monthly_enrol['mom_growth'].round(2)

print("\n📈 MONTH-OVER-MONTH GROWTH RATE:")
display(monthly_enrol[['total_enrol', 'mom_growth']])

# Visualize
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Line chart - total enrollments
monthly_enrol['total_enrol'].plot(ax=axes[0], marker='o', linewidth=2, markersize=8, color='green')
axes[0].set_title('Total Enrollments Over Time (Mar-Dec 2025)', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Total Enrollments', fontsize=12)
axes[0].set_xlabel('Month', fontsize=12)
axes[0].grid(alpha=0.3)
axes[0].ticklabel_format(axis='y', style='plain')

# Add trend line
from scipy.stats import linregress
x = np.arange(len(monthly_enrol))
slope, intercept, r_value, p_value, std_err = linregress(x, monthly_enrol['total_enrol'])
trend_line = slope * x + intercept
axes[0].plot(monthly_enrol.index, trend_line, 'r--', linewidth=2, label=f'Trend (R²={r_value**2:.3f})')
axes[0].legend()

# Stacked area chart - age groups
monthly_enrol[['age_0_5', 'age_5_17', 'age_18_greater']].plot.area(
    ax=axes[1], 
    stacked=True,
    color=['#ff9999', '#66b3ff', '#99ff99'],
    alpha=0.7
)
axes[1].set_title('Age Group Composition Over Time', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Enrollments', fontsize=12)
axes[1].set_xlabel('Month', fontsize=12)
axes[1].legend(['Age 0-5', 'Age 5-17', 'Age 18+'], loc='upper left')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('monthly_trend.png', dpi=300, bbox_inches='tight')
plt.show()

# Insights
print("\n" + "="*60)
print("💡 KEY INSIGHTS:")
highest_month = monthly_enrol['total_enrol'].idxmax()
lowest_month = monthly_enrol['total_enrol'].idxmin()
print(f"📈 Highest enrollment month: {highest_month} ({monthly_enrol.loc[highest_month, 'total_enrol']:,})")
print(f"📉 Lowest enrollment month: {lowest_month} ({monthly_enrol.loc[lowest_month, 'total_enrol']:,})")
print(f"📊 Average monthly enrollment: {monthly_enrol['total_enrol'].mean():,.0f}")
print(f"📊 Trend slope: {slope:,.0f} enrollments/month ({'increasing' if slope > 0 else 'decreasing'})")
print("="*60)