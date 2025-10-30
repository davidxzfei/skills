# Document Skills - 10 Complete Demo Examples

This document provides ten detailed, hands-on examples demonstrating how to leverage the document skills (`docx`, `pdf`, `pptx`, `xlsx`) in Claude Code. Each example includes context, the full prompt to send to Claude, expected workflow, and sample outputs.

---

## Demo 1: Create a Professional Word Document from Notes

**Skill:** `docx`  
**Scenario:** Transform raw meeting notes into a formatted project proposal document

### Sample Input File
Create `notes/meeting_notes.txt`:
```
Project Apex - Strategic Roadmap
- Launch new mobile app Q2 2025
- Target market: enterprise users
- Budget: $450k
- Timeline: 6 months
- Key features: offline sync, real-time collaboration, security compliance
- Team: 5 developers, 2 designers, 1 PM
```

### Prompt to Claude
```
Use the docx skill to create a professional project proposal from notes/meeting_notes.txt. 
Format it with:
- A title page with "Project Apex Strategic Roadmap"
- Executive summary section
- Project scope and objectives
- Timeline and milestones
- Budget breakdown
- Team structure
Save as proposals/project_apex.docx
```

### Expected Workflow
1. Claude reads the `docx-js.md` documentation
2. Creates a TypeScript/JavaScript file using the docx library
3. Structures content with proper heading hierarchy
4. Applies professional formatting (fonts, spacing, styles)
5. Exports to `proposals/project_apex.docx`

### Key Learning
- How docx-js creates structured documents from scratch
- YAML frontmatter triggers the right workflow
- Document object model for sections, paragraphs, text runs

---

## Demo 2: Track Changes in a Contract with Redlining

**Skill:** `docx`  
**Scenario:** Review and mark up a legal agreement with tracked changes

### Sample Input File
Create `contracts/service_agreement.docx` (or use any existing Word doc)

### Prompt to Claude
```
Use the docx skill to review contracts/service_agreement.docx and implement these changes with tracked changes:
1. Change payment term from "30 days" to "45 days net" in Section 3
2. Update the liability cap from $50,000 to $100,000 in Section 5.2
3. Add "and its affiliates" after "Company" in the Definitions section
4. Change the renewal term from "automatic" to "upon mutual written agreement"

Save the reviewed document as contracts/service_agreement_reviewed.docx
```

### Expected Workflow
1. Claude converts docx to markdown to understand structure
2. Unpacks the docx file using `ooxml/scripts/unpack.py`
3. Greps `word/document.xml` to locate exact text passages
4. Creates Python scripts using the Document library to insert tracked changes
5. Batches changes logically (e.g., definitions first, then payment terms)
6. Packs the modified directory back to docx
7. Verifies all changes with pandoc conversion

### Key Learning
- Redlining workflow for professional document review
- How tracked changes appear in OOXML (`<w:ins>` and `<w:del>` tags)
- Batch strategy for managing multiple edits
- Importance of precise text matching with grep

---

## Demo 3: Convert Word Document to Images for Visual Review

**Skill:** `docx`  
**Scenario:** Create page-by-page screenshots of a report for presentation

### Sample Input File
Use any multi-page Word document: `reports/annual_report.docx`

### Prompt to Claude
```
Use the docx skill to convert reports/annual_report.docx into individual page images 
at 150 DPI resolution. Save them as report_page_1.jpg, report_page_2.jpg, etc. 
in the images/ folder.
```

### Expected Workflow
1. Convert DOCX to PDF using LibreOffice headless mode
2. Use `pdftoppm` to render each PDF page as a JPEG
3. Output numbered image files

### Sample Commands
```bash
soffice --headless --convert-to pdf reports/annual_report.docx
pdftoppm -jpeg -r 150 annual_report.pdf images/report_page
```

### Key Learning
- Two-step conversion process (DOCX → PDF → images)
- Quality/size trade-offs with DPI settings
- Batch processing for multi-page documents

---

## Demo 4: Extract Tables from a PDF Report

**Skill:** `pdf`  
**Scenario:** Pull financial tables from a PDF earnings call transcript

### Sample Input File
Create or find a PDF with tables: `finance/q4_earnings.pdf`

### Prompt to Claude
```
Use the pdf skill to extract all tables from finance/q4_earnings.pdf. 
Convert each table to CSV format and save them as:
- table_1.csv
- table_2.csv
- etc.
Also provide a summary of what data each table contains.
```

### Expected Workflow
1. Claude uses `pdfplumber.open()` to read the PDF
2. Iterates through pages calling `page.extract_tables()`
3. Converts each table array to CSV
4. Analyzes headers to describe table contents

### Sample Python Code
```python
import pdfplumber
import csv

with pdfplumber.open("finance/q4_earnings.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            with open(f"table_{i+1}_{j+1}.csv", "w") as f:
                writer = csv.writer(f)
                writer.writerows(table)
```

### Key Learning
- pdfplumber's table detection capabilities
- Handling multi-page PDFs with tables on different pages
- CSV export for downstream analysis

---

## Demo 5: Fill Out a PDF Form Programmatically

**Skill:** `pdf`  
**Scenario:** Complete a tax form with data from a JSON file

### Sample Input Files
- `tax/w9_form.pdf` (blank IRS W-9 form)
- `tax/vendor_info.json`:
```json
{
  "name": "Acme Consulting LLC",
  "business_name": "Acme Consulting LLC",
  "tax_classification": "LLC",
  "address": "123 Main Street",
  "city_state_zip": "San Francisco, CA 94102",
  "ssn_ein": "12-3456789"
}
```

### Prompt to Claude
```
Use the pdf skill to fill the W-9 form at tax/w9_form.pdf with the data 
from tax/vendor_info.json. Map the JSON fields to the appropriate form fields, 
flatten the result, and save as tax/w9_completed.pdf.
```

### Expected Workflow
1. Claude reads `pdf/forms.md` for form-filling guidance
2. Inspects form fields with `pypdf`
3. Maps JSON keys to PDF field names
4. Fills fields using `PdfWriter.update_page_form_field_values()`
5. Flattens the form so it can't be edited further
6. Saves the completed PDF

### Key Learning
- Inspecting interactive PDF form fields
- Programmatic form completion at scale
- Flattening to create read-only PDFs

---

## Demo 6: Split and Merge PDF Documents

**Skill:** `pdf`  
**Scenario:** Extract specific sections from a large manual and create a custom guide

### Sample Input File
`manuals/employee_handbook.pdf` (100-page document)

### Prompt to Claude
```
Use the pdf skill to:
1. Extract pages 1-5 (Introduction) to intro.pdf
2. Extract pages 20-35 (Benefits) to benefits.pdf
3. Extract pages 80-85 (Policies) to policies.pdf
4. Merge these three sections into a new onboarding_guide.pdf

Keep them in the order: intro → benefits → policies
```

### Expected Workflow
1. Read the handbook PDF with `PdfReader`
2. Create separate `PdfWriter` objects for each section
3. Add specified page ranges to each writer
4. Write individual section PDFs
5. Create a new writer and merge all sections in order
6. Save final merged PDF

### Key Learning
- Page extraction by range
- Multi-document merging
- Reordering and reorganizing PDF content

---

## Demo 7: Build a Branded Pitch Deck Presentation

**Skill:** `pptx`  
**Scenario:** Create a startup pitch deck with custom branding

### Sample Input File
Create `pitch/content.md`:
```markdown
# Slide 1: Company Overview
**TechFlow Solutions** - Revolutionizing Enterprise Workflow Automation

# Slide 2: The Problem
- Manual processes cost businesses $450B annually
- 60% of knowledge workers spend 3+ hours/day on repetitive tasks
- Legacy systems don't integrate well

# Slide 3: Our Solution
AI-powered workflow engine that:
- Learns from existing processes
- Auto-generates integrations
- Reduces manual work by 75%

# Slide 4: Market Opportunity
TAM: $12B | SAM: $3.5B | SOM: $450M (Year 3)

# Slide 5: Traction
- 15 enterprise customers
- $2M ARR
- 150% YoY growth

# Slide 6: The Ask
Raising $5M Series A for sales and product expansion
```

### Prompt to Claude
```
Use the pptx skill to create a professional pitch deck from pitch/content.md.

Design requirements:
- Use a Deep Purple & Emerald color palette (#B165FB, #40695B, #181B24)
- Modern, minimal design with strong visual hierarchy
- Include slide numbers
- Use geometric accent elements
- Apply bold sans-serif fonts
- Each slide should have a strong focal point

Save as pitch/techflow_deck.pptx
```

### Expected Workflow
1. Claude reads the design requirements and plans visual approach
2. Creates HTML slides with CSS styling matching the color palette
3. Structures content with proper heading hierarchy
4. Adds visual elements (dividers, accent shapes)
5. Converts HTML to PPTX using html2pptx
6. Outputs the final presentation

### Key Learning
- html2pptx workflow for custom-designed decks
- Color palette selection and application
- Visual hierarchy through typography and layout
- Content-driven design choices

---

## Demo 8: Edit PowerPoint Speaker Notes

**Skill:** `pptx`  
**Scenario:** Add detailed presenter notes to an existing deck

### Sample Input File
Use any existing PowerPoint: `presentations/team_update.pptx`

### Prompt to Claude
```
Use the pptx skill to add comprehensive speaker notes to presentations/team_update.pptx.

For each slide, create notes that include:
- Key talking points (3-5 bullets)
- Timing guidance (suggested minutes per slide)
- Transition cues to the next slide
- Any relevant statistics or details not shown on slides

Save the updated deck as presentations/team_update_with_notes.pptx
```

### Expected Workflow
1. Unpack the PPTX using `ooxml/scripts/unpack.py`
2. Read each slide's content from `ppt/slides/slideN.xml`
3. Create or update `ppt/notesSlides/notesSlideN.xml` for each slide
4. Insert structured speaker notes in the notes text frame
5. Pack the modified presentation

### Key Learning
- PPTX file structure and notesSlides XML format
- Programmatic notes creation
- Aligning notes with slide content

---

## Demo 9: Create a Financial Dashboard in Excel

**Skill:** `xlsx`  
**Scenario:** Build a KPI tracking spreadsheet with formulas and formatting

### Sample Input File
Create `data/monthly_metrics.csv`:
```csv
Month,Revenue,Expenses,New Customers,Churn
Jan,120000,85000,45,3
Feb,135000,88000,52,4
Mar,142000,91000,48,2
Apr,155000,95000,61,5
```

### Prompt to Claude
```
Use the xlsx skill to create a financial dashboard at dashboards/kpi_tracker.xlsx 
using the data from data/monthly_metrics.csv.

Include:
1. Raw data sheet with the CSV imported
2. Dashboard sheet with:
   - Total revenue, expenses, profit
   - Average new customers per month
   - Churn rate calculation
   - Month-over-month growth percentages
   - Conditional formatting (green for positive growth, red for negative)
3. A simple column chart showing revenue vs expenses by month

Use professional formatting with clear headers and appropriate number formats.
```

### Expected Workflow
1. Claude reads CSV data
2. Creates workbook with multiple sheets
3. Writes raw data to first sheet
4. Adds calculated columns with Excel formulas (SUM, AVERAGE, percentage growth)
5. Applies conditional formatting rules
6. Creates chart objects
7. Styles with borders, fonts, and number formats
8. Saves as XLSX

### Sample Python (using openpyxl)
```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import PatternFill

wb = Workbook()
ws = wb.active
ws.title = "Dashboard"

# Add formulas
ws['B2'] = '=SUM(Data!B2:B5)'
ws['B3'] = '=SUM(Data!C2:C5)'
ws['B4'] = '=B2-B3'

# Conditional formatting
ws.conditional_formatting.add('B2:B4', 
    ColorScaleRule(start_type='min', start_color='FF0000',
                   end_type='max', end_color='00FF00'))
```

### Key Learning
- Excel formula syntax in programmatic creation
- Multi-sheet workbook organization
- Conditional formatting and charting
- Professional spreadsheet design patterns

---

## Demo 10: Clean and Analyze Sales Pipeline Data

**Skill:** `xlsx`  
**Scenario:** Import messy CSV data, clean it, and create a pivot analysis

### Sample Input File
Create `sales/pipeline_raw.csv`:
```csv
Lead Name,Company,Status,Value,Date Created,Owner
John Smith,Acme Corp,Qualified,"$45,000",1/15/2024,Sarah
Jane Doe,Beta Inc,Negotiation,"$82,500",1/18/2024,Mike
Bob Johnson,Gamma LLC,Qualified,"$32,000",1/20/2024,Sarah
Alice Williams,Delta Co,Closed Won,"$67,000",1/22/2024,Mike
Charlie Brown,Epsilon,Qualified,"$28,500",1/25/2024,Sarah
```

### Prompt to Claude
```
Use the xlsx skill to clean and analyze sales/pipeline_raw.csv:

1. Clean the data:
   - Remove $ and commas from Value column, convert to numbers
   - Parse Date Created into proper date format
   - Standardize Status values
   
2. Add calculated columns:
   - Days in pipeline (today - date created)
   - Win probability based on status
   - Weighted value (value × probability)
   
3. Create pivot table showing:
   - Total pipeline value by owner
   - Count of deals by status
   - Average deal size by owner
   
4. Add a summary sheet with key metrics:
   - Total pipeline value
   - Weighted pipeline value
   - Average deal size
   - Conversion rate
   
Save as sales/pipeline_analysis.xlsx
```

### Expected Workflow
1. Read CSV with pandas or csv module
2. Clean data (regex for currency, date parsing)
3. Add calculated columns with formulas or Python logic
4. Create pivot table structure in Excel
5. Generate summary metrics
6. Format for readability (currency format, borders, bold headers)
7. Save multi-sheet workbook

### Key Learning
- Data cleaning patterns for real-world messy data
- Pivot table creation programmatically
- Business intelligence patterns in spreadsheets
- Formula-driven vs calculated values

---

## General Tips for Using Document Skills

### 1. Be Specific About File Paths
Always provide absolute or relative paths from your workspace root.

### 2. Describe the Desired Output
Rather than saying "edit this document," specify what changes you want and in what format.

### 3. Provide Context for Design Decisions
For presentations and formatted documents, mention tone, audience, and brand guidelines.

### 4. Request Verification Steps
Ask Claude to verify results (e.g., "confirm all changes were applied" or "show me the first few rows of the output").

### 5. Iterate on Complex Tasks
For documents with many changes, start with a small batch to verify the approach works, then scale up.

### 6. Check Dependencies
If you see missing library errors, Claude can install them with apt or pip commands.

### 7. Combine Skills
You can use multiple skills in one request: "Extract tables from this PDF, then create an Excel analysis."

### 8. Save Intermediate Files
For complex pipelines, save intermediate outputs (e.g., extracted data, draft versions) for debugging.

### 9. Ask for Explanations
Claude can walk through the workflow step-by-step to help you understand how skills work under the hood.

### 10. Explore the Documentation
Each skill has extensive markdown docs (`SKILL.md`, `ooxml.md`, `docx-js.md`, etc.) that Claude references. You can read these too for deeper understanding.

---

## Next Steps

- **Try these examples** in your Claude Code workspace
- **Modify prompts** to fit your real use cases
- **Mix and match skills** for document workflows
- **Read the skill documentation** in each subfolder for advanced patterns
- **Share your workflows** with your team by creating custom skills that wrap these building blocks

Happy document automation! 🚀
