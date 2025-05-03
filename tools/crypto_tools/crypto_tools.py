import os
import sys
import time
import base64
import hashlib
import binascii
import random
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from colorama import init, Fore, Style

from tools.ascii_generator import generate_category_ascii, clear_screen, spinner_animation, typing_animation, display_system_info

init(autoreset=True)

def generate_random_password(length=16, include_special=True):
    print(f"\n{Fore.YELLOW}[*] Generating random password...{Style.RESET_ALL}")
    
    if length < 8:
        print(f"{Fore.RED}[-] Password length should be at least 8 characters. Setting to 8.{Style.RESET_ALL}")
        length = 8
    
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = string.punctuation if include_special else ""
    
    all_chars = lowercase + uppercase + digits + special
    
    # Ensure at least one character from each category
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits)
    ]
    
    if include_special:
        password.append(random.choice(special))
    
    # Fill the rest of the password
    password.extend(random.choice(all_chars) for _ in range(length - len(password)))
    
    # Shuffle the password
    random.shuffle(password)
    password = ''.join(password)
    
    print(f"{Fore.GREEN}[+] Generated password: {password}{Style.RESET_ALL}")
    
    # Calculate password strength
    strength = 0
    if any(c in lowercase for c in password):
        strength += 1
    if any(c in uppercase for c in password):
        strength += 1
    if any(c in digits for c in password):
        strength += 1
    if include_special and any(c in special for c in password):
        strength += 1
    
    strength_text = ""
    if strength == 1:
        strength_text = f"{Fore.RED}Weak{Style.RESET_ALL}"
    elif strength == 2:
        strength_text = f"{Fore.YELLOW}Moderate{Style.RESET_ALL}"
    elif strength == 3:
        strength_text = f"{Fore.GREEN}Strong{Style.RESET_ALL}"
    elif strength == 4:
        strength_text = f"{Fore.CYAN}Very Strong{Style.RESET_ALL}"
    
    print(f"{Fore.CYAN}Password Strength: {strength_text}")
    print(f"{Fore.CYAN}Length: {Style.RESET_ALL}{length} characters")
    
    return password

def hash_text(text, algorithm="sha256"):
    print(f"\n{Fore.YELLOW}[*] Hashing text using {algorithm}...{Style.RESET_ALL}")
    
    algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha224": hashlib.sha224,
        "sha256": hashlib.sha256,
        "sha384": hashlib.sha384,
        "sha512": hashlib.sha512,
        "blake2b": hashlib.blake2b,
        "blake2s": hashlib.blake2s
    }
    
    if algorithm not in algorithms:
        print(f"{Fore.RED}[-] Invalid algorithm. Using SHA-256 instead.{Style.RESET_ALL}")
        algorithm = "sha256"
    
    try:
        hash_obj = algorithms[algorithm](text.encode())
        hash_hex = hash_obj.hexdigest()
        
        print(f"{Fore.GREEN}[+] {algorithm.upper()} Hash: {hash_hex}{Style.RESET_ALL}")
        return hash_hex
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error hashing text: {str(e)}{Style.RESET_ALL}")
        return None

def encrypt_text(text, password):
    print(f"\n{Fore.YELLOW}[*] Encrypting text...{Style.RESET_ALL}")
    
    try:
        # Generate a key from the password
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        # Encrypt the text
        f = Fernet(key)
        encrypted_text = f.encrypt(text.encode())
        
        # Combine salt and encrypted text
        result = base64.urlsafe_b64encode(salt + encrypted_text)
        
        print(f"{Fore.GREEN}[+] Text encrypted successfully!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Encrypted Text: {Style.RESET_ALL}{result.decode()}")
        
        return result.decode()
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error encrypting text: {str(e)}{Style.RESET_ALL}")
        return None

def decrypt_text(encrypted_text, password):
    print(f"\n{Fore.YELLOW}[*] Decrypting text...{Style.RESET_ALL}")
    
    try:
        # Decode the combined salt and encrypted text
        decoded = base64.urlsafe_b64decode(encrypted_text)
        salt = decoded[:16]
        encrypted_data = decoded[16:]
        
        # Regenerate the key from the password and salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        # Decrypt the text
        f = Fernet(key)
        decrypted_text = f.decrypt(encrypted_data).decode()
        
        print(f"{Fore.GREEN}[+] Text decrypted successfully!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Decrypted Text: {Style.RESET_ALL}{decrypted_text}")
        
        return decrypted_text
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error decrypting text: {str(e)}{Style.RESET_ALL}")
        return None

def generate_rsa_keys(key_size=2048):
    print(f"\n{Fore.YELLOW}[*] Generating RSA key pair ({key_size} bits)...{Style.RESET_ALL}")
    
    try:
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        
        # Get public key
        public_key = private_key.public_key()
        
        # Serialize private key to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        
        # Serialize public key to PEM format
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        
        print(f"{Fore.GREEN}[+] RSA key pair generated successfully!{Style.RESET_ALL}")
        
        # Save keys to files
        save = input(f"\n{Fore.CYAN}Save keys to files? (y/n): {Style.RESET_ALL}").lower()
        if save == 'y':
            with open("private_key.pem", "w") as f:
                f.write(private_pem)
            
            with open("public_key.pem", "w") as f:
                f.write(public_pem)
            
            print(f"{Fore.GREEN}[+] Keys saved to private_key.pem and public_key.pem{Style.RESET_ALL}")
        
        return private_pem, public_pem
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error generating RSA keys: {str(e)}{Style.RESET_ALL}")
        return None, None

def rsa_encrypt_text(text, public_key_pem):
    print(f"\n{Fore.YELLOW}[*] Encrypting text with RSA public key...{Style.RESET_ALL}")
    
    try:
        # Load public key
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        
        # Encrypt the text
        encrypted = public_key.encrypt(
            text.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Encode to base64 for easier handling
        encrypted_b64 = base64.b64encode(encrypted).decode()
        
        print(f"{Fore.GREEN}[+] Text encrypted successfully with RSA!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Encrypted Text (Base64): {Style.RESET_ALL}{encrypted_b64}")
        
        return encrypted_b64
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error encrypting with RSA: {str(e)}{Style.RESET_ALL}")
        return None

def rsa_decrypt_text(encrypted_text_b64, private_key_pem):
    print(f"\n{Fore.YELLOW}[*] Decrypting text with RSA private key...{Style.RESET_ALL}")
    
    try:
        # Decode from base64
        encrypted = base64.b64decode(encrypted_text_b64)
        
        # Load private key
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None
        )
        
        # Decrypt the text
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()
        
        print(f"{Fore.GREEN}[+] Text decrypted successfully with RSA!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Decrypted Text: {Style.RESET_ALL}{decrypted}")
        
        return decrypted
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error decrypting with RSA: {str(e)}{Style.RESET_ALL}")
        return None

def encode_decode_base64():
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║           BASE64 ENCODE/DECODE           ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Encode text to Base64")
    print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Decode Base64 to text")
    
    choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")
    
    if choice == "1":
        text = input(f"\n{Fore.CYAN}Enter text to encode: {Style.RESET_ALL}")
        
        try:
            encoded = base64.b64encode(text.encode()).decode()
            print(f"\n{Fore.GREEN}[+] Base64 Encoded: {encoded}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error encoding to Base64: {str(e)}{Style.RESET_ALL}")
    
    elif choice == "2":
        text = input(f"\n{Fore.CYAN}Enter Base64 to decode: {Style.RESET_ALL}")
        
        try:
            decoded = base64.b64decode(text).decode()
            print(f"\n{Fore.GREEN}[+] Decoded Text: {decoded}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error decoding Base64: {str(e)}{Style.RESET_ALL}")
    
    else:
        print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")

def crypto_tools_menu():
    while True:
        clear_screen()
        print(generate_category_ascii("CRYPTO TOOLS"))
        display_system_info()
        
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║          CRYPTOGRAPHY TOOLS MENU         ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Generate Random Password")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Hash Text")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Encrypt/Decrypt Text (Symmetric)")
        print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Generate RSA Key Pair")
        print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Encrypt/Decrypt with RSA (Asymmetric)")
        print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Base64 Encode/Decode")
        print(f"{Fore.CYAN}[7]{Style.RESET_ALL} Back to Main Menu")
        
        choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")
        
        if choice == "1":
            length = input(f"\n{Fore.CYAN}Enter password length (default: 16): {Style.RESET_ALL}")
            if not length.isdigit():
                length = 16
            else:
                length = int(length)
            
            include_special = input(f"{Fore.CYAN}Include special characters? (y/n, default: y): {Style.RESET_ALL}").lower() != 'n'
            
            generate_random_password(length, include_special)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "2":
            text = input(f"\n{Fore.CYAN}Enter text to hash: {Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}Available hash algorithms:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[1]{Style.RESET_ALL} MD5 (Not secure for passwords)")
            print(f"{Fore.CYAN}[2]{Style.RESET_ALL} SHA-1 (Not secure for passwords)")
            print(f"{Fore.CYAN}[3]{Style.RESET_ALL} SHA-256 (Recommended)")
            print(f"{Fore.CYAN}[4]{Style.RESET_ALL} SHA-512")
            print(f"{Fore.CYAN}[5]{Style.RESET_ALL} BLAKE2b")
            
            algo_choice = input(f"\n{Fore.CYAN}Select algorithm (default: 3): {Style.RESET_ALL}")
            
            algorithm = "sha256"
            if algo_choice == "1":
                algorithm = "md5"
            elif algo_choice == "2":
                algorithm = "sha1"
            elif algo_choice == "4":
                algorithm = "sha512"
            elif algo_choice == "5":
                algorithm = "blake2b"
            
            hash_text(text, algorithm)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "3":
            print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║        SYMMETRIC ENCRYPTION MENU         ║{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
            
            print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Encrypt Text")
            print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Decrypt Text")
            
            encrypt_choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")
            
            if encrypt_choice == "1":
                text = input(f"\n{Fore.CYAN}Enter text to encrypt: {Style.RESET_ALL}")
                password = input(f"{Fore.CYAN}Enter encryption password: {Style.RESET_ALL}")
                
                encrypted = encrypt_text(text, password)
                if encrypted:
                    save = input(f"\n{Fore.CYAN}Save encrypted text to file? (y/n): {Style.RESET_ALL}").lower()
                    if save == 'y':
                        filename = input(f"{Fore.CYAN}Enter filename (default: encrypted.txt): {Style.RESET_ALL}")
                        if not filename:
                            filename = "encrypted.txt"
                        
                        with open(filename, 'w') as f:
                            f.write(encrypted)
                        
                        print(f"{Fore.GREEN}[+] Encrypted text saved to {filename}{Style.RESET_ALL}")
            
            elif encrypt_choice == "2":
                encrypted_text = input(f"\n{Fore.CYAN}Enter encrypted text: {Style.RESET_ALL}")
                password = input(f"{Fore.CYAN}Enter decryption password: {Style.RESET_ALL}")
                
                decrypt_text(encrypted_text, password)
            
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "4":
            key_size = input(f"\n{Fore.CYAN}Enter key size (1024, 2048, or 4096, default: 2048): {Style.RESET_ALL}")
            
            if key_size not in ["1024", "2048", "4096"]:
                key_size = 2048
            else:
                key_size = int(key_size)
            
            private_key, public_key = generate_rsa_keys(key_size)
            
            if private_key and public_key:
                print(f"\n{Fore.CYAN}Private Key:{Style.RESET_ALL}")
                print(private_key[:100] + "...")
                
                print(f"\n{Fore.CYAN}Public Key:{Style.RESET_ALL}")
                print(public_key[:100] + "...")
            
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "5":
            print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║        ASYMMETRIC ENCRYPTION MENU        ║{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
            
            print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Encrypt Text with Public Key")
            print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Decrypt Text with Private Key")
            
            rsa_choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")
            
            if rsa_choice == "1":
                text = input(f"\n{Fore.CYAN}Enter text to encrypt: {Style.RESET_ALL}")
                
                key_source = input(f"{Fore.CYAN}Use key from [1] File or [2] Paste (default: 1): {Style.RESET_ALL}")
                
                public_key = ""
                if key_source == "2":
                    print(f"{Fore.YELLOW}Paste public key (end with a line containing only 'END'):{Style.RESET_ALL}")
                    while True:
                        line = input()
                        if line == "END":
                            break
                        public_key += line + "\n"
                else:
                    key_file = input(f"{Fore.CYAN}Enter public key file path (default: public_key.pem): {Style.RESET_ALL}")
                    if not key_file:
                        key_file = "public_key.pem"
                    
                    try:
                        with open(key_file, 'r') as f:
                            public_key = f.read()
                    except Exception as e:
                        print(f"{Fore.RED}[-] Error reading key file: {str(e)}{Style.RESET_ALL}")
                        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                        continue
                
                encrypted = rsa_encrypt_text(text, public_key)
                if encrypted:
                    save = input(f"\n{Fore.CYAN}Save encrypted text to file? (y/n): {Style.RESET_ALL}").lower()
                    if save == 'y':
                        filename = input(f"{Fore.CYAN}Enter filename (default: rsa_encrypted.txt): {Style.RESET_ALL}")
                        if not filename:
                            filename = "rsa_encrypted.txt"
                        
                        with open(filename, 'w') as f:
                            f.write(encrypted)
                        
                        print(f"{Fore.GREEN}[+] Encrypted text saved to {filename}{Style.RESET_ALL}")
            
            elif rsa_choice == "2":
                encrypted_text = input(f"\n{Fore.CYAN}Enter encrypted text (Base64): {Style.RESET_ALL}")
                
                key_source = input(f"{Fore.CYAN}Use key from [1] File or [2] Paste (default: 1): {Style.RESET_ALL}")
                
                private_key = ""
                if key_source == "2":
                    print(f"{Fore.YELLOW}Paste private key (end with a line containing only 'END'):{Style.RESET_ALL}")
                    while True:
                        line = input()
                        if line == "END":
                            break
                        private_key += line + "\n"
                else:
                    key_file = input(f"{Fore.CYAN}Enter private key file path (default: private_key.pem): {Style.RESET_ALL}")
                    if not key_file:
                        key_file = "private_key.pem"
                    
                    try:
                        with open(key_file, 'r') as f:
                            private_key = f.read()
                    except Exception as e:
                        print(f"{Fore.RED}[-] Error reading key file: {str(e)}{Style.RESET_ALL}")
                        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                        continue
                
                rsa_decrypt_text(encrypted_text, private_key)
            
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "6":
            encode_decode_base64()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "7":
            break
        
        else:
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
            time.sleep(1)
