# ExacTrac Data Extractor

This Python tool automates the extraction of patient IDs and shifts (LAT, LNG, VRT, Pitch, Roll, Yaw) from **Brainlab ExacTrac** PDF reports.

# Features
- Scans a directory for setup report PDFs.
- Automatically identifies the **Patient ID**.
- Locates the **"Referenzbildaufnahme"** section.
- Extracts shift (mm) and rotation (deg) values using Regex.
- Exports all data into a clean ';' delimited '.csv' file for Excel analysis.

# How to Use
1. Install Dependencies:
   You will need the 'pdfplumber' library.
