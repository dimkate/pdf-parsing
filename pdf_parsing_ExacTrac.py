import pdfplumber
import os
import csv
import re

input_folder = 'anon_ExacTrac_data' 
output_csv = 'results_ExacTrac.csv'

# ID regex 
id_reg = re.compile(r'(?:ID|Patienten-ID):\s*([A-Za-z0-9]+)', re.IGNORECASE)
# Regex finding 3 numbers without parenthesis
num_reg = re.compile(r'(?<!\()(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)(?!\))')

os.makedirs(os.path.dirname(output_csv), exist_ok=True)

with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Patient_ID', 'LAT_mm', 'LNG_mm', 'VRT_mm', 'Pitch_deg', 'Roll_deg', 'Yaw_deg', 'Filename'])

    for filename in os.listdir(input_folder):
        if not filename.endswith(".pdf"): continue
        full_path = os.path.join(input_folder, filename)
        
        try:
            with pdfplumber.open(full_path) as pdf:
                p_id = "Unknown"
                data_written = False
                
                for page in pdf.pages:
                    # extraction of ID (if it has not been found already)
                    if p_id == "Unknown":
                        full_text = page.extract_text() or ""
                        id_match = id_reg.search(full_text)
                        if id_match: p_id = id_match.group(1)

                    # find the word "Referenzbildaufnahme" in text
                    words = page.extract_words()
                    target = next((w for w in words if "Referenzbildaufnahme" in w['text']), None)
                    
                    if target:
                        # set ROI around the word "Referenzbildaufnahme"
                        # top: 20 points above the word
                        # bottom: 100 points beneath the word (3-4 lines of data)
                        roi_box = (0, target['top'] - 20, page.width, target['bottom'] + 100)
                        
                        # crop page only in ROI
                        roi_text = page.crop(roi_box).extract_text()
                        
                        # find num_reg in ROI
                        matches = num_reg.findall(roi_text)
                        
                        if len(matches) >= 2:
                            # matches[0] --> mm, matches[1] --> degrees
                            writer.writerow([p_id, *matches[0], *matches[1], filename])
                            data_written = True
                            break # breah after finding the right values

                if not data_written:
                    writer.writerow([p_id, "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", filename])

        except Exception as e:
            print(f"Error in {filename}: {e}")

print("\nData saved in:", output_csv, "\n")
