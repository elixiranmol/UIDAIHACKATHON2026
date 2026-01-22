print("="*60)
print("📊 BIVARIATE ANALYSIS: AGE DISTRIBUTION OVER TIME")
print("="*60)

# Calculate age percentages by month
month_age = enrol.groupby('year_month')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
month_age_pct = month_age.div(month_age.sum(axis=1), axis=0) * 100

print("\n📊 AGE PERCENTAGE BY MONTH:")
display(month_age_pct.round(2))

# Check for trend
print("\n📈 TREND ANALYSIS:")
from scipy.stats import linregress
x = np.arange(len(month_age_pct))
slope_child, _, r_child, _, _ = linregress(x, month_age_pct['age_0_5'])
slope_youth, _, r_youth, _, _ = linregress(x, month_age_pct['age_5_17'])
slope_adult, _, r_adult, _, _ = linregress(x, month_age_pct['age_18_greater'])

print(f"Age 0-5 trend:  {slope_child:+.3f}% per month (R²={r_child**2:.3f})")
print(f"Age 5-17 trend: {slope_youth:+.3f}% per month (R²={r_youth**2:.3f})")
print(f"Age 18+ trend:  {slope_adult:+.3f}% per month (R²={r_adult**2:.3f})")

if abs(slope_child) < 0.5 and abs(slope_youth) < 0.5:
    print("\n🚨 FINDING: Age distribution is STABLE over time")
    print("   → This confirms SYSTEMIC data collection bias, not improving")
else:
    print("\n💡 FINDING: Age distribution is CHANGING over time")
    print("   → System is gradually correcting the bias")

# Visualize
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Line chart - percentages
month_age_pct.plot(ax=axes[0], marker='o', linewidth=2, markersize=8)
axes[0].set_title('Age Group Percentage Trend Over Time', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Percentage (%)', fontsize=12)
axes[0].set_xlabel('Month', fontsize=12)
axes[0].legend(['Age 0-5', 'Age 5-17', 'Age 18+'], loc='best')
axes[0].grid(alpha=0.3)
axes[0].axhline(y=33.33, color='red', linestyle='--', alpha=0.5, label='Equal distribution')

# Stacked area chart
month_age_pct.plot.area(ax=axes[1], color=['#ff9999', '#66b3ff', '#99ff99'], alpha=0.7)
axes[1].set_title('Age Group Composition Over Time', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Percentage (%)', fontsize=12)
axes[1].set_xlabel('Month', fontsize=12)
axes[1].legend(['Age 0-5', 'Age 5-17', 'Age 18+'], loc='best')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('age_trend.png', dpi=300, bbox_inches='tight')
plt.show()

# Final insight based on the last month's data
last_month = month_age_pct.iloc[-1]
print("\n" + "="*60)
print(f"📅 LATEST STATUS ({month_age_pct.index[-1]}):")
print(f"   - Babies (0-5): {last_month['age_0_5']:.1f}%")
print(f"   - School Kids (5-17): {last_month['age_5_17']:.1f}%")
print(f"   - Adults (18+): {last_month['age_18_greater']:.1f}%")
if last_month['age_0_5'] > 60:
    print("⚠️  CONCLUSION: The system is STILL in 'Birth Registration' mode.")
elif last_month['age_5_17'] > 40:
    print("⚠️  CONCLUSION: The system has shifted to 'School Catch-up' mode.")
else:
    print("✅  CONCLUSION: The system is reaching a balanced state.")
print("="*60)