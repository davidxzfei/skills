# Deploying Document Skills to Claude Code

## Overview
The document skills in this repository (`docx`, `pdf`, `pptx`, `xlsx`) can be loaded into Claude Code to give the IDE rich document authoring and editing capabilities. This guide walks through installing the `document-skills` plugin bundle in Claude Code and offers ten ready-to-run demo prompts that showcase how each skill works.

## Prerequisites
- Access to Claude Code with plugin support enabled
- A Claude Code chat or notebook session where you can run `/plugin` commands
- Internet access so Claude Code can pull this GitHub repository

## Install from the Claude Code Plugin Marketplace (Recommended)
1. **Add the Anthropic skills marketplace once**
   ```
   /plugin marketplace add anthropics/skills
   ```
2. **Open the plugin picker** in Claude Code and choose **Browse and install plugins**.
3. Select **anthropic-agent-skills**.
4. Choose **document-skills** and press **Install now**.
5. Verify the install with:
   ```
   /plugin list
   ```
   You should see `document-skills@anthropic-agent-skills` listed.

You can also install the bundle directly from chat:
```
/plugin install document-skills@anthropic-agent-skills
```

## Using the document skills inside Claude Code
- Once installed, simply reference the skill in your instruction. Claude will automatically summon it when the task matches the skill’s description.
- Example phrasing: “Use the **docx** skill to create a project proposal from these notes.”
- For repeat work, pin the plugin in the Claude Code sidebar so you can toggle it on for any session.
- To check which skills are active in the current conversation, run `/plugin status`.

## Updating or removing the plugin
- **Update** to the latest version:
  ```
  /plugin update document-skills@anthropic-agent-skills
  ```
- **Remove** if no longer needed:
  ```
  /plugin uninstall document-skills@anthropic-agent-skills
  ```

## Ten demo prompts to showcase the document skills
Use these prompts inside Claude Code after enabling the plugin. Swap file paths with documents in your workspace as needed.

| # | Skill | Demo Prompt | What it Exercises |
|---|-------|-------------|-------------------|
| 1 | docx | “Use the docx skill to draft a 2-page consulting proposal in my `/docs/client_brief.txt` notes, and export it as `proposal.docx` using the docx-js workflow.” | Generating a new Word document from scratch |
| 2 | docx | “Using the docx skill, open `contracts/master_agreement.docx`, track every change that updates the renewal term to 24 months, and save the reviewed copy.” | Tracked changes & precise redlining |
| 3 | docx | “Convert `reports/q1_summary.docx` into page images using the docx skill so I can review the layout visually.” | DOCX → PDF → JPEG conversion workflow |
| 4 | pdf | “With the pdf skill, extract all tables from `finance/earnings_call.pdf` into CSV snippets so I can paste them into a spreadsheet.” | Table extraction via pdfplumber |
| 5 | pdf | “Fill the onboarding form `hr/new_hire_form.pdf` using the pdf skill with the data in `hr/new_hire.json`, and flatten the result.” | Form filling and flattening |
| 6 | pdf | “Split `legal/appendix_bundle.pdf` into one file per appendix using the pdf skill.” | Splitting PDFs with pypdf |
| 7 | pptx | “Leverage the pptx skill to build a 6-slide pitch deck summarizing `notes/startup_pitch.md`, applying a teal and coral palette.” | Creating new presentations via html2pptx |
| 8 | pptx | “Open `slides/quarterly_review.pptx` with the pptx skill, add speaker notes for each slide, and export the updated deck.” | Editing PPTX speaker notes |
| 9 | xlsx | “Use the xlsx skill to construct a KPI dashboard in `spreadsheets/kpi_tracker.xlsx`, complete with formulas for MoM growth and conditional formatting.” | Building structured spreadsheets |
| 10 | xlsx | “Clean and normalize the CSV at `data/sales_pipeline.csv`, loading it into `analysis/pipeline_review.xlsx` with pivot tables using the xlsx skill.” | Data cleaning and analysis with spreadsheets |

Tip: After each run, ask Claude to describe the steps it took. This helps you understand how the skill interprets your request and which internal scripts it uses.
