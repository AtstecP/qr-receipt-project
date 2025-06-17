import pdfkit
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings

def generate_receipt_pdf(receipt_data: dict, business_info: dict) -> str:
    # Calculate totals
    subtotal = sum(item['price'] * item['quantity'] for item in receipt_data['items'])
    hst = subtotal * 0.13
    total = subtotal + hst
    
    # Render HTML template
    env = Environment(loader=FileSystemLoader('app/templates'))
    template = env.get_template("receipt.html")
    html = template.render(
        receipt=receipt_data,
        business=business_info,
        subtotal=subtotal,
        hst=hst,
        total=total
    )
    
    # Generate PDF
    options = {
        'encoding': 'UTF-8',
        'quiet': ''
    }
    pdf_path = f"receipts/{receipt_data['id']}.pdf"
    pdfkit.from_string(html, pdf_path, options=options)
    
    return pdf_path