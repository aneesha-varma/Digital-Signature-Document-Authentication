<<<<<<< HEAD
# Digital Signature-Based Document Authentication System

## Project Overview

The Digital Signature-Based Document Authentication System is a Python application designed to verify document authenticity and integrity using RSA digital signatures and SHA-256 hashing.

The application allows users to sign documents, download signature records, and verify whether a document has been modified after signing.

## Objectives

- Generate RSA public and private key pairs.
- Calculate SHA-256 document hashes.
- Digitally sign documents using RSA-PSS.
- Verify signatures using the corresponding public key.
- Detect document modification through hash comparison and signature verification.
- Provide a simple interface using Streamlit.

## Technologies Used

- **Programming Language:** Python
- **Frontend:** Streamlit
- **Cryptographic Algorithm:** RSA-PSS
- **Hashing Algorithm:** SHA-256
- **Library:** Python Cryptography
- **Version Control:** Git and GitHub

## Project Structure

```text
Digital-Signature-Document-Authentication/
├── app.py
├── crypto_utils.py
├── requirements.txt
├── README.md
├── .gitignore
├── keys/
│   └── .gitkeep
├── uploads/
│   └── .gitkeep
└── signatures/
    └── .gitkeep
```

## Prerequisites

- Python 3.10 or newer
- Visual Studio Code
- Git

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Digital-Signature-Document-Authentication.git
cd Digital-Signature-Document-Authentication
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## How to Use

1. Open the application.
2. Click **Generate RSA Key Pair**.
3. Download the public key and keep the private key secure.
4. Open the Sign Document tab.
5. Upload a test document and click **Sign Document**.
6. Download the signature record.
7. Open the Verify Document tab.
8. Upload the document, its signature record, and the signer's public key.
9. Click **Verify Authenticity** to view the result.

## Testing

### Test 1: Valid Document

Sign a file and verify it without modifying its contents.

**Expected result:** Verification successful.

### Test 2: Tampered Document

Modify the contents of the signed file and verify it using the original signature record and public key.

**Expected result:** Verification failed; document hash mismatch.

### Test 3: Incorrect Public Key

Try verifying a document using a different public key.

**Expected result:** Verification failed.

### Test 4: Invalid Signature Record

Modify or corrupt the signature record.

**Expected result:** Verification failed.

## Security Considerations

- Never publish or share the private key.
- The demonstration stores its private key without password protection.
- A valid signature confirms integrity and verification under a particular public key; identity verification requires a trusted association between the signer and that key.
- The project is intended for educational use and is not a production document-signing service.

## Future Enhancements

- Password-protected private keys.
- User login and role-based access.
- A trusted certificate authority and digital certificates.
- PDF-specific signature support.
- Document signing history and audit logs.
- Secure storage and deployment.

## Author

Aneesha Varma.

## License

This project is available for educational purposes.
=======
# Digital-Signature-Document-Authentication
A Python-based document authentication system using RSA digital signatures and SHA-256 hashing to verify document integrity and detect tampering.
>>>>>>> 6d1c76b32699d64a91a86e261101962f96f152e8
