from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate

# Load the certificate and private key
def load_certificate_and_key(cert_path, key_path):
    with open(cert_path, "rb") as cert_file:
        certificate = load_pem_x509_certificate(cert_file.read())
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    return certificate, private_key

# Function to verify the certificate (simulate the client-server verification)
def verify_certificate(certificate):
    # For real-world usage, check the certificate chain or trust store
    # Here we're assuming it's self-signed for simplicity
    print("Certificate is valid (self-signed).")

# Function to authenticate user based on private key and certificate
def authenticate_user(certificate, private_key):
    print("Authenticating user...")
    # Generate a message to sign
    message = b"Hello, this is a challenge message."
    
    # The user signs the message with their private key
    signed_message = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    # The server (in a real system) would verify this signature using the user's public certificate
    try:
        certificate.public_key().verify(
            signed_message,
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("Authentication successful.")
    except Exception as e:
        print(f"Authentication failed: {e}")

if __name__ == "__main__":
    cert, private_key = load_certificate_and_key("certificate.pem", "private_key.pem")
    verify_certificate(cert)
    authenticate_user(cert, private_key)
