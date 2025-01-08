from pki_auth import generate_rsa_keypair, generate_self_signed_cert, save_to_files
from authenticate_with_cert import load_certificate_and_key, verify_certificate, authenticate_user
from tee_auth import use_tee_for_secure_operations

def authenticate_user_system():
    # Step 1: Load certificate and private key
    cert, private_key = load_certificate_and_key("certificate.pem", "private_key.pem")
    
    # Step 2: Verify certificate (for real-world cases, verify against a CA)
    verify_certificate(cert)
    
    # Step 3: Authenticate the user with the certificate
    authenticate_user(cert, private_key)
    
    # Step 4: Optionally use TEE for sensitive operations like signing
    use_tee_for_secure_operations()

if __name__ == "__main__":
    authenticate_user_system()
