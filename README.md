
# QR Receipt Generator

A web application that generates receipts and provides them via QR code. Users can scan the QR code to access a PDF receipt, which is dynamically generated on the backend. This project combines backend APIs, frontend interfaces, and QR code generation to streamline receipt management.

## Features

- **User Registration & Authentication**: Users can register, log in, and authenticate via JWT tokens.
- **QR Code Generation**: QR codes are generated for each receipt, which link to a dynamically created PDF file containing the receipt details.
- **Receipt Management**: Users can view and download their receipts in PDF format.
- **Backend & Frontend**: A FastAPI-based backend with a React frontend using Vite for fast development.

## Technologies Used

- **Frontend**: React, Vite, TailwindCSS
- **Backend**: FastAPI, SQLAlchemy, JWT for authentication
- **Database**: PostgreSQL (Neon)
- **QR Code Generation**: Python libraries like `qrcode`
- **PDF Generation**: Python libraries like `ReportLab` or `pdfkit`
- **Authentication**: JWT (JSON Web Tokens)
- **Deployment**: Docker (optional for easy deployment)

## Project Structure

```
├─ backend/
│ ├─ app/
│ │ ├─ api/v1/endpoints/ # REST endpoints (auth, receipts, stats)
│ │ ├─ core/ # config, security, settings
│ │ ├─ db/ # session, base
│ │ ├─ middlewear/ 
│ │ ├─ models/ # SQLAlchemy models
│ │ ├─ schemas/ # Pydantic schemas
│ │ ├─ services/
│ │ │ └─ recipts/ 
│ │ │ ├─ jinja_templates/ # HTML -> PDF templates
│ │ │ └─ temporary_files/ # temp artifacts (PDF/QR)
│ └─ env/ # Python venv (local only)
├─ frontend/
│ └─ qr-react-app/
│ ├─ src/ # components, panels, lib/api.js
│ ├─ public/
│ └─ dist/ # build output
└─ mobile/ # (reserved for future)
```

### Backend

- The backend is built using **FastAPI**, providing APIs for user authentication, receipt creation, and receipt PDF generation.
- Receipts are stored in a **PostgreSQL (Neon)** database, and a QR code is linked to each receipt.
- The backend handles **JWT** authentication for user security.
- The backend directory includes `app/api/v1/endpoints` for API routes, `app/core` for core configurations, `app/db` for database connections, and `app/services` for business logic.

### Frontend

- The frontend is built with **React** and **Vite**, offering a fast development experience.
- Users can register, log in, and view their receipts with associated QR codes.
- The frontend is located in the `frontend/qr-react-app` directory.
- It uses **TailwindCSS** for styling and **Vite** for fast build and hot-reload capabilities.

