import os
from cryptography.fernet import Fernet

class FileEncryptor:
    @staticmethod
    def generate_and_save_key(key_path="secret.key"):
        """
        Generates an AES-based secure key and saves it to a file.
        """
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        print(f"Key generated and securely stored at: {key_path}")

    @staticmethod
    def load_key(key_path="secret.key"):
        """
        Loads the saved secret cryptographic key from disk.
        """
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"Cryptographic key file '{key_path}' missing.")
        with open(key_path, "rb") as key_file:
            return key_file.read()

    def encrypt_file(self, target_file_path, key_path="secret.key"):
        """
        Encrypts a target file using the loaded secret key.
        """
        try:
            key = self.load_key(key_path)
            fernet = Fernet(key)

            with open(target_file_path, "rb") as file_to_encrypt:
                raw_data = file_to_encrypt.read()

            # Scramble data stream via Fernet symmetric token encryption
            encrypted_data = fernet.encrypt(raw_data)

            with open(target_file_path, "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)

            print(f"Success: Content inside '{target_file_path}' has been encrypted.")
        except Exception as e:
            print(f"Encryption Routine Failure: {e}")

    def decrypt_file(self, target_file_path, key_path="secret.key"):
        """
        Decrypts an encrypted target file back into its raw layout.
        """
        try:
            key = self.load_key(key_path)
            fernet = Fernet(key)

            with open(target_file_path, "rb") as encrypted_file:
                cipher_data = encrypted_file.read()

            # Reverse the scrambling routine back into plain text binary representation
            decrypted_data = fernet.decrypt(cipher_data)

            with open(target_file_path, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)

            print(f"Success: Content inside '{target_file_path}' has been decrypted back to original.")
        except Exception as e:
            print(f"Decryption Routine Failure: {e}")

if __name__ == "__main__":
    print("Symmetric Cryptographic File Protection Engine")
    print("-" * 50)

    engine = FileEncryptor()
    target_doc = "confidential_notes.txt"
    key_file = "secret.key"

    # 1. Setup sample document for execution demo
    if not os.path.exists(target_doc):
        with open(target_doc, "w", encoding="utf-8") as f:
            f.write("CONFIDENTIAL DATA: System architecture credentials = Admin123\n")
        print(f"Created sample text baseline data file: {target_doc}")

    # 2. Setup key file configuration validation boundaries
    if not os.path.exists(key_file):
        engine.generate_and_save_key(key_file)

    print("-" * 50)
    print("Current Plain Text Inside File:")
    with open(target_doc, "r", encoding="utf-8") as f:
        print(f"➔ {f.read().strip()}")
    print("-" * 50)

    # 3. Trigger Encryption Simulation
    input("Press Enter to execute file ENCRYPTION routing...")
    engine.encrypt_file(target_doc, key_file)
    
    print("\nFile State Post-Encryption (Raw Binaries Scrambled):")
    with open(target_doc, "rb") as f:
        print(f"➔ {f.read()[:60]}... [Truncated]")
    print("-" * 50)

    # 4. Trigger Decryption Simulation
    input("Press Enter to execute file DECRYPTION restoration routing...")
    engine.decrypt_file(target_doc, key_file)

    print("\nFile State Post-Decryption (Restored Plain Text Layout):")
    with open(target_doc, "r", encoding="utf-8") as f:
        print(f"➔ {f.read().strip()}")
    print("-" * 50)
  
