
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
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── db/
│   │   ├── env/
│   │   ├── middlewear/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── __pycache__/
│   ├── Dockerfile
├── frontend/
│   └── qr-react-app/
│       ├── node_modules/
│       ├── public/
│       └── src/
│           ├── assets/
│           └── components/
├── mobile/
└── README.md
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

### Mobile

- The `mobile/` folder can be used for potential mobile app development (if needed).

## Installation

### Backend

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/qr-receipt-project.git
    cd qr-receipt-project/backend
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the PostgreSQL (Neon) database. Configure your connection details in the `.env` file or database settings.

4. Run the FastAPI backend:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend

1. Navigate to the frontend directory:
    ```bash
    cd qr-receipt-project/frontend/qr-react-app
    ```

2. Install the required dependencies:
    ```bash
    npm install
    ```

3. Start the Vite development server:
    ```bash
    npm run dev
    ```

### Database Setup

1. Set up your PostgreSQL (Neon) database and update the database credentials in your backend configuration.
2. Apply migrations (if using SQLAlchemy):
    ```bash
    alembic upgrade head
    ```

## Usage

1. **User Registration**:
    - Register a new user by providing an email and password. This will create a user in the system.

2. **Login**:
    - After registration, log in using your credentials. A JWT token will be issued for further authentication.

3. **Generate Receipt**:
    - Once logged in, you can generate a receipt by providing the necessary details (e.g., total amount, items).

4. **Scan QR Code**:
    - Each generated receipt will have a unique QR code. Scanning the code will redirect you to the corresponding PDF receipt.

## API Endpoints

- **POST /api/v1/register**: Register a new user.
- **POST /api/v1/login**: Log in and receive a JWT token.
- **POST /api/v1/receipts**: Generate a new receipt.
- **GET /api/v1/receipts/{receipt_id}**: Retrieve a receipt by its ID.
- **GET /api/v1/qr/{receipt_id}**: Retrieve the QR code for a receipt.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
