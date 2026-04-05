# Quick Start Guide - Report Generation System

## 30-Second Setup

### 1. Verify Data File
```bash
# Check if clinical_trials_extracted.csv exists
dir clinical_trials_extracted.csv
```

### 2. Run Batch Generation
```bash
python batch_report_generator.py
```

### 3. Check Output
```bash
# View generated reports
dir reports_output/
```

---

## What Gets Generated

**17 Reports** in JSON format:
- clinical_positioning_*.json
- regulatory_risk_*.json
- financial_exposure_*.json
- time_to_market_*.json
- competitive_density_*.json
- partnership_licensing_*.json
- innovation_strength_*.json
- patent_landscape_*.json
- pipeline_monitoring_*.json
- market_access_*.json
- regulatory_landscape_*.json
- clinical_trials_*.json
- early_warning_*.json
- competitive_landscape_*.json
- sales_market_share_*.json
- patent_expiry_*.json
- fto_assessment_*.json

Plus: `summary_*.json` with overview of all reports

---

## Each Report Contains

```
✓ Metadata (report type, date, record count)
✓ Raw Data (companies, trials, diseases, phases)
✓ Analytics (distributions, aggregations, trends)
✓ 6 CI Scores with 95% Confidence Intervals:
  - Clinical Maturity
  - Regulatory Strength
  - Pipeline Diversification
  - Financial Stability
  - Partnership Activity
  - Innovation Index
✓ Source References
```

---

## Python Usage

### Generate All Reports
```python
from batch_report_generator import BatchReportGenerator

batch_gen = BatchReportGenerator("clinical_trials_extracted.csv")
result = batch_gen.run_batch_generation(export_format="json")
print(f"Generated {result['reports_generated']} reports")
```

### Generate for Specific Company
```python
result = batch_gen.generate_by_company("Absci Corporation Common Stock")
batch_gen.export_reports(result, format="json")
```

### Generate for Specific Disease Area
```python
result = batch_gen.generate_by_disease_area("Neurodegenerative Disorders")
batch_gen.export_reports(result, format="json")
```

### Generate Single Report
```python
from report_generator import ReportGenerator, ReportType

gen = ReportGenerator("clinical_trials_extracted.csv")
df = gen.apply_filters(company_name="Absci")
report = gen.generate_report(ReportType.CLINICAL_POSITIONING, df)
```

---

## CI Score Interpretation

| Score | Meaning |
|---|---|
| 80-100 | Excellent (Low Risk) |
| 60-79 | Good (Moderate Risk) |
| 40-59 | Fair (Moderate-High Risk) |
| 20-39 | Poor (High Risk) |
| 0-19 | Critical (Critical Risk) |

---

## Example Report Output

```json
{
  "metadata": {
    "report_type": "Clinical Positioning Analysis",
    "generated_date": "2026-04-04T10:30:00",
    "data_records": 150
  },
  "ci_domain_scores": {
    "Clinical Maturity": {
      "score": 65.3,
      "ci_lower": 58.2,
      "ci_upper": 72.4
    },
    "Regulatory Strength": {
      "score": 72.1,
      "ci_lower": 65.8,
      "ci_upper": 78.4
    },
    ...
  }
}
```

---

## File Structure

```
compintel/
├── report_generator.py           # Core engine
├── report_templates.py           # 17 templates
├── data_pipeline.py              # Extract→Process→Score→Export
├── batch_report_generator.py     # Batch orchestrator
├── CI_SCORING_ENGINE.md          # Score documentation
├── REPORT_GENERATION_SYSTEM.md   # Full documentation
├── QUICK_START.md                # This file
├── clinical_trials_extracted.csv # Input data
└── reports_output/               # Generated reports
```

---

## Troubleshooting

**Issue**: "File not found"
- Solution: Ensure `clinical_trials_extracted.csv` is in the same directory

**Issue**: "Missing required columns"
- Solution: Check CSV has all required columns (Company_Name, Trial_NCT_ID, etc.)

**Issue**: Low CI scores
- Solution: May indicate limited data. Check data quality and sample size.

---

## Next Steps

1. ✅ Run: `python batch_report_generator.py`
2. ✅ Review: Check `reports_output/` directory
3. ✅ Integrate: Use JSON exports in your dashboard
4. ✅ Schedule: Set up periodic generation
5. ✅ Customize: Modify templates as needed

---

## Documentation

- **Full System Guide**: `REPORT_GENERATION_SYSTEM.md`
- **CI Scoring Details**: `CI_SCORING_ENGINE.md`
- **Implementation Summary**: `IMPLEMENTATION_SUMMARY.md`
- **Code Comments**: See inline documentation in Python files

---

## Support

For detailed information:
- CI Score calculations → `CI_SCORING_ENGINE.md`
- System architecture → `REPORT_GENERATION_SYSTEM.md`
- Implementation details → `IMPLEMENTATION_SUMMARY.md`
- Code examples → See Python files
