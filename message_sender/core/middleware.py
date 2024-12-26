from cryptography.fernet import Fernet
import base64
import hashlib
import os
import json

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Generate or load encryption key
        self.key = self.get_or_create_key()
        self.fernet = Fernet(self.key)

    def get_or_create_key(self):
        # Try to get key from environment variable
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            # Generate a new key if none exists
            key = Fernet.generate_key()
            # Save the key
            os.environ['ENCRYPTION_KEY'] = key.decode()
            print(f"Generated new encryption key: {key.decode()}")
        elif isinstance(key, str):
            # Convert string key back to bytes
            key = key.encode()
            print(f"Using existing encryption key")
        return key

    def encrypt_message(self, message):
        """
        Encrypts a message using Fernet symmetric encryption
        Also creates a hash for integrity verification
        """
        if isinstance(message, str):
            message = message.encode()
        
        # Create a hash of the original message for integrity check
        message_hash = hashlib.sha256(message).hexdigest()
        
        # Encrypt the message
        encrypted_message = self.fernet.encrypt(message)
        
        # Combine encrypted message and hash
        combined = base64.b64encode(
            encrypted_message + b"||" + message_hash.encode()
        ).decode()
        
        return combined

    def decrypt_message(self, encrypted_data):
        """
        Decrypts a message and verifies its integrity
        """
        try:
            # Decode the combined data
            decoded = base64.b64decode(encrypted_data.encode())
            encrypted_message, received_hash = decoded.split(b"||")
            
            # Decrypt the message
            decrypted_message = self.fernet.decrypt(encrypted_message)
            
            # Verify integrity
            calculated_hash = hashlib.sha256(decrypted_message).hexdigest().encode()
            if calculated_hash != received_hash:
                raise ValueError("Message integrity check failed")
            
            return decrypted_message.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def process_response(self, request, response):
        if hasattr(response, 'content'):
            try:
                # Only encrypt if it's a JSON response
                content = json.loads(response.content.decode('utf-8'))
                if isinstance(content, dict) and 'message' in content:
                    content['message'] = self.encrypt_message(content['message'])
                    response.content = json.dumps(content).encode('utf-8')
            except:
                pass
        return response

    def __call__(self, request):
        response = self.get_response(request)
        return response
