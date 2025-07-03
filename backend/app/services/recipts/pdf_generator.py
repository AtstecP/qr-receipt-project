from pdfkit import from_string
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session

import os

from app.services.utils import get_company_name
from app.models.receipt import Receipt

data = {
  'receipt_id': 20250619,
  'user_id': 98327,
  'timestamp': '2025-06-19T14:30:45Z',
  'company_name': 'QuickFix Tech Solutions',
  'total': 154.75,
  'items_json': [
    {
      'name': 'USB-C Charger',
      'quantity': 1,
      'price': 34.99
    },
    {
      'name': 'Wireless Mouse',
      'quantity': 2,
      'price': 29.88
    },
    {
      'name': 'Laptop Stand',
      'quantity': 1,
      'price': 59.00
    }
  ]
}

def model_to_dict(obj):
    return {
        column.name: getattr(obj, column.name)
        for column in obj.__table__.columns
    }

def generate_receipt_pdf(db: Session, recipt_id: str):
  cwd = os.getcwd()
  file_path = os.path.join(
        cwd,
        'app',
        'services',
        'recipts',
        'temporary_files',
        f'{recipt_id}.pdf'
    )
  if os.path.exists(file_path):
    return file_path
  template_path = os.path.join(
      cwd,
      'app',
      'services',
      'recipts',
      'jinja_templates'
  )
  env = Environment(loader=FileSystemLoader(template_path))
  template = env.get_template('receipt.html') 
  receipt = db.query(Receipt).filter(Receipt.receipt_id == recipt_id).first()
  receipt_data = model_to_dict(receipt) + {'company_name' : get_company_name(db, receipt.user_id)}
  print(receipt_data)
  html = template.render(dict(receipt_data))
  content = from_string(html)
  try:
      with open(file_path, 'wb+') as file:
          file.write(content)

  except Exception as error:
      raise error(f'Error saving file to disc. Error: {error}')

  return file_path

if __name__=='__main__':
    print(generate_receipt_pdf())


