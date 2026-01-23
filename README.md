# UIDAIHACKATHON2026
Aadhaar Enrollment and Update Analysis (2025)
Overview
This repository contains a comprehensive forensic analysis of 4.94 million Aadhaar transaction records spanning March to December 2025. The study identifies a critical shift in the Aadhaar ecosystem from a universal identity program to a bifurcated system characterized by infant registration, regional exclusion zones, and operational volatility.

Dataset Description
The analysis integrates 12 CSV files across three primary domains:

Enrollment Data: 1,006,029 records capturing new registrations across three age cohorts (0-5, 5-17, 18+).

Demographic Updates: 2,071,474 records tracking address, name, and mobile number changes.

Biometric Updates: 1,861,893 records documenting fingerprint and iris re-capture events.

Analysis Pipeline
1. Data Cleaning and Standardization
To ensure cross-dataset integrity, the following preprocessing steps were implemented:

Naming Conventions: Standardized state and district names to resolve inconsistencies (e.g., mapping "West Bengli" to "West Bengal").

Temporal Alignment: Standardized all date formats to DD-MM-YYYY and handled missing or null values.

Deduplication: Identified and removed duplicate records to prevent volume inflation.

2. Feature Engineering
Derived new metrics to transition from raw counts to diagnostic indicators:

Total Activity: Aggregated fragmented age columns into single volume metrics for each dataset.

Normalized Ratios: Calculated child_pct, youth_pct, and adult_pct to enable fair comparison between states of varying sizes.

Time-Series Buckets: Extracted monthly periods (year_month) to isolate long-term trends from daily noise.

3. Univariate Analysis
Established baseline distributions for the system:

Geographic Distribution: Identified top-performing states (Uttar Pradesh, Bihar) and underserved districts using a "Low Activity Threshold" of <100 records.

Age Composition: Discovered the "Baby Bias" anomaly, where 65.2% of new enrollments are infants (0-5), indicating adult saturation.

Monthly Trends: Quantified system volatility, noting a 3.5x surge in July followed by a 47% crash in October.

4. Bivariate Analysis
Correlated multiple variables to identify regional phases:

State x Age Mix: Classified regions into three modes: "Baby Registration" (South/Central), "Campaign Mode" (North/Urban), and "Adult Catch-up" (Northeast).

Time x Age Composition: Tracked the worsening infant bias, which grew from 32% in March to 73.7% in December.

5. Forensic and Integrity Analysis
Utilized cross-dataset comparisons to detect systemic failures:

Update-to-Enrollment Ratio: Found a 7:1 ratio (Demographic Updates vs. Enrollments), confirming the system is in a "Maintenance Phase."

Ghost District Detection: Isolated 31 districts where enrollments were high but digital footprints (updates) were zero.

Bengaluru Case Study: Identified 23,074 enrollments in Bengaluru Urban with a 0.0% update rate, suggesting data pipeline failures or fraudulent identities.

6. Machine Learning Anomaly Detection
Implemented an Isolation Forest model (Contamination = 0.5%) to find statistical outliers:

Meghalaya Outlier: Flagged Meghalaya with a 15.36% anomaly rate (6.5x national average) due to its unique "Adult Enrollment" status.

Pattern Classification: Categorized anomalies into "Extreme Volume" (mass camps) and "Adult Spikes" (exclusion zones).

Key Findings Summary
Saturation: Aadhaar has effectively reached 100% adult saturation, with 65% of new intake now being newborns.

Volatility: The system operates in an unstable "Campaign Mode" characterized by extreme surges.

Integrity Crisis: 31 districts exhibit "Ghost Enrollment" patterns requiring immediate audit.

Regional Disparity: The Northeast remains in a distinct "Exclusion Phase," requiring adult-focused infrastructure.

Requirements
Python 3.x

Pandas, NumPy

Matplotlib, Seaborn

Scikit-Learn (for Isolation Forest)

Scipy (for Linear Regression)
