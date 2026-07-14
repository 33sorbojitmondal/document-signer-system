import base64
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed


def generate_rsa_key_pair():
    """Generate RSA-2048 key pair for digital signing."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_private_key(private_key):
    """Serialize private key to PEM string."""
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pem.decode('utf-8')


def serialize_public_key(public_key):
    """Serialize public key to PEM string."""
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem.decode('utf-8')


def load_private_key(pem_string):
    """Load private key from PEM string."""
    return serialization.load_pem_private_key(
        pem_string.encode('utf-8'),
        password=None,
        backend=default_backend(),
    )


def load_public_key(pem_string):
    """Load public key from PEM string."""
    return serialization.load_pem_public_key(
        pem_string.encode('utf-8'),
        backend=default_backend(),
    )


def compute_document_hash(file_content):
    """Compute SHA-256 hash of document content."""
    return hashlib.sha256(file_content).digest()


def sign_document(private_key_pem, file_content):
    """
    Sign document using RSA-PSS with SHA-256.
    Returns base64-encoded signature and document hash.
    """
    private_key = load_private_key(private_key_pem)
    document_hash = compute_document_hash(file_content)

    signature = private_key.sign(
        document_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        Prehashed(hashes.SHA256()),
    )

    return base64.b64encode(signature).decode('utf-8'), document_hash.hex()


def verify_document_signature(public_key_pem, file_content, signature_b64):
    """
    Verify document signature using RSA-PSS with SHA-256.
    Returns True if valid, False otherwise.
    """
    try:
        public_key = load_public_key(public_key_pem)
        document_hash = compute_document_hash(file_content)
        signature = base64.b64decode(signature_b64)

        public_key.verify(
            signature,
            document_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            Prehashed(hashes.SHA256()),
        )
        return True
    except Exception:
        return False
