# Aadhaar Forensic & Machine Learning Analysis: 2025 National Audit

**Author:** [Anmol,Janvi]  
**Scope:** 4.94 Million Records (March 2025 – December 2025)

---

## **1. Executive Summary**

This repository houses a comprehensive forensic audit of the Aadhaar ecosystem, analyzing nearly **5 million enrollment and update records**. Using statistical modeling, time-series analysis, and unsupervised machine learning (*Isolation Forests*), this study moves beyond simple descriptive statistics to identify systemic operational failures.

The core finding of this analysis is the bifurcation of the identity infrastructure into **"Three Indias"**:

1.  **Infant India:** In saturated states, the system has devolved into a birth registry (**65%** of intake is age 0-5).
2.  **Maintenance India:** In mature economies, the system is purely a utility for demographic updates (**7:1** update-to-enrollment ratio).
3.  **Excluded India:** In specific tribal regions (e.g., Meghalaya), the system is still in a desperate "catch-up" phase for adult enrollment.

Furthermore, forensic filters identified **31 "Ghost Districts"**—regions exhibiting statistical impossibilities that suggest deep-rooted data pipeline failures or organized enrollment fraud.

---

## **2. Repository Structure**

The project is organized to ensure reproducibility and logical flow.

```text
├── data/
│   ├── raw/                   # Original 12 CSV extracts (Enrollment, Demo, Bio)
│   └── processed/             # Cleaned and merged datasets for ML ingestion
│
├── notebooks/
│   ├── 01_Data_Cleaning.ipynb # Standardization of geographic nomenclature
│   ├── 02_EDA_Univariate.ipynb# Age distribution and monthly trend analysis
│   ├── 03_Forensics.ipynb     # Cross-dataset integrity checks (Ghost Districts)
│   └── 04_ML_Anomaly.ipynb    # Isolation Forest modeling for outlier detection
│
├── outputs/
│   ├── figures/               # High-resolution forensic charts (PNG)
│   └── tables/                # Exported anomalies and summary stats (CSV)
│
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
## **3. Detailed Technical Pipeline
Phase I: Data Engineering & Standardization
The primary challenge in analyzing Indian government datasets is inconsistent nomenclature.

Normalization: We implemented a custom mapping layer to standardize state names (e.g., mapping "Orissa" -> "Odisha", "Pondicherry" -> "Puducherry") to ensure 100% join integrity across disparate datasets.

Feature Engineering: Raw counts were converted into normalized density metrics (e.g., enrollments_per_1000_updates) to allow for fair comparison between massive states (UP) and smaller territories (Ladakh).

Time-Series Bucketing: Daily transaction logs were aggregated into monthly buckets (YYYY-MM) to smooth out daily server-side noise and isolate true operational trends.

Phase II: Forensic Statistical Analysis
We developed specific "integrity ratios" to health-check the system.

The Saturation Ratio: We compared the volume of Demographic Updates against New Enrollments. A ratio > 5:1 indicates a "Maintenance Phase." The national average was found to be 7.17:1.

The "Ghost District" Filter: We applied a Boolean mask to filter districts with:

Enrollments > 1,000 (High Volume)

Demographic Updates == 0 (Zero Footprint)

Result: This filter caught 31 districts that are statistically impossible in a natural human population, indicating artificial data generation.

Phase III: Machine Learning Anomaly Detection
To find non-linear outliers, we moved beyond threshold-based rules to unsupervised learning.

Algorithm: Isolation Forest (Ensemble Anomaly Detection).

Hyperparameters:

contamination=0.005 (Assuming 0.5% of data is anomalous).

n_estimators=100 (Number of base estimators in the ensemble).

Features Used: total_enrollment, child_percentage, adult_percentage, update_volume.

Outcome: The model successfully separated "Organic Growth" (normal clusters) from "Artificial Spikes" (outliers), flagging Meghalaya as a distinct cluster due to its inverted age pyramid.

## **4. Key Findings & Implications
A. The "Baby Bias" (Demographic Shift)
Observation: 65.2% of all new enrollments are infants (0-5 years), while adults (18+) constitute only 3.1%.

Implication: The Aadhaar system has fundamentally shifted its purpose. It is no longer an "Identity Card for All" but has effectively become a Digital Birth Certificate system. Adult saturation is near 100% in most regions.

B. The "Ghost District" Phenomenon (Integrity Crisis)
Observation: In Bengaluru Urban, the system recorded 23,074 new enrollments but 0.0% demographic updates.

Implication: This is the "Smoking Gun" of the analysis. A population of 23,000 real people will statistically generate hundreds of address or phone updates within months. A zero-update rate implies these IDs may be fraudulent ("Ghost IDs") or the data pipeline for this district is severed.

C. The "Exclusion Zone" (Regional Disparity)
Observation: While the rest of India enrolls babies, Meghalaya shows an anomaly rate of 15.36%, with 32% of its enrollments coming from adults.

Implication: This confirms that the Northeast was left behind in the initial waves of enrollment. The region is currently in a desperate "Catch-Up Phase," requiring different infrastructure than the rest of the country.

D. Operational Volatility (Campaign Mode)
Observation: Enrollment volume surged 3.5x in July 2025 and crashed by 47% in October 2025.

Implication: The system does not offer steady-state service. It relies on volatile "Campaign Mode" drives—massive, coordinated camps followed by periods of inactivity. This volatility correlates with high biometric failure rates (1.9M recaptures).

## **5. Visual Evidence
The outputs/figures/ directory contains high-fidelity charts supporting these findings:

cross_dataset_fraud_analysis.png: A scatter plot where the X-axis represents Enrollment and the Y-axis represents Updates. The "Ghost Districts" are visible as a flat line of bubbles clinging to the bottom axis.

age_distribution.png: A pie chart visualizing the 65.2% "Baby Bias," visually proving the saturation of the adult market.

ml_anomaly_detection.png: Visualizes the Isolation Forest decision boundary, highlighting the Meghalaya cluster as a distinct statistical outlier.

6. How to Run the Analysis
Prerequisites
Python 3.8+

Jupyter Notebook

Installation
Clone the repository:

Bash

git clone [https://github.com/yourusername/aadhaar-forensics-2025.git](https://github.com/yourusername/aadhaar-forensics-2025.git)
cd aadhaar-forensics-2025
Install dependencies:

Bash

pip install -r requirements.txt
Execution
Run the notebooks in sequential order to reproduce the pipeline:

Launch Jupyter: jupyter notebook

Open notebooks/01_Data_Cleaning.ipynb to prepare the raw data.

Run notebooks/04_ML_Anomaly.ipynb to generate the fraud detection models and anomaly lists.

7. Recommendations
Based on the forensic evidence, we propose three immediate actions:

1. Targeted Forensic Audit: The 31 Ghost Districts must be subjected to an immediate physical audit. The 0.0% update rate in major urban centers (Bengaluru) is a critical red flag for potential synthetic identity fraud.

2. Infrastructure Bifurcation: Stop treating India as a monolith. Divide the operational infrastructure into two distinct wings:

Wing A (Maintenance): Optimized for updates and biometric re-verification (for 90% of India).

Wing B (Enrollment): Mobile units focused exclusively on adult enrollment in the Northeast (Meghalaya/Assam).

3. Stabilization of Operations: End the "Campaign Mode" of operation. The 3.5x volatility spikes degrade data quality. Transition to a steady-state "Always On" service model to reduce the biometric recapture rate.
