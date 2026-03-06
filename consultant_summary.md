# Account Intelligence Radar – Consultant Summary

## Problem

Business outreach often lacks structured intelligence about target companies.
Consultants spend significant time manually searching for company information
such as leadership, strategic initiatives, and industry positioning.

This project solves that problem by automating company research and generating
structured intelligence reports from public web sources.

## Solution

The system builds an automated pipeline that:

1. Discovers candidate sources using SerpAPI
2. Uses an LLM to select the most relevant sources
3. Extracts structured facts using Firecrawl
4. Merges results into a structured intelligence report

The output includes company identifiers, business units, leadership signals,
strategic initiatives, and evidence links.

## Architecture

Pipeline:

Input
→ SERP Discovery
→ LLM Source Selection
→ Firecrawl Extraction
→ Data Fusion
→ Report Generation

## Key Risks and Mitigation

API failures:
Handled using error checking and retry logic.

Hallucination risk:
All claims are linked to source URLs.

Missing data:
Fields return null when information cannot be verified.

## Future Improvements

- Geography mode for discovering companies by region
- I would integrate geographic filtering with the company analysis module. After retrieving companies from a specific region, each company would be passed to the company-status evaluation component to determine its suitability
- work more on output stratucer and report
