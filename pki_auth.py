import os
import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography import x509  # Import x509 module
from cryptography.hazmat.backends import default_backend

# Function to generate RSA key pair
def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Function to create a self-signed certificate
def generate_self_signed_cert(private_key, public_key):
    # Use NameAttribute to wrap the OID and the corresponding value
    subject = issuer = x509.Name([
        x509.NameAttribute(x509.NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(x509.NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "My Organization"),
        x509.NameAttribute(x509.NameOID.COMMON_NAME, "mydomain.com")
    ])
    
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(public_key).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).add_extension(x509.SubjectAlternativeName([x509.DNSName("mydomain.com")]), critical=False).sign(private_key, hashes.SHA256(), default_backend())
    return cert

# Saving certificate and key to files
def save_to_files(cert, private_key):
    with open("certificate.pem", "wb") as cert_file:
        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))
    
    with open("private_key.pem", "wb") as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

private_key, public_key = generate_rsa_keypair()
certificate = generate_self_signed_cert(private_key, public_key)
save_to_files(certificate, private_key)
