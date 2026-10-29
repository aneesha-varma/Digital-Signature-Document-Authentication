import base64
import hashlib
import json
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


KEY_DIR = Path("keys")
KEY_DIR.mkdir(exist_ok=True)


def generate_key_pair():
    """Generate and save an RSA private/public key pair."""

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    (KEY_DIR / "private_key.pem").write_bytes(private_pem)
    (KEY_DIR / "public_key.pem").write_bytes(public_pem)

    return public_pem


def load_private_key():
    path = KEY_DIR / "private_key.pem"

    if not path.exists():
        raise FileNotFoundError(
            "Generate a key pair before signing a document."
        )

    return serialization.load_pem_private_key(
        path.read_bytes(),
        password=None
    )


def calculate_hash(document_bytes):
    """Calculate the SHA-256 hash of the original document."""

    return hashlib.sha256(document_bytes).hexdigest()


def sign_document(document_bytes, filename):
    """Sign the original document and create a signature record."""

    private_key = load_private_key()

    signature = private_key.sign(
        document_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    record = {
        "filename": filename,
        "algorithm": "RSA-PSS with SHA-256",
        "sha256": calculate_hash(document_bytes),
        "signature": base64.b64encode(signature).decode("ascii")
    }

    return json.dumps(record, indent=4).encode("utf-8")


def verify_document(document_bytes, record_bytes, public_pem):
    """Check both the document hash and its digital signature."""

    try:
        record = json.loads(record_bytes.decode("utf-8"))

        if record.get("algorithm") != "RSA-PSS with SHA-256":
            return False, "Unsupported signature algorithm."

        current_hash = calculate_hash(document_bytes)

        if current_hash != record.get("sha256"):
            return False, "Document hash mismatch. Tampering detected."

        public_key = serialization.load_pem_public_key(public_pem)

        signature = base64.b64decode(
            record["signature"],
            validate=True
        )

        public_key.verify(
            signature,
            document_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True, "Document is authentic and its signature is valid."

    except InvalidSignature:
        return False, "Invalid signature. The document or signature is not authentic."

    except (ValueError, TypeError, KeyError, UnicodeDecodeError):
        return False, "Invalid signature record, public key, or file format."

    except json.JSONDecodeError:
        return False, "The signature record is not valid JSON."