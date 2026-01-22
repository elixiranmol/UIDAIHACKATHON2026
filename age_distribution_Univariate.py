print("="*60)
print("📊 UNIVARIATE ANALYSIS: AGE DISTRIBUTION")
print("="*60)

# Calculate total by age group
age_totals = {
    'Age 0-5': enrol['age_0_5'].sum(),
    'Age 5-17': enrol['age_5_17'].sum(),
    'Age 18+': enrol['age_18_greater'].sum()
}

total = sum(age_totals.values())

print("\n📊 AGE GROUP DISTRIBUTION:")
for age_group, count in age_totals.items():
    pct = count / total * 100
    print(f"{age_group:12s}: {count:12,} ({pct:5.2f}%)")

print(f"\n{'Total':12s}: {total:12,} (100.00%)")

# 🚨 CRITICAL FINDING
print("\n" + "="*60)
print("🚨 CRITICAL FINDING: AGE DISTRIBUTION ANOMALY!")
print("="*60)
child_pct = age_totals['Age 0-5'] / total * 100
if child_pct > 50:
    print(f"⚠️  Age 0-5 represents {child_pct:.1f}% of enrollments!")
    print(f"⚠️  Normal population pyramid: 20-30% are children")
    print(f"⚠️  This is a {child_pct/30:.1f}x OVER-REPRESENTATION")
    print(f"\n💡 POSSIBLE CAUSES:")
    print(f"   1. Focus on newborn Aadhaar for welfare schemes")
    print(f"   2. Lack of follow-up enrollment after age 5")
    print(f"   3. Data collection bias toward birth registrations")
print("="*60)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Pie chart
colors = ['#ff9999', '#66b3ff', '#99ff99']
axes[0].pie(age_totals.values(), labels=age_totals.keys(), autopct='%1.1f%%', 
           startangle=90, colors=colors, textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[0].set_title('Age Distribution in Aadhaar Enrollments', fontsize=14, fontweight='bold')

# Bar chart
ages = list(age_totals.keys())
counts = list(age_totals.values())
axes[1].bar(ages, counts, color=colors, alpha=0.7, edgecolor='black')
axes[1].set_ylabel('Total Enrollments', fontsize=12)
axes[1].set_title('Enrollment Count by Age Group', fontsize=14, fontweight='bold')
axes[1].ticklabel_format(axis='y', style='plain')
for i, v in enumerate(counts):
    axes[1].text(i, v + max(counts)*0.02, f'{v:,}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('age_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
