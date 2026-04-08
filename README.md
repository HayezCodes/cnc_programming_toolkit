# CNC Programming Toolkit

A Streamlit-based toolkit for CNC programmers to quickly calculate speeds, feeds, threads, and machining geometry.

## Features
- Speeds & Feeds (Lathe + Mill)
- Thread lookup and modeling support
- Machining calculators:
  - Triangle
  - Keyway
  - Chamfer
  - Drill Breakthrough
- Standard / Metric support (diameters only)
- Shop-focused logic (IPR for lathe, IPM for mill)

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py