# Everest Movers Invoice System
**Cargo Packaging L.L.C**

## Short Description (what problem it solves)
Everest Movers Invoice System is a **desktop invoice generator** that runs locally on your computer and produces **clean, professional invoices** with **print-ready A4 output**. It is designed for teams who want a simple, reliable way to create invoices—without online tools, complex software, or technical setup.

## Key Features (bullet points)
- **Desktop-friendly**: packaged as an executable for Windows, macOS, and Linux
- **Simple user interface**: built for non-technical users
- **Manual invoice entry**: enter customer and invoice details in a straightforward form
- **Multiple item rows**: add as many line items as needed
- **Save invoices locally**: keep records on your machine (no internet required)
- **Instant preview**: review the final layout before printing
- **High-quality print output**: stable layout optimized to match the reference invoice design
- **Print and PDF export**: print directly or download as PDF using the browser print dialog

## Screenshots Section
![App Screenshot](./assets/screenshot.png)

Screenshots for this project are stored in **`static/screenshot/`**. Replace the image above with your own screenshot file (or update the path) to show the latest UI.

## How It Works (step-by-step flow)
1. **Launch the app** by running the desktop executable.
2. The app opens in your **default browser** (the system runs locally on your machine).
3. Click **New Invoice** to start an invoice.
4. Enter invoice information (customer details, invoice number/date, etc.).
5. Add **item rows** (description, quantity, rate, totals).
6. Click **Save** to store the invoice locally.
7. Open **Preview** to verify the final print layout.
8. Use **Print / Save as PDF** to print or download a PDF.

## Installation Guide (for non-technical users)
### Step 1: Run the executable
- **Windows**: double-click the `.exe` file.
- **macOS**: open the `.app` (if Gatekeeper shows a warning, open via **Right click → Open**).
- **Linux**: run the binary (you may need to mark it executable).

### Step 2: Open in your browser
- The app will open automatically in your default browser.
- If it does not open, use the address shown in the app window (commonly `http://127.0.0.1:5000`).

### Step 3: Start using
- No login and no online setup.
- Your invoices are stored **locally** on your computer.

## Usage Guide
### Create an invoice
- Click **New Invoice**.
- Fill in the required invoice and customer fields.

### Add rows (line items)
- Use **Add Row** (or the equivalent button) to insert additional item lines.
- Enter item description, quantity, unit price, and any other required fields.

### Save
- Click **Save Invoice** to store the invoice in the local database.

### Preview
- Open **Preview** to confirm spacing, alignment, totals, and overall layout.

### Print / Download PDF
- Click **Print / Save PDF**.
- In the print dialog:
  - Choose **A4**
  - Use **Portrait**
  - For PDF: select **Save as PDF** as the destination

## Project Structure (simple explanation of folders)
- **`app.py`**: application entry point (starts the local server)
- **`templates/`**: HTML pages used by the app (UI and print layout)
- **`static/`**: static assets such as CSS, images, and screenshots (including `static/screenshot/`)
- **`invoices.db`**: local SQLite database file created on first run (stores saved invoices)
- **`requirements.txt`**: Python dependencies (for developers/build process)
- **`*.spec`**: PyInstaller build configuration (used to package the desktop executable)

## Tech Stack
- **Flask**: local web application framework
- **SQLite**: local database for invoice storage
- **HTML/CSS**: user interface and print layout
- **PyInstaller**: packaging into a desktop executable

## Print & PDF System
This system is built with print quality as a first priority.
- **Optimized for A4 printing**: designed to print cleanly on A4, portrait orientation
- **Stable layout**: spacing and alignment are structured for consistent results across printers
- **Professional output**: the preview reflects the final print/PDF layout so you can confirm before printing

## Configuration (optional basic edits like company name)
Basic branding and wording can be adjusted if needed.
- **Company name / tagline**: update the values shown in the invoice header within the template files in `templates/`.
- **Logo and visuals**: replace image assets in `static/` (if your invoice design includes a logo).

After changes, re-run the executable (or rebuild the desktop package if you are distributing a new version).

## Known Limitations (keep minimal and professional)
- **Local-only**: invoices are stored on the same computer where the app is used.
- **PDF generation uses the browser print engine**: final PDF output depends on the browser’s print settings (A4/portrait recommended).

## Future Improvements (optional)
- Search and filters for saved invoices
- Export/backup tools for invoice data
- Optional template switching for different invoice formats

## License (simple placeholder)
All rights reserved. License terms to be defined.
