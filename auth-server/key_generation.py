from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

PRIVATE_KEY_PATH = Path("/app/keys/private.pem")
PUBLIC_KEY_PATH = Path("/app/game-keys/public.pem")


def generate_keys_if_missing():
    # If both keys already exist, do nothing.
    if PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists():
        print("RSA keys already exist. Keeping existing keys.")
        return

    # Don't silently create a mismatched key pair.
    if PRIVATE_KEY_PATH.exists() or PUBLIC_KEY_PATH.exists():
        raise RuntimeError(
            "Only one RSA key exists. Both keys must be present or absent."
        )

    print("Generating new RSA key pair...")

    # Generate a 2048-bit RSA private key.
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Get the matching public key.
    public_key = private_key.public_key()

    # Convert private key to PEM format.
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Convert public key to PEM format.
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Save both keys.
    PRIVATE_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)

    PRIVATE_KEY_PATH.write_bytes(private_pem)
    PRIVATE_KEY_PATH.chmod(0o600)

    PUBLIC_KEY_PATH.write_bytes(public_pem)

    print("RSA key pair successfully generated.")
    
#if only one file exists, the code stops rather than generating a potentially mismatched pair.