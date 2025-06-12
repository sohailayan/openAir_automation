# Playwright-Python-Framework

## Overview
Automates OpenAIR (Valtech) SSO login and timesheet submission using Playwright routed through MCP, with PyTest and Page Object Model (POM).

## Setup
1. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure MCP server is running and accessible.

## Running Tests
```bash
pytest Test/
```

## Project Structure
- `Pages/`: Page Object Model classes for login and timesheet pages
- `Test/`: Test cases and PyTest configuration

## Notes
- All browser automation is routed through the MCP server.
- Update credentials and selectors as needed for your environment. 