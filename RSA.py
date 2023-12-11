import random
import math

# List of prime numbers
available_primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, ...]


def is_prime(num):
    
    #Check if a number is prime
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def mod_inverse(a, m):
    
    #Compute the modular multiplicative inverse of 'a' modulo 'm'
    m0, x0, x1 = m, 0, 1

    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0

    return x1 + m0 if x1 < 0 else x1


def encrypt(message, public_key):
    
    #Encrypt a message using RSA
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message


def decrypt(encrypted_message, private_key):
    
    #Decrypt an encrypted message using RSA
    d, n = private_key
    decrypted_message = ''.join([chr(pow(char, d, n) % 256) for char in encrypted_message])
    return decrypted_message


def generate_keypair():
    
    #Generate a pair of public and private keys
    print("The prime numbers from 11:", available_primes)

    # Choose two distinct prime numbers from user input
    while True:
        try:
            p = int(input("\nEnter a prime number (p >= 11): "))
            if is_prime(p) and p >= 11:
                break
            else:
                print("Invalid input. Please enter a prime number greater than or equal to 11.")

        except ValueError:
            print("Error: Please enter a valid numeric input for the prime number.")

    while True:
        try:
            q = int(input("Enter another prime number (q >= 11 and different from p): "))
            if is_prime(q) and q >= 11 and q != p:
                break
            else:
                print("Invalid input. Please enter a prime number greater than 11 and different from p.")

        except ValueError:
            print("Error: Please enter a valid numeric input for the prime number.")

    print(f"\nGenerated prime numbers: p = {p}, q = {q}")

    # Compute n (modulus) and phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Choose a random public key 'e' such that 1 < e < phi_n and gcd(e, phi_n) = 1
    e = random.randint(2, phi_n - 1)
    while math.gcd(e, phi_n) != 1 or mod_inverse(e, phi_n) == e:
        e = random.randint(2, phi_n - 1)

    print(f"Chosen public key 'e': {e}")

    # Compute the private key 'd'
    d = mod_inverse(e, phi_n)

    print(f"Computed private key 'd': {d}")

    print(f"Computed modulus 'n': {n}")

    # Public key: (e, n), Private key: (d, n)
    return ((e, n), (d, n))


# Loop for repeated input
while True:
    
    # Generate key pair
    print("Generating key pair...")
    public_key, private_key = generate_keypair()

    # Input message to be encrypted
    while True:
        message = input("\nEnter the message to be encrypted (or type 'exit' to end): ")
        
        #Checks if the input is an ASCII character
        if all(ord(char) > 127 for char in message):
            print("Invalid input. Please enter a message without ASCII characters.")
        else:
            break

    if message.lower() == 'exit':
        break  # Exit the loop if the user types 'exit'

    # Encrypt the message
    print("\nEncrypting message...")
    encrypted_message = encrypt(message, public_key)
    print("Encrypted message:", encrypted_message)

    # Ask the user to enter private key (d) and (n)
    try:
        user_d, user_n = map(int, input("\nEnter the private key (d, n): ").split(','))
        user_private_key = (user_d, user_n)

        # Check if both d and n are incorrect before attempting to decrypt
        if user_d != private_key[0] or user_n != private_key[1]:
            print("Incorrect private key. Exiting the system.")
            exit()  # Exit the system if both d and n are incorrect

        decrypted_message = decrypt(encrypted_message, user_private_key)
        
    except ValueError:
        print("Incorrect private key. Exiting the system.")
        exit()  # Exit the system on numeric input error

    print("\nDecrypted message:", decrypted_message)

    # Ask the user if they want to continue
    continue_input = input("\nDo you want to encrypt another message? (yes/no): ")
    if continue_input.lower() != 'yes':
        break  # Exit the loop if the user does not want to continue
