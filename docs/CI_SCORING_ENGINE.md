# CI Scoring Engine - Calculate Domain Scores with Confidence Intervals

## Overview
The CI Scoring Engine calculates 6 domain-specific competitive intelligence scores (0-100) with 95% confidence intervals for each report.

## 6 CI Domains

### 1. Clinical Maturity Score
**Definition**: Measures the advancement of clinical development pipeline

**Calculation**:
- Phase I: 20 points
- Phase II: 40 points
- Phase III: 70 points
- Phase IV: 90 points
- Early Phase I: 10 points

**Status Multipliers**:
- RECRUITING: 1.2x
- ACTIVE_NOT_RECRUITING: 1.1x
- COMPLETED: 0.9x
- TERMINATED: 0.5x

**Formula**: `Mean(Phase_Score × Status_Multiplier)` across all trials

**Data Sources**:
- Trial_Clinical_Phase
- Trial_Overall_Status
- Trial_NCT_ID

---

### 2. Regulatory Strength Score
**Definition**: Assesses regulatory pathway progress and market access readiness

**Status Weights**:
- COMPLETED: 80 points
- ACTIVE_NOT_RECRUITING: 60 points
- RECRUITING: 50 points
- TERMINATED: 20 points
- UNKNOWN: 30 points

**Formula**: `Mean(Status_Weight)` across all trials

**Data Sources**:
- Trial_Overall_Status
- Trial_Clinical_Phase
- Company regulatory milestones

---

### 3. Pipeline Diversification Score
**Definition**: Measures breadth of pipeline across diseases and indications

**Calculation**:
```
Diversity_Score = Min(100, (Unique_Diseases + Unique_Areas × 2) × 5)
```

**Factors**:
- Number of unique diseases
- Number of unique disease areas
- Lead product count
- Indication breadth

**Data Sources**:
- Disease
- Disease_Area
- Lead_Product

---

### 4. Financial Stability Score
**Definition**: Evaluates financial health and investment capacity

**Calculation**:
```
Score = 50 + 20 × Log10(Avg_Market_Cap / Median_Market_Cap)
Clipped to [20, 95]
```

**Factors**:
- Market capitalization
- Stock price trends
- Revenue stability
- Investor highlights

**Data Sources**:
- Market_Cap
- Last_Sale
- Investor_Highlights

---

### 5. Partnership Activity Score
**Definition**: Measures collaboration and licensing activity

**Calculation**:
```
Partnership_Ratio = Count(Non-Null Partnerships) / Total_Records
Score = 30 + (Partnership_Ratio × 70)
```

**Factors**:
- Number of partnerships
- Collaboration types
- Licensing deals
- Strategic alliances

**Data Sources**:
- Partnerships
- Company_Name
- Lead_Product

---

### 6. Innovation Index Score
**Definition**: Assesses technology platform strength and innovation capability

**Calculation**:
```
Tech_Ratio = Count(Non-Null Technology) / Total_Records
Score = 40 + (Tech_Ratio × 60)
```

**Factors**:
- Technology platform diversity
- Novel mechanisms
- IP portfolio strength
- Patent count

**Data Sources**:
- Technology
- Lead_Product
- Company innovation metrics

---

## Confidence Interval Calculation

### 95% Confidence Interval Formula
```
CI_Lower = Mean - (1.96 × Standard_Error)
CI_Upper = Mean + (1.96 × Standard_Error)

Where:
Standard_Error = StdDev(Scores) / √N
N = Number of samples
```

### Interpretation
- **Score**: Point estimate of CI metric
- **CI_Lower**: Lower bound of 95% confidence interval
- **CI_Upper**: Upper bound of 95% confidence interval

Example: `75.2 (95% CI: 68.5-81.9)` means we are 95% confident the true score lies between 68.5 and 81.9

---

## Data Requirements

### Mandatory Fields
- Company_Name
- Trial_NCT_ID
- Trial_Clinical_Phase
- Trial_Overall_Status
- Disease
- Disease_Area
- Market_Cap
- Partnerships
- Technology

### Optional Fields
- Lead_Product
- Investor_Highlights
- Last_Sale

---

## Score Interpretation Guide

### Score Ranges
| Range | Interpretation | Risk Level |
|-------|---|---|
| 80-100 | Excellent | Low |
| 60-79 | Good | Moderate |
| 40-59 | Fair | Moderate-High |
| 20-39 | Poor | High |
| 0-19 | Critical | Critical |

---

## Report Generation Workflow

```
1. DATA EXTRACTION
   ↓
2. DATA CLEANING & VALIDATION
   ↓
3. APPLY FILTERS (if any)
   ↓
4. CALCULATE 6 CI SCORES
   ├─ Clinical Maturity
   ├─ Regulatory Strength
   ├─ Pipeline Diversification
   ├─ Financial Stability
   ├─ Partnership Activity
   └─ Innovation Index
   ↓
5. CALCULATE 95% CONFIDENCE INTERVALS
   ↓
6. GENERATE REPORT WITH:
   ├─ Raw Data Summary
   ├─ Processed Analytics
   ├─ CI Domain Scores
   └─ Source References
   ↓
7. EXPORT (JSON/CSV/Excel)
```

---

## Example Report Output

```json
{
  "metadata": {
    "report_type": "Clinical Positioning Analysis",
    "generated_date": "2026-04-04T10:30:00",
    "data_records": 150,
    "filters_applied": {}
  },
  "ci_domain_scores": {
    "Clinical Maturity": {
      "score": 65.3,
      "ci_lower": 58.2,
      "ci_upper": 72.4,
      "description": "Phase progression, trial status, enrollment"
    },
    "Regulatory Strength": {
      "score": 72.1,
      "ci_lower": 65.8,
      "ci_upper": 78.4,
      "description": "Approvals, regulatory milestones, market access"
    },
    "Pipeline Diversification": {
      "score": 58.9,
      "ci_lower": 52.1,
      "ci_upper": 65.7,
      "description": "Number of indications, disease areas, lead products"
    },
    "Financial Stability": {
      "score": 71.2,
      "ci_lower": 64.5,
      "ci_upper": 77.9,
      "description": "Market cap, stock price, investor highlights"
    },
    "Partnership Activity": {
      "score": 52.3,
      "ci_lower": 45.6,
      "ci_upper": 59.0,
      "description": "Partnerships, collaborations, licensing deals"
    },
    "Innovation Index": {
      "score": 61.7,
      "ci_lower": 54.2,
      "ci_upper": 69.2,
      "description": "Technology platform, novel mechanisms, IP strength"
    }
  },
  "source_references": {
    "primary": ["clinicaltrials.gov", "NASDAQ", "SEC Filings"],
    "secondary": ["Company Press Releases", "Patent Databases", "HTA Submissions"]
  }
}
```

---

## Usage Examples

### Python Implementation

```python
from report_generator import ReportGenerator, ReportType
from data_pipeline import DataPipeline

# Initialize
pipeline = DataPipeline("clinical_trials_extracted.csv")

# Run pipeline
result = pipeline.run_pipeline(output_format="json")

# Access scores
print(result["scores"])
# Output: {
#   "Clinical Maturity": 65.3,
#   "Regulatory Strength": 72.1,
#   ...
# }
```

### Batch Generation

```python
from batch_report_generator import BatchReportGenerator

# Initialize
batch_gen = BatchReportGenerator("clinical_trials_extracted.csv")

# Generate all 17 reports
result = batch_gen.run_batch_generation(export_format="json")

# Access results
print(f"Generated {result['reports_generated']} reports")
```

---

## Data Quality Considerations

### Missing Data Handling
- Market_Cap: Filled with median value
- Partnerships: Treated as 0 if null
- Technology: Treated as 0 if null
- Trial_Overall_Status: Defaulted to "UNKNOWN"

### Outlier Detection
- Market cap values > 3 standard deviations flagged
- Scores automatically clipped to [0, 100] range

### Validation Rules
- Minimum 5 records required for CI calculation
- Confidence intervals automatically adjusted for small samples

---

## Performance Metrics

- **Processing Time**: ~2-5 seconds per 1000 records
- **Memory Usage**: ~50MB per 10,000 records
- **Accuracy**: ±5% for CI bounds with n≥30

---

## References

- Clinical Trial Data: clinicaltrials.gov API
- Financial Data: NASDAQ
- Regulatory Data: SEC EDGAR, FDA
- Patent Data: USPTO, WIPO
