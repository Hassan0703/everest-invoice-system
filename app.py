"""
Everest Movers - Invoice Generator
Main Flask Application
"""

import os
import sqlite3
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'everest_movers_2024'

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'invoices.db')


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_db()
    cursor = conn.cursor()

    # Create invoices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT NOT NULL,
            invoice_date TEXT NOT NULL,
            due_date TEXT,
            bill_to_name TEXT,
            bill_to_address TEXT,
            bill_to_email TEXT,
            company_name TEXT DEFAULT 'EVEREST MOVERS CARGO PACKAGING LLC',
            company_address TEXT DEFAULT 'IT CANTER BUR DUBAI OFFICE NO 403, DUBAI UAE',
            company_phone TEXT DEFAULT '+92 3096882551',
            company_email TEXT DEFAULT 'support@eversemovers.com',
            tax_percent REAL DEFAULT 0,
            discount REAL DEFAULT 0,
            terms TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create invoice items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            item_date TEXT,
            job_no TEXT,
            client TEXT,
            description TEXT,
            location TEXT,
            crew TEXT,
            pick_drop_charges REAL DEFAULT 0,
            crew_amount REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized.")


def get_next_invoice_number():
    """Generate next invoice number."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM invoices")
    count = cursor.fetchone()['cnt']
    conn.close()
    year = datetime.now().year
    return f"INV-{year}-{str(count + 1).zfill(4)}"


@app.route('/')
def index():
    """Home - list all invoices."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices ORDER BY created_at DESC")
    invoices = cursor.fetchall()
    conn.close()
    return render_template('index.html', invoices=invoices)


@app.route('/create', methods=['GET'])
def create_invoice():
    """Show create invoice form."""
    invoice_number = get_next_invoice_number()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('create.html', invoice_number=invoice_number, today=today)


@app.route('/save', methods=['POST'])
def save_invoice():
    """Save invoice to database."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400

        # Validate required fields
        if not data.get('invoice_number'):
            return jsonify({'success': False, 'error': 'Invoice number is required'}), 400
        if not data.get('invoice_date'):
            return jsonify({'success': False, 'error': 'Invoice date is required'}), 400
        if not data.get('items') or len(data['items']) == 0:
            return jsonify({'success': False, 'error': 'At least one item is required'}), 400

        # Safe number parsing
        def safe_float(val, default=0):
            try:
                v = float(str(val).replace(',', '').strip())
                return max(0, v)  # No negatives
            except:
                return default

        tax_percent = safe_float(data.get('tax_percent', 0))
        discount = safe_float(data.get('discount', 0))

        conn = get_db()
        cursor = conn.cursor()

        # Insert invoice
        cursor.execute('''
            INSERT INTO invoices (
                invoice_number, invoice_date, due_date,
                bill_to_name, bill_to_address, bill_to_email,
                company_name, company_address, company_phone, company_email,
                tax_percent, discount, terms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('invoice_number'),
            data.get('invoice_date'),
            data.get('due_date', ''),
            data.get('bill_to_name', ''),
            data.get('bill_to_address', ''),
            data.get('bill_to_email', ''),
            data.get('company_name', 'EVEREST MOVERS CARGO PACKAGING LLC'),
            data.get('company_address', 'IT CANTER BUR DUBAI OFFICE NO 403, DUBAI UAE'),
            data.get('company_phone', '+92 3096882551'),
            data.get('company_email', 'support@eversemovers.com'),
            tax_percent,
            discount,
            data.get('terms', '')
        ))

        invoice_id = cursor.lastrowid

        # Insert items
        for item in data['items']:
            pick_drop = safe_float(item.get('pick_drop_charges', 0))
            crew_amt = safe_float(item.get('crew_amount', 0))
            total_amt = pick_drop + crew_amt  # Strict formula

            cursor.execute('''
                INSERT INTO invoice_items (
                    invoice_id, item_date, job_no, client, description,
                    location, crew, pick_drop_charges, crew_amount, total_amount
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                invoice_id,
                item.get('date', ''),
                item.get('job_no', ''),
                item.get('client', ''),
                item.get('description', ''),
                item.get('location', ''),
                item.get('crew', ''),
                pick_drop,
                crew_amt,
                total_amt
            ))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'invoice_id': invoice_id})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/invoice/<int:invoice_id>')
def view_invoice(invoice_id):
    """View/preview invoice."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
    invoice = cursor.fetchone()
    if not invoice:
        conn.close()
        return "Invoice not found", 404

    cursor.execute("SELECT * FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
    items = cursor.fetchall()
    conn.close()

    # Calculate totals
    subtotal = sum(item['total_amount'] for item in items)
    tax_amount = subtotal * (invoice['tax_percent'] / 100)
    total = subtotal + tax_amount - invoice['discount']

    return render_template('invoice.html',
                           invoice=invoice,
                           items=items,
                           subtotal=subtotal,
                           tax_amount=tax_amount,
                           total=total)


@app.route('/delete/<int:invoice_id>', methods=['POST'])
def delete_invoice(invoice_id):
    """Delete an invoice."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
        cursor.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    init_db()
    import webbrowser
    import threading

    def open_browser():
        import time
        time.sleep(1.2)
        webbrowser.open('http://127.0.0.1:5000')

    # Open browser automatically
    threading.Thread(target=open_browser, daemon=True).start()

    print("\n" + "="*50)
    print("  Everest Movers - Invoice Generator")
    print("  Running at: http://127.0.0.1:5000")
    print("  Press Ctrl+C to stop")
    print("="*50 + "\n")

    app.run(debug=False, port=5000, host='127.0.0.1')
