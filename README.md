# Account Intelligence Radar

A Python research tool that generates structured company intelligence reports
for business outreach.

## Overview

This tool automates the process of discovering and extracting business intelligence
about companies from public web sources.

It combines:

- SERP discovery using SerpAPI
- LLM decision making for source selection
- Structured extraction using Firecrawl

The output is a structured intelligence report with evidence sources.

## Architecture

Pipeline:

Input (Company + Objective)
→ SERP Discovery
→ Source Selection (LLM)
→ Web Extraction (Firecrawl)
→ Data Fusion
→ Report Generation

## Setup

1. Clone the repository

2. Install dependencies : pip install -r requirements.txt

3. pip install -r requirements.txt

4. Create .env file look to env.example:
   SERPAPI_KEY=...
   FIRECRAWL_API_KEY=...
   GEMINI_API_KEY=...

## Run the tool

open any cmd on path of project then write : python main.py

Then provide:

Company name  
Objective prompt

Example:
Company: Apple
Objective:
Extract headquarters, business units, key executives and strategic initiatives.

## Output

Reports are generated as:

- JSON structured intelligence
- Human readable report

Saved inside:reports/

## Sample Reports

Included examples:

- Apple
- Misraj ai
