from pdfkit import from_string
from jinja2 import Environment, FileSystemLoader



data = {
  "receipt_id": 20250619,
  "user_id": 98327,
  "timestamp": "2025-06-19T14:30:45Z",
  "company_name": "QuickFix Tech Solutions",
  "total": 154.75,
  "items_json": [
    {
      "name": "USB-C Charger",
      "quantity": 1,
      "price": 34.99
    },
    {
      "name": "Wireless Mouse",
      "quantity": 2,
      "price": 29.88
    },
    {
      "name": "Laptop Stand",
      "quantity": 1,
      "price": 59.00
    }
  ]
}


def generate_receipt_pdf():
    env = Environment(loader=FileSystemLoader('jinja_templates'))
    template = env.get_template("receipt.html")
    html = template.render(**data)


    content = from_string(html)
    try:
        with open('your_pdf_file_here.pdf', 'wb+') as file:
            file.write(content)

    except Exception as error:
        raise error(f'Error saving file to disc. Error: {error}')

    return content

if __name__=="__main__":
    print(generate_receipt_pdf())


