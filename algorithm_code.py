import os
from sympy import symbols, simplify, Mod
from sympy.parsing.sympy_parser import parse_expr
from cryptography.hazmat.primitives.asymmetric import dh
from Crypto.Cipher import DES
import heapq
from graphviz import Digraph
import json
import http.server
import socketserver
import webbrowser
import subprocess
import time
import atexit
import math

def start_http_server():
    try:
        process = subprocess.Popen(['python3', '-m', 'http.server', '8080'], cwd='/home/arjay/Repository/Algorithm-Complexities',stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except FileNotFoundError as e:
        print(f"Error starting HTTP server: {e}")
        return None

def terminate_http_server(process):
    if process:
        process.terminate() 
        process.wait()  

atexit.register(terminate_http_server)

def start_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8080), handler) as httpd:
        print(f"Serving at port {8080}")
        httpd.serve_forever()

def open_browser():
    webbrowser.open(f"http://localhost:{8080}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_for_output():
    input("\nPress Enter to continue...")   

def show_main_menu():
    print("\nNumber System:")
    print("1) Calculator")
    print("2) Conversion")
    print("3) Bitwise Operations")
    print("\nNumber Theory:")
    print("4) Prime Factorization")
    print("5) Prime Numbers")
    print("6) GCD & LCM Calculator")
    print("7) Egyptian Fraction")
    print("8) Fibonacci")
    print("9) Euclidean Algorithm")
    print("10) Sieve of Eratosthenes")
    print("11) Modular Arithmetic")
    print("\nCryptography")
    print("12) Caesar Cipher")
    print("13) RSA (Rivest-Shamir-Adleman) Algorithm")
    print("14) Diffie-Hellman Key Exchange")
    print("15) AES (Advanced Encryption Standard)")
    print("16) DES (Data Encryption Standard)")
    print("\nGreedy Algorithm")
    print("17) Activity Selection Problem")
    print("18) Job Sequencing Problem") 
    print("19) Huffman Coding and Decoding")
    print("20) Knapsack Problem")
    print("21) Coin Change Problem")
    print("22) Mice to Holes Problem")
    print("\nGreedy Algorithm In Graphs")
    print("23) Minimum Spanning Tree")
    print("\n00) Exit")

class Calculator:
    def __init__(self):
        self.operations = {
            1: '+', 
            2: '-', 
            3: '*', 
            4: '/'
        }

    def calculator_menu(self):
        while True:
            clear_screen()
            print("\nCalculator Menu:")
            print("\n".join(f"{i}) {op}" for i, op in self.operations.items()))
            print("5) Back to Main Menu")
            
            calc_choice = int(input("Enter your choice: "))
            
            if calc_choice == 5:
                break
            
            if calc_choice in self.operations:
                clear_screen()
                print("Choose number system:")
                print("1) Binary")
                print("2) Octal")
                print("3) Hexadecimal")
                print("4) Decimal")
                base_choice = int(input("Enter choice: "))
                self.perform_operation(self.operations[calc_choice], base_choice)

    def perform_operation(self, operation, base):
        num1 = input("\nFirst Number: ")
        num2 = input("Second Number: ")

        base_map = {1: 2, 2: 8, 3: 16, 4: 10}
        selected_base = base_map[base]

        try:
            decimal_num1 = int(num1, selected_base)
            decimal_num2 = int(num2, selected_base)
        except ValueError:
            print("Invalid input. Please enter numbers in the specified base.")
            pause_for_output()
            return

        try:
            if operation == '+':
                result = decimal_num1 + decimal_num2
            elif operation == '-':
                result = decimal_num1 - decimal_num2
            elif operation == '*':
                result = decimal_num1 * decimal_num2
            elif operation == '/':
                if decimal_num2 == 0:
                    print("Error: Division by zero.")
                    pause_for_output()
                    return
                result = decimal_num1 // decimal_num2

            result_in_base = format(result, {2: 'b', 8: 'o', 16: 'X' , 10 :'d'}[selected_base])
            print(f"Result: {result_in_base}")
            pause_for_output()

        except Exception as e:
            print(f"Error performing operation: {e}")
            pause_for_output()
    
    def calculate_gcd(self, a, b):
        """Calculate GCD of two numbers and show steps."""
        print(f"Calculating GCD of {a} and {b} using the Euclidean algorithm:")
        steps = []
        while b:
            steps.append(f"GCD({a}, {b})")
            a, b = b, a % b
            steps.append(f"  a becomes {a}, b becomes {b} (Next step: GCD({a}, {b}))")
        print("Steps:")
        for step in steps:
            print(step)
        return a

    def calculate_lcm(self, a, b):
        """Calculate LCM of two numbers and show steps."""
        print(f"Calculating LCM of {a} and {b}:")
        gcd = self.calculate_gcd(a, b)  
        lcm = abs(a * b) // gcd
        print(f"LCM formula: LCM(a, b) = |a * b| / GCD(a, b)")
        print(f"Using GCD({a}, {b}) = {gcd}, the LCM is: {lcm}")
        return lcm
    
    def fibonacci_menu(self):
        """Fibonacci sequence generator."""
        while True:
            clear_screen()
            print("\nFibonacci Menu:")
            print("1) Generate Fibonacci sequence up to N terms")
            print("2) Back to Main Menu")

            choice = int(input("Enter your choice: "))
            if choice == 2:
                break
            elif choice == 1:
                n = int(input("Enter the number of terms: "))
                sequence = self.generate_fibonacci(n)
                print(f"Fibonacci sequence up to {n} terms: {sequence}")
            else:
                print("Invalid choice! Please choose again.")
            pause_for_output()

    def generate_fibonacci(self, n):
        """Generate Fibonacci sequence up to N terms with steps."""
        if n <= 0:
            return "Input should be a positive integer."
        elif n == 1:
            print("fib(1) = 0")
            return [0]
        elif n == 2:
            print("fib(1) = 0")
            print("fib(2) = 1")
            return [0, 1]

        sequence = [0, 1]
        print("fib(1) = 0")
        print("fib(2) = 1")
        for i in range(2, n):
            next_value = sequence[-1] + sequence[-2]
            sequence.append(next_value)
            print(f"fib({i + 1}) = fib({i}) + fib({i - 1}) = {sequence[-1]}")

        return sequence
        
    def sieve_menu(self):
        """Sieve of Eratosthenes for prime numbers."""
        while True:
            clear_screen()
            print("\nSieve of Eratosthenes Menu:")
            print("1) Generate prime numbers up to a given number")
            print("2) Back to Main Menu")

            choice = int(input("348:s "))
            if choice == 2:
                break
            elif choice == 1:
                limit = int(input("Generate primes up to: "))
                primes = self.sieve_of_eratosthenes(limit)
                print(f"Prime numbers up to {limit}: {primes}")
            else:
                print("Invalid choice! Please choose again.")
            pause_for_output()

    def sieve_of_eratosthenes(self, limit):
        """Generate all primes up to 'limit' using Sieve of Eratosthenes."""
        is_prime = [True] * (limit + 1)
        primes = []
        for num in range(2, limit + 1):
            if is_prime[num]:
                primes.append(num)
                for multiple in range(num * num, limit + 1, num):
                    is_prime[multiple] = False
        return primes

    def euclidean_menu(self):
        clear_screen()  
        print("Welcome to the Euclidean Algorithm Calculator!")
        try:
            a = int(input("Enter the first number: "))
            b = int(input("Enter the second number: "))
            print(f"The GCD of {a} and {b} is: {self.euclidean_algorithm(a, b)}")
        except ValueError:
            print("Please enter valid integers.")
        
    def euclidean_algorithm(self, a, b):
        print("\nStarting Euclidean Algorithm Steps:")
        step = 1
        while b != 0:
            print(f"Step {step}:")
            print(f"  a = {a}, b = {b}")
            a, b = b, a % b
            print(f"  Updated values -> a = {a}, b = {b}\n")
            step += 1
        print(f"Algorithm completed. THE GCD is {a}")
        pause_for_output()
        return a
    
    def modular_menu(self):
        clear_screen()
        print("Welcome to the Modular Arithmetic Calculator!")
        try:
            expr = input("Enter an expression (e.g., 3 - 2*5**6 + 3*(4)**5 + 1): ")
            modulus = int(input("Enter the modulus: "))
            result = self.modular_arithmetic(expr, modulus)
            print(f"The result of ({expr}) mod {modulus} is: {result}")
            pause_for_output()
        except ValueError:
            print("Invalid input. Please enter a valid expression and modulus.")

    def modular_arithmetic(self, expression, modulus):
        """Evaluate an expression under a modulus and show steps."""
        parsed_expr = parse_expr(expression)
        print(f"Parsed expression: {parsed_expr}")
        simplified_expr = simplify(parsed_expr)
        print(f"Simplified expression: {simplified_expr}")
        mod_expr = Mod(simplified_expr, modulus)
        print(f"Calculating: ({simplified_expr}) mod {modulus}")
        return mod_expr   
        

def convert_to_egyptian(numerator, denominator):
    """Convert a fraction to a list of Egyptian fractions."""
    if denominator == 0:
        return None
        
    egyptian_fractions = []
    
    if numerator * denominator < 0:
        print("Warning: Converting to positive fraction first")
    numerator, denominator = abs(numerator), abs(denominator)
    
    if numerator == 0:
        return []
    
    if denominator % numerator == 0:
        print(f"Fraction {numerator}/{denominator} is an integer.")
        return [denominator // numerator]

    print(f"Converting {numerator}/{denominator} to Egyptian fractions:")
    
    while numerator != 0:
        unit_fraction = -(-denominator // numerator)  
        egyptian_fractions.append(unit_fraction)
        
        print(f"  Adding unit fraction: 1/{unit_fraction}")

      
        new_numerator = numerator * unit_fraction - denominator
        new_denominator = denominator * unit_fraction
        
        print(f"  New fraction: {new_numerator}/{new_denominator} after subtracting 1/{unit_fraction}")
        
  
        if new_numerator != 0:
            gcd = Calculator.calculate_gcd(0, abs(new_numerator), new_denominator)
            numerator = new_numerator // gcd
            denominator = new_denominator // gcd
            print(f"  Simplified to: {numerator}/{denominator}")
        else:
            numerator = 0
            
    return egyptian_fractions
        

def conversion_menu():
    conversion_methods = [
        ("Binary to Others", binary_to_others),
        ("Octal to Others", octal_to_others),
        ("Decimal to Others", decimal_to_others),
        ("Hexadecimal to Others", hexadecimal_to_others),
        ("Back to Main Menu", None)
    ]

    while True:
        clear_screen()
        print("\nConversion Menu:")
        for i, (desc, _) in enumerate(conversion_methods):
            print(f"{i + 1}) {desc}")

        conv_choice = int(input("348: "))
        
        if conv_choice == 5:
            break

        _, conversion_function = conversion_methods[conv_choice - 1]
        conversion_function() if conversion_function else None

def binary_to_others():
    clear_screen()
    binary = input("\nEnter binary number: ")
    decimal = int(binary, 2)
    print("Decimal:", decimal)
    print("Octal:", convert_number(binary, 2, 8))
    print("Hexadecimal:", convert_number(binary, 2, 16))
    pause_for_output()

def octal_to_others():
    clear_screen()
    octal = input("\nEnter octal number: ")
    decimal = int(octal, 8)
    print("Decimal:", decimal)
    print("Binary:", convert_number(octal, 8, 2))
    print("Hexadecimal:", convert_number(octal, 8, 16))
    pause_for_output()

def decimal_to_others():
    clear_screen()
    decimal = input("\nEnter decimal number: ")
    print("Binary:", convert_number(decimal, 10, 2))
    print("Octal:", convert_number(decimal, 10, 8))
    print("Hexadecimal:", convert_number(decimal, 10, 16))
    pause_for_output()

def hexadecimal_to_others():
    clear_screen()
    hex_val = input("\nEnter hexadecimal number: ")
    decimal = int(hex_val, 16)
    print("Decimal:", decimal)
    print("Binary:", convert_number(hex_val, 16, 2))
    print("Octal:", convert_number(hex_val, 16, 8))
    pause_for_output()

def convert_number(num, base_from, base_to):
    if isinstance(num, int):
        if base_from == 10:
            return format(num, {2: 'b', 8: 'o', 10: 'd', 16: 'X'}[base_to])
        else:
            raise ValueError("Integer input must be in base 10")
    
    decimal_num = int(str(num), base_from)
    return format(decimal_num, {2: 'b', 8: 'o', 10: 'd', 16: 'X'}[base_to])

def bitwise_menu():
    while True:
        clear_screen()
        print("\nBitwise Operations Menu:")
        print("1) Show Bitwise Table")
        print("2) Back to Main Menu")
        
        bitwise_choice = int(input("Enter your choice: "))  
        
        if bitwise_choice == 2:
            break
        if bitwise_choice == 1:
            show_bitwise_table()

def show_bitwise_table():
    x = input("\nEnter Binary X: ")
    y = input("Enter Binary Y: ")
    
    if len(x) != len(y):
        print("Error: Binary strings must be of the same length.")
        pause_for_output()
        return
    
    results = {
        'AND': bitwise_and(x, y),
        'OR': bitwise_or(x, y),
        'XOR': bitwise_xor(x, y),
        '!X': bitwise_not(x),
        '!Y': bitwise_not(y)
    }

    print(f"{'X':<10} {'Y':<10} {'AND':<10} {'OR':<10} {'XOR':<10} {'!X':<10} {'!Y':<10}")
    print("-" * 70)
    for i in range(len(x)):
        print(f"{x[i]:<10} {y[i]:<10} {results['AND'][i]:<10} {results['OR'][i]:<10} {results['XOR'][i]:<10} {results['!X'][i]:<10} {results['!Y'][i]:<10}")
    pause_for_output()

def bitwise_and(x, y):
    return ''.join('1' if x[i] == '1' and y[i] == '1' else '0' for i in range(len(x)))

def bitwise_or(x, y):
    return ''.join('1' if x[i] == '1' or y[i] == '1' else '0' for i in range(len(x)))

def bitwise_xor(x, y):
    return ''.join('1' if x[i] != y[i] else '0' for i in range(len(x)))

def bitwise_not(x):
    return ''.join('0' if bit == '1' else '1' for bit in x)

def prime_menu():
    while True:
        clear_screen()
        print("Prime Numbers")
        try:
            from_digit = int(input("FROM: "))
            to_digit = int(input("TO: "))
            if from_digit > to_digit:
                print("Error: 'FROM' must be less than or equal to 'TO'. Please try again.")
                pause_for_output()
                continue

            primes = get_prime_numbers(from_digit, to_digit)
            if primes:
                print(f"Prime numbers between {from_digit} and {to_digit}: {primes}")
            else:
                print(f"No prime numbers found between {from_digit} and {to_digit}.")
            pause_for_output()
            break
            
        except ValueError:
            print("Invalid input! Please enter integers only.")

def is_prime(num):
    if num <= 1:
        return False
    return all(num % i != 0 for i in range(2, int(num**0.5) + 1))

def get_prime_numbers(start, end):
    return [num for num in range(start, end + 1) if is_prime(num)]

def gcd_lcm_menu(self):
        while True:
            clear_screen()
            print("\nGCD & LCM Calculator Menu:")
            print("1) Calculate GCD")
            print("2) Calculate LCM")
            print("3) Back to Main Menu")

            choice = int(input("Enter your choice: "))
            
            if choice == 3:
                break
            elif choice in [1, 2]:
                a = int(input("Enter first number: "))
                b = int(input("Enter second number: "))
                if choice == 1:
                    gcd_result = self.calculate_gcd(a, b)
                    print(f"GCD of {a} and {b} is: {gcd_result}")
                else:
                    lcm_result = self.calculate_lcm(a, b)
                    print(f"LCM of {a} and {b} is: {lcm_result}")
                pause_for_output()

def egyptian_fraction_menu(calculator):
    """Handle the Egyptian fraction menu operations."""
    while True:
        clear_screen()
        print("\nEgyptian Fraction Calculator")
        print("1) Convert fraction to Egyptian fractions")
        print("2) Back to Main Menu")
        
        try:
            choice = int(input("Enter your choice: "))
            
            if choice == 2:
                break
            elif choice == 1:
                try:
                    numerator = int(input("\nEnter numerator: "))
                    denominator = int(input("Enter denominator: "))
                    if denominator == 0:
                        print("Error: Denominator cannot be zero.")
                    else:
                        egyptian_fractions = convert_to_egyptian(numerator, denominator)
                        print("\nEgyptian fraction representation:")
                        print(" + ".join([f"1/{f}" for f in egyptian_fractions]))
                except ValueError:
                    print("Please enter valid integers.")
                pause_for_output()
            else:
                print("Invalid choice. Please try again.")
                pause_for_output()
        except ValueError:
            print("Invalid input. Please enter a number.")
            pause_for_output()

def prime_factorization_menu():
    clear_screen()
    number = int(input("Enter a positive integer for prime factorization: "))
    if number > 0:
        factors = prime_factors(number)
        print(f"Prime factors of {number} are: {factors}")
        pause_for_output()
    else:
        print("Please enter a positive integer.")
        pause_for_output()

def prime_factors(n):
    factors = []
    
    
    while n % 2 == 0:
        factors.append(2)
        print(f"Found factor: 2")
        n //= 2
        print(f"Reducing n: Now n = {n}")
    
    
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            print(f"Found factor: {i}")
            n //= i
            print(f"Reducing n: Now n = {n}")
    
    
    if n > 2:
        factors.append(n)
        print(f"Found factor: {n}")

    return factors

def user_input(prompt, key_length=None):
    """Handles user input for text and keys, ensuring correct length for cryptographic keys."""
    if key_length:
        while True:
            key = input(prompt)
            if len(key) == key_length:
                return key.encode()
            print(f"Key must be exactly {key_length} bytes.")
    else:
        return input(prompt)

def caesar_cipher_menu():
    clear_screen()
    text = user_input("Enter text to encrypt: ")
    shift = int(user_input("Enter shift value: "))
    encrypted_text = caesar_cipher(text, shift)
    print(f"\nEncrypted Text (Caesar Cipher): {encrypted_text}")
    pause_for_output()

def caesar_cipher(text, shift):
    """Encrypts text using Caesar Cipher."""
    result = ""
    print(f"\nEncrypting text: '{text}' with a shift of {shift}")
    
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26  
            print(f"Processing character: {char}")
            
            if char.isupper():
                new_char = chr(((ord(char) - 65 + shift_amount) % 26) + 65)
                print(f"Uppercase: '{char}' becomes '{new_char}'")
            else:
                new_char = chr(((ord(char) - 97 + shift_amount) % 26) + 97)
                print(f"Lowercase: '{char}' becomes '{new_char}'")
            
            result += new_char
        else:
            print(f"Non-alphabet character: '{char}' remains unchanged")
            result += char
    
    return result

def rsa_menu():
    clear_screen()
    p = int(input("Enter a prime number p: "))
    q = int(input("Enter a prime number q: "))
    e = int(input("Enter a public key exponent e (must be coprime with φ(n)): "))
    plaintext = int(input("Enter the plaintext (an integer less than n): "))
    return rsa_encrypt_decrypt(p, q, e, plaintext)

def rsa_encrypt_decrypt(p, q, e, plaintext):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    print(f"\nStep 1: Calculate n and φ(n)")
    print(f"n = p * q = {p} * {q} = {n}")
    print(f"φ(n) = (p - 1) * (q - 1) = ({p} - 1) * ({q} - 1) = {phi_n}")
    pause_for_output()  

    D = None
    attempts = []
    found = False

    
    for i in range(1, 1000): 
        potential_d = (phi_n * i + 1) / e
        attempts.append((i, round(potential_d, 2)))  
        if potential_d == int(potential_d):
            D = int(potential_d)
            found = True
            break

    
    print("\nStep 2: Finding D with each i value:")
    for attempt in attempts:
        i_val, d_val = attempt
        print(f"i = {i_val}, D = (φ(n) * i + 1) / e = ({phi_n} * {i_val} + 1) / {e} = {d_val}")
    
    if found:
        print(f"\nFound D = {D} when i = {i}\n")
    else:
        print("\nFailed to find a valid D within the range.")

    pause_for_output()  

  
    ciphertext = pow(plaintext, e, n) 
    print(f"Step 3: Encrypting the plaintext")
    print(f"Ciphertext = plaintext^e mod n = {plaintext}^{e} mod {n} = {ciphertext}")
    pause_for_output()  

   
    decrypted_text = pow(ciphertext, D, n)  
    print(f"\nStep 4: Decrypting the ciphertext")
    print(f"Recovered plaintext = ciphertext^D mod n = {ciphertext}^{D} mod {n} = {decrypted_text}")
    pause_for_output() 

    return {
        "n": n,
        "phi_n": phi_n,
        "public_key": (e, n),
        "private_key": (D, n),
        "ciphertext": ciphertext,
        "decrypted_text": decrypted_text
    }

def diffie_hellman_menu():
    clear_screen()
    p = int(input("Enter a prime number p: "))
    g = int(input("Enter a base number g: "))
    a = int(input("Enter your private key a: "))
    b = int(input("Enter your friend's private key b: "))
    return diffie_hellman_key_exchange(p, g, a, b)

def diffie_hellman_key_exchange(p, g, a, b):
    """Perform Diffie-Hellman key exchange with key substitution until keys match."""
    
   
    A = pow(g, a, p)  
    B = pow(g, b, p)  
    
    print(f"\nAlice A = g^a % p = {g}^{a} % {p} = {A}")
    print(f"Bob key B = g^b % p = {g}^{b} % {p} = {B}")
    
    
    input("\nPress Enter to continue...")
    
    
    shared_secret_A = A  
    shared_secret_B = B  
    
    print("\nStarting key substitution process...")
    
    iteration = 1
    while shared_secret_A != shared_secret_B:
        print(f"\nIteration {iteration}:")
        print(f"Alice Current Key = {shared_secret_A}")
        print(f"Bob Current key = {shared_secret_B}")
        
        
        shared_secret_A = pow(shared_secret_B, a, p)
        print(f"Alice new shared secret key = B^a % p = {shared_secret_B}^{a} % {p} = {shared_secret_A}")
        
       
        shared_secret_B = pow(shared_secret_A, b, p)
        print(f"Bob friend's new shared secret key = A^b % p = {shared_secret_A}^{b} % {p} = {shared_secret_B}")
        
        iteration += 1
        
        
        input("\nPress Enter to continue...")

   
    print("\nThe shared secret keys match!")
    print(f"Final shared secret key = {shared_secret_A}")
    
    pause_for_output()  

def aes_menu():
    clear_screen()
    plainText = input("Enter plain text in multiple of 16 bytes: ")
    key = input("Enter key in multiple of 16 bytes: ")

    def keyExpansion(key,numround,rci,s_box):
        round_const = rci[numround-1]
        gw3 = [key[3][1],key[3][2],key[3][3],key[3][0]]
        for i in range(4):
            u = hex(s_box[int(gw3[i][2],16)][int(gw3[i][3],16)])
            if(u == "0x0"):
                u = "0x00"
            elif(len(u.lstrip("0x"))<=1):
                u = "0x0"+u.lstrip("0x")
            gw3[i] = u
        a = 1
        b = 1
        if(gw3[0] == "0x00" or gw3[0] == "0x0"):
            a = 0
        else:
            a = int(gw3[0].lstrip("0x"),16)
        x = hex(int(a^int(round_const.lstrip("0x"),16)))
        if(x == "0x0"):
            x = "0x00"
        elif(len(x.lstrip("0x"))<=1):
            x = "0x0"+x.lstrip("0x")
        gw3[0] = x
        w4 = []
        for i in range(4):
            r = 1
            p = 1
            if(gw3[i] == "0x00" or gw3[i] == "0x0"):
                r = 0
            else:
                r = int(gw3[i].lstrip("0x"),16)
            if(key[0][i] == "0x00" or key[0][i] == "0x0"):
                p = 0
            else:
                p = int(key[0][i].lstrip("0x"),16)
            y = hex(r^p)
            if(y == "0x0"):
                y = "0x00"
            elif(len(y.lstrip("0x")) <= 1):
                y = "0x0"+y.lstrip("0x")
            w4.append(y)
        w5 = []
        w6 = []
        w7 = []
        for i in range(4):
            r = 1
            p = 1
            if(w4[i] == "0x00" or w4[i] == "0x0"):
                r = 0
            else:
                r = int(w4[i].lstrip("0x"),16)
            if(key[1][i] == "0x00" or key[1][i] == "0x0"):
                p = 0
            else:
                p = int(key[1][i].lstrip("0x"),16)
            y = hex(r^p)
            if(y == "0x0"):
                y = "0x00"
            elif(len(y.lstrip("0x")) <= 1):
                y = "0x0"+y.lstrip("0x")
            w5.append(y)
        for i in range(4):
            r = 1
            p = 1
            if(w5[i] == "0x00" or w5[i] == "0x0"):
                r = 0
            else:
                r = int(w5[i].lstrip("0x"),16)
            if(key[2][i] == "0x00" or key[2][i] == "0x0"):
                p = 0
            else:
                p = int(key[2][i].lstrip("0x"),16)
            y = hex(r^p)
            if(y == "0x0"):
                y = "0x00"
            elif(len(y.lstrip("0x")) <= 1):
                y = "0x0"+y.lstrip("0x")
            w6.append(y)
        for i in range(4):
            r = 1
            p = 1
            if(w6[i] == "0x00" or w6[i] == "0x0"):
                r = 0
            else:
                r = int(w6[i].lstrip("0x"),16)
            if(key[3][i] == "0x00" or key[3][i] == "0x0"):
                p = 0
            else:
                p = int(key[3][i].lstrip("0x"),16)
            y = hex(r^p)
            if(y == "0x0"):
                y = "0x00"
            elif(len(y.lstrip("0x")) <= 1):
                y = "0x0"+y.lstrip("0x")
            w7.append(y)
        return [w4,w5,w6,w7]

    def addRoundKey(pt,rk):
        for i in range(4):
            for j in range(4):
                x = 0
                y = 0
                if(pt[j][i] != "0x00"):
                    x = int(pt[j][i].lstrip("0x"),16)
                if(rk[j][i] != "0x00"):
                    y = int(rk[j][i].lstrip("0x"),16)
                z = hex(x^y)
                if(z == "0x0"):
                    z = "0x00"
                elif(len(z.lstrip("0x")) <= 1):
                    z = "0x0"+z.lstrip("0x")
                pt[j][i] = z
        return pt

    def substitute(pt,s_box):
        for i in range(4):
            for j in range(4):
                u = hex(s_box[int(pt[i][j][2],16)][int(pt[i][j][3],16)])
                if(u == "0x0"):
                    u = "0x00"
                elif(len(u.lstrip("0x"))<=1):
                    u = "0x0"+u.lstrip("0x")
                pt[i][j] = u
        return pt

    def shiftRow(pt):
        pt[0][1],pt[1][1],pt[2][1],pt[3][1] = pt[1][1],pt[2][1],pt[3][1],pt[0][1]
        pt[0][2],pt[1][2],pt[2][2],pt[3][2] = pt[2][2],pt[3][2],pt[0][2],pt[1][2]
        pt[0][3],pt[1][3],pt[2][3],pt[3][3] = pt[3][3],pt[0][3],pt[1][3],pt[2][3]
        return pt

    def mixMulCol(col,mul2,mul3):
        temp = []
        i = mul2[int(col[0][2],16)][int(col[0][3],16)]
        j = mul3[int(col[1][2],16)][int(col[1][3],16)]
        k = int(col[2],16)
        l = int(col[3],16)
        m = hex(i^j^k^l)
        if(m == "0x0"):
            m = "0x00"
        elif(len(m.lstrip("0x")) <= 1):
            m = "0x0"+m.lstrip("0x")
        temp.append(m)

        i = int(col[0],16)
        j = mul2[int(col[1][2],16)][int(col[1][3],16)]
        k = mul3[int(col[2][2],16)][int(col[2][3],16)]
        l = int(col[3],16)
        m = hex(i^j^k^l)
        if(m == "0x0"):
            m = "0x00"
        elif(len(m.lstrip("0x")) <= 1):
            m = "0x0"+m.lstrip("0x")
        temp.append(m)

        i = int(col[0],16)
        j = int(col[1],16)
        k = mul2[int(col[2][2],16)][int(col[2][3],16)]
        l = mul3[int(col[3][2],16)][int(col[3][3],16)]
        m = hex(i^j^k^l)
        if(m == "0x0"):
            m = "0x00"
        elif(len(m.lstrip("0x")) <= 1):
            m = "0x0"+m.lstrip("0x")
        temp.append(m)

        i = mul3[int(col[0][2],16)][int(col[0][3],16)]
        j = int(col[1],16)
        k = int(col[2],16)
        l = mul2[int(col[3][2],16)][int(col[3][3],16)]
        m = hex(i^j^k^l)
        if(m == "0x0"):
            m = "0x00"
        elif(len(m.lstrip("0x")) <= 1):
            m = "0x0"+m.lstrip("0x")
        temp.append(m)
        return temp
    def mixCol(mul2,mul3,pt):
        res = []
        for i in range(4):
            temp = []
            temp.append(pt[i][0])
            temp.append(pt[i][1])
            temp.append(pt[i][2])
            temp.append(pt[i][3])
            res.append(mixMulCol(temp,mul2,mul3))
        return res
    def printMatrix(m):
        for i in range(4):
            for j in range(4):
                y = m[j][i]
                if(y == "0x00"):
                    y = "00"
                elif(len(y.lstrip("0x")) <= 1):
                    y = "0"+y.lstrip("0x")
                else:
                    y = y.lstrip("0x")
                print(y.upper(),end=" ")
            print(" ")
    def printCipher(m):
        for i in range(4):
            for j in range(4):
                y = m[i][j]
                if(y == "0x00"):
                    y = "00"
                elif(len(y.lstrip("0x")) <= 1):
                    y = "0"+y.lstrip("0x")
                else:
                    y = y.lstrip("0x")
                print(y.upper(),end=" ")
        print(" ")

    s_box = [
        [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
        [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
        [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
        [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
        [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
        [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
        [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
        [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
        [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
        [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
        [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
        [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
        [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
        [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
        [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
        [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
    ]
    rci = ["0x01","0x02","0x04","0x08","0x10","0x20","0x40","0x80","0x1B","0x36"]
    mul2 = [
        [0x00,0x02,0x04,0x06,0x08,0x0a,0x0c,0x0e,0x10,0x12,0x14,0x16,0x18,0x1a,0x1c,0x1e],
    [0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e],
    [0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e],
    [0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e],
    [0x80,0x82,0x84,0x86,0x88,0x8a,0x8c,0x8e,0x90,0x92,0x94,0x96,0x98,0x9a,0x9c,0x9e],
    [0xa0,0xa2,0xa4,0xa6,0xa8,0xaa,0xac,0xae,0xb0,0xb2,0xb4,0xb6,0xb8,0xba,0xbc,0xbe],
    [0xc0,0xc2,0xc4,0xc6,0xc8,0xca,0xcc,0xce,0xd0,0xd2,0xd4,0xd6,0xd8,0xda,0xdc,0xde],
    [0xe0,0xe2,0xe4,0xe6,0xe8,0xea,0xec,0xee,0xf0,0xf2,0xf4,0xf6,0xf8,0xfa,0xfc,0xfe],
    [0x1b,0x19,0x1f,0x1d,0x13,0x11,0x17,0x15,0x0b,0x09,0x0f,0x0d,0x03,0x01,0x07,0x05],
    [0x3b,0x39,0x3f,0x3d,0x33,0x31,0x37,0x35,0x2b,0x29,0x2f,0x2d,0x23,0x21,0x27,0x25],
    [0x5b,0x59,0x5f,0x5d,0x53,0x51,0x57,0x55,0x4b,0x49,0x4f,0x4d,0x43,0x41,0x47,0x45],
    [0x7b,0x79,0x7f,0x7d,0x73,0x71,0x77,0x75,0x6b,0x69,0x6f,0x6d,0x63,0x61,0x67,0x65],
    [0x9b,0x99,0x9f,0x9d,0x93,0x91,0x97,0x95,0x8b,0x89,0x8f,0x8d,0x83,0x81,0x87,0x85],
    [0xbb,0xb9,0xbf,0xbd,0xb3,0xb1,0xb7,0xb5,0xab,0xa9,0xaf,0xad,0xa3,0xa1,0xa7,0xa5],
    [0xdb,0xd9,0xdf,0xdd,0xd3,0xd1,0xd7,0xd5,0xcb,0xc9,0xcf,0xcd,0xc3,0xc1,0xc7,0xc5],
    [0xfb,0xf9,0xff,0xfd,0xf3,0xf1,0xf7,0xf5,0xeb,0xe9,0xef,0xed,0xe3,0xe1,0xe7,0xe5]]

    mul3 = [[0x00,0x03,0x06,0x05,0x0c,0x0f,0x0a,0x09,0x18,0x1b,0x1e,0x1d,0x14,0x17,0x12,0x11],
    [0x30,0x33,0x36,0x35,0x3c,0x3f,0x3a,0x39,0x28,0x2b,0x2e,0x2d,0x24,0x27,0x22,0x21],
    [0x60,0x63,0x66,0x65,0x6c,0x6f,0x6a,0x69,0x78,0x7b,0x7e,0x7d,0x74,0x77,0x72,0x71],
    [0x50,0x53,0x56,0x55,0x5c,0x5f,0x5a,0x59,0x48,0x4b,0x4e,0x4d,0x44,0x47,0x42,0x41],
    [0xc0,0xc3,0xc6,0xc5,0xcc,0xcf,0xca,0xc9,0xd8,0xdb,0xde,0xdd,0xd4,0xd7,0xd2,0xd1],
    [0xf0,0xf3,0xf6,0xf5,0xfc,0xff,0xfa,0xf9,0xe8,0xeb,0xee,0xed,0xe4,0xe7,0xe2,0xe1],
    [0xa0,0xa3,0xa6,0xa5,0xac,0xaf,0xaa,0xa9,0xb8,0xbb,0xbe,0xbd,0xb4,0xb7,0xb2,0xb1],
    [0x90,0x93,0x96,0x95,0x9c,0x9f,0x9a,0x99,0x88,0x8b,0x8e,0x8d,0x84,0x87,0x82,0x81],
    [0x9b,0x98,0x9d,0x9e,0x97,0x94,0x91,0x92,0x83,0x80,0x85,0x86,0x8f,0x8c,0x89,0x8a],
    [0xab,0xa8,0xad,0xae,0xa7,0xa4,0xa1,0xa2,0xb3,0xb0,0xb5,0xb6,0xbf,0xbc,0xb9,0xba],
    [0xfb,0xf8,0xfd,0xfe,0xf7,0xf4,0xf1,0xf2,0xe3,0xe0,0xe5,0xe6,0xef,0xec,0xe9,0xea],
    [0xcb,0xc8,0xcd,0xce,0xc7,0xc4,0xc1,0xc2,0xd3,0xd0,0xd5,0xd6,0xdf,0xdc,0xd9,0xda],
    [0x5b,0x58,0x5d,0x5e,0x57,0x54,0x51,0x52,0x43,0x40,0x45,0x46,0x4f,0x4c,0x49,0x4a],
    [0x6b,0x68,0x6d,0x6e,0x67,0x64,0x61,0x62,0x73,0x70,0x75,0x76,0x7f,0x7c,0x79,0x7a],
    [0x3b,0x38,0x3d,0x3e,0x37,0x34,0x31,0x32,0x23,0x20,0x25,0x26,0x2f,0x2c,0x29,0x2a],
    [0x0b,0x08,0x0d,0x0e,0x07,0x04,0x01,0x02,0x13,0x10,0x15,0x16,0x1f,0x1c,0x19,0x1a]]

    initialState = []
    initialKey = []
    finalState = []
    total = 0
    for i in range(4):
        temp = []
        temp1 = []
        temp2 = []
        for j in range(4):
            temp2.append(hex(ord(plainText[total])))
            temp.append(hex(ord(plainText[total])))
            temp1.append(hex(ord(key[total])))
            total+=1
        initialState.append(temp)
        initialKey.append(temp1)
        finalState.append(temp2)
    print("--------Initial----------")
    print("Initial Plain text Matrix")
    printMatrix(initialState)
    print("Initial Key matrix")
    printMatrix(initialKey)
    print("-------------------------")
    print("---------Round 0---------")
    print("After round 0 add key")
    initialState = addRoundKey(initialState,initialKey)
    printMatrix(initialState)
    for i in range(1,11):
        print("--------Round "+str(i)+"---------")
        initialKey = keyExpansion(initialKey,i,rci,s_box)
        print("This round Key")
        printMatrix(initialKey)
        print("After Susbstitution")
        initialState = substitute(initialState,s_box)
        printMatrix(initialState)

        print("After shift rows")
        initialState = shiftRow(initialState)
        printMatrix(initialState)
        if(i!=10):
            print("After Mix column")
            initialState = mixCol(mul2,mul3,initialState)
            printMatrix(initialState)

        print("After add round key")
        initialState = addRoundKey(initialState,initialKey)
        printMatrix(initialState)
    print("-----------Result----------")
    print("Original Message")
    printCipher(finalState)
    print("The cipher text is")
    printCipher(initialState)



class DES:
    S0_table = [
        [1, 0, 3, 2],
        [3, 2, 0, 1],
        [0, 2, 1, 3],
        [2, 1, 0, 3]
    ]

    S1_table = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 2],
        [2, 1, 0, 3]
    ]

    def hexToInt_single(self, hex_str):
        return int(hex_str, 16)

    def intToBinaryString_single(self, num, bits=2):
        return format(num, '0{}b'.format(bits))

    def binaryToHex_single(self, binary_str):
        return format(int(binary_str, 2), 'x')

    def hexToInt(self, hex_list):
        return [int(x, 16) for x in hex_list]

    def hexToBinaryString(self, hex_values, bits=8):
        return [format(int(x, 16), '0{}b'.format(bits)) for x in hex_values]

    def binaryToHex(self, binary_str):
        return format(int(binary_str, 2), 'x')

    def valid_input(self, label, size, limit):
        num = []
        print(f"\nEnter your {label} Values")
        for i in range(size):
            while True:
                val = int(input(f"\n{label}[{i + 1}] = "))
                if limit <= val <= size:
                    num.append(val)
                    break
                else:
                    print(f"Invalid input. Please enter a valid number between {limit} and {size}.")
        return num

    def valid_key_input(self, label, size, limit):
        num = []
        print(f"\nEnter your {label} Values")
        for i in range(size):
            while True:
                val = int(input(f"\n{label}[{i}] = "))
                if val in [0, 1]:
                    num.append(val)
                    break
                else:
                    print(f"Invalid input. Please enter 0 or 1.")
        return num

    def display_box(self, label, values, inputSize, outputSize):
        boxWidth = 10 + inputSize * 4

        if label == "KEY":
            print("\nKEY: ", "".join(map(str, values)))
        else:
            print('_' * boxWidth)
            print("|" + f"{label:<{boxWidth - 1}}|")
            print("|Input   |" + "".join([f"{i:<4}" for i in range(1, inputSize + 1)]) + "|")
            print('-' * boxWidth)
            print("|Output  |" + "".join([f"{x:<4}" for x in values]) + "|")
            print('-' * boxWidth)

    def permutate(self, permPattern, bits, size, message):
        print(f"permutate {message}: ", end='')
        storage = [bits[permPattern[i] - 1] for i in range(size)]
        print("".join(map(str, storage)))
        return storage

    def left_shift(self, bits, shifts):
        return bits[shifts:] + bits[:shifts]

    def binaryStringToVector(self, binary_str):
        return [int(bit) for bit in binary_str]

    def IP_EP_STEP(self, PT, IP, EP, P4, K1):
        Initial = self.permutate(IP, PT, 8, "IP")

        left_half = Initial[:4]
        right_half = Initial[4:]

        print("\nCurrent Plaintext: ", "".join(map(str, PT)))
        print("IP: ", "".join(map(str, Initial)))
        print("left_half: ", "".join(map(str, left_half)))
        print("right_half: ", "".join(map(str, right_half)))

        EP_bit = self.permutate(EP, right_half, 8, "EP")

        XOR_result = [EP_bit[i] ^ K1[i] for i in range(8)]

        print("EP: ", "".join(map(str, EP_bit)))
        print("XOR of EP and K1: ", "".join(map(str, XOR_result)))

        S0 = XOR_result[:4]
        S1 = XOR_result[4:]

        S0_row = int(f"{S0[0]}{S0[3]}", 2)
        S0_col = int(f"{S0[1]}{S0[2]}", 2)
        S1_row = int(f"{S1[0]}{S1[3]}", 2)
        S1_col = int(f"{S1[1]}{S1[2]}", 2)

        print(f"S0 row: {S0_row}, col: {S0_col}")
        print(f"S1 row: {S1_row}, col: {S1_col}")

        S0_answer = self.S0_table[S0_row][S0_col]
        S1_answer = self.S1_table[S1_row][S1_col]

        s0_binary = self.intToBinaryString_single(S0_answer, 2)
        s1_binary = self.intToBinaryString_single(S1_answer, 2)

        print("S0 Output (binary): ", s0_binary)
        print("S1 Output (binary): ", s1_binary)

        combined_binary = s0_binary + s1_binary
        combined_vector = self.binaryStringToVector(combined_binary)

        P4_bit = self.permutate(P4, combined_vector, 4, "P4")

        XOR_result2 = [P4_bit[i] ^ left_half[i] for i in range(4)]

        final_answer = XOR_result2 + right_half

        print("XOR of IP,SOS1 and P4: ", "".join(map(str, final_answer)))

        shifted_answer = right_half + XOR_result2

        print("final_answer: ", "".join(map(str, shifted_answer)))

        return shifted_answer

    def des_menu(self):
        clear_screen()
        print("\n\n| ----- DES ----- |\n\n")
        print("| ---- USER INPUT FOR KEYS ---- |\n\n")
        p10 = self.valid_input("P10", 10, 1)
        p8 = self.valid_input("P8", 8, 1)
        p4 = self.valid_input("P4", 4, 1)
        EP = self.valid_input("EP", 8, 1)
        IP = self.valid_input("IP", 8, 1)
        KEY_INPUT = self.valid_key_input("KEY", 10, 0)

        self.display_box("P10", p10, 10, 10)
        self.display_box("P8", p8, 8, 8)
        self.display_box("P4", p4, 4, 4)
        self.display_box("EP", EP, 8, 8)
        self.display_box("IP", IP, 8, 8)
        self.display_box("KEY", KEY_INPUT, 10, 10)

        print("\n\n| ----- SOLVING FOR KEY ----- |\n")
        print("\n| ----- Getting Permutation and Key ----- |\n")
        self.display_box("KEY", KEY_INPUT, 10, 10)

        permuted_key = self.permutate(p10, KEY_INPUT, 10, "P10")

        left_half = permuted_key[:5]
        right_half = permuted_key[5:]

        left_half = self.left_shift(left_half, 1)
        right_half = self.left_shift(right_half, 1)

        combined_key_for_K1 = left_half + right_half

        K1 = self.permutate(p8, combined_key_for_K1, 8, "P8")

        print("\nKey 1: ", "".join(map(str, K1)))

        left_half = self.left_shift(left_half, 2)
        right_half = self.left_shift(right_half, 2)

        combined_key_for_K2 = left_half + right_half
        K2 = self.permutate(p8, combined_key_for_K2, 8, "P8")

        print("\nKey 2: ", "".join(map(str, K2)))

        decision = input("\n\nSingle Hexa Combination or Plaintext? (H/P) \n\n").strip().upper()

        if decision == 'H':
            PT = input("\nEnter your PlainText: ").strip()
            hex_values = [format(ord(ch), 'x') for ch in PT]
            Integer_hex = self.hexToInt(hex_values)
            hex_to_binaries = self.hexToBinaryString(hex_values, 8)

            print("\n\n| ---- Complete Hex to Binary Values From Letters ---- | \n\n")
            print("Hex to Integers: ")
            for i in range(len(hex_values)):
                print(f"{hex_values[i]} = {Integer_hex[i]}")

            print("\nHex to Binaries: ")
            for i in range(len(hex_to_binaries)):
                print(f"{hex_values[i]} = {hex_to_binaries[i]}")

            print("\n\n| ---- Complete Hex to Binary Values From Letters ---- | \n\n")
            print("\n\n| ----- Round 1 ----- |\n\n")
                    
            XorFirstRound = []

            for i in range(len(hex_to_binaries)):
                print(f"------> Letter being Solved {PT[i]} <------")
                hex_holder = self.binaryStringToVector(hex_to_binaries[i])
                IP_Permutate = self.IP_EP_STEP(hex_holder, IP, EP, p4, K1)
                XorFirstRound.append(IP_Permutate)
                print(f"\n------> Letter being Solved {PT[i]} <------\n")
            print("\n\n| ----- Round 1 ----- |")

            print("\n\n| ----- Round 2 ----- |\n\n")
            for i in range(len(hex_to_binaries)):
                print(f"------> Letter being Solved {PT[i]} <------")
                IP_Permutate = self.IP_EP_STEP(XorFirstRound[i], IP, EP, p4, K2)
                print(f"\n------> Letter being Solved {PT[i]} <------\n")
            print("\n\n| ----- Round 2 ----- |\n\n")

        else:
            PT = input("\nEnter your Hexa: ").strip()
            binary_holder = self.binaryStringToVector(PT)
            print("\n\n| ----- Round 1 ----- |\n\n")
            XorFirstRound = self.IP_EP_STEP(binary_holder, IP, EP, p4, K2)
            print("\n\n| ----- Round 1 ----- |\n\n")
            print("\n\n| ----- Round 2 ----- |\n\n")
            self.IP_EP_STEP(XorFirstRound, IP, EP, p4, K2)
            print("\n\n| ----- Round 2 ----- |\n\n")

        print("\n\n| ----- DES ----- |\n\n")
        pause_for_output()

def activity_menu():
    clear_screen()
    n = int(input("Enter the number of activities: "))
    activities = []
    
    for i in range(n):
        start = int(input(f"Start time for Activity {i + 1}: "))
        end = int(input(f"End time for Activity {i + 1}: "))
        activities.append((start, end))
    
    
    print("\nActivity Data:\n")
    print("+-----------+-----------+-----------+")
    print("| Activity  | Start     | End       |")
    print("+-----------+-----------+-----------+")
    for i, activity in enumerate(activities):
        print(f"| {i + 1:<9} | {activity[0]:<9} | {activity[1]:<9} |")
    print("+-----------+-----------+-----------+")
    pause_for_output()
    
    
    activitySelection(activities)
    
def activitySelection(activities):
  
    activities.sort(key=lambda x: x[1])

    
    selected_activities = [activities[0]]
    last_end_time = activities[0][1]

    
    for i in range(1, len(activities)):
        if activities[i][0] >= last_end_time:
            selected_activities.append(activities[i])
            last_end_time = activities[i][1]

    
    print("\nSelected Activities for Maximum Number:")
    print("+-----------+-----------+-----------+")
    print("| Activity  | Start     | End       |")
    print("+-----------+-----------+-----------+")
    for i, activity in enumerate(selected_activities):
        print(f"| {i + 1:<9} | {activity[0]:<9} | {activity[1]:<9} |")
    print("+-----------+-----------+-----------+")
    pause_for_output()

def printJobScheduling(arr, t):
    n = len(arr)
    
    
    arr.sort(key=lambda x: x[2], reverse=True)

    
    result = [False] * t
    job_sequence = ['-'] * t
    total_profit = 0

    for i in range(len(arr)):
        for j in range(min(t - 1, arr[i][1] - 1), -1, -1):
            if not result[j]:
                result[j] = True
                job_sequence[j] = arr[i][0]
                total_profit += arr[i][2]  
                break

    
    print("\nJob Sequence for Maximum Profit:")
    print("+-----+-----+-----+")
    print("| " + "   ".join(job_sequence) + "  |")
    print("+-----+-----+-----+")
    print(f"Maximum Profit: {total_profit}")



def job_sequencing_menu():
    clear_screen()
    n = int(input("Enter the number of jobs: "))
    jobs = []
    
    for i in range(n):
        deadline = int(input(f"Deadline for J{i + 1}: "))
        profit = int(input(f"Profit for J{i + 1}: "))
        jobs.append([f"J{i + 1}", deadline, profit])
    
    
    print("\nJob Data:\n")
    print("+-----------+-----------+-----------+")
    print("| Job       | Deadline  | Profit    |")
    print("+-----------+-----------+-----------+")
    for job in jobs:
        print(f"| {job[0]:<9} | {job[1]:<9} | {job[2]:<9} |")
    print("+-----------+-----------+-----------+")
    
    
    max_time_slots = max(job[1] for job in jobs)

    
    printJobScheduling(jobs, max_time_slots)


class Node:
    def __init__(self, data, freq):
        self.data = data
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def print_codes(self, root, code, huffman_codes, code_lengths):
        if not root:
            return

        if root.data != ' ':
            huffman_codes[root.data] = code
            code_lengths[root.data] = len(code)

        self.print_codes(root.left, code + "0", huffman_codes, code_lengths)
        self.print_codes(root.right, code + "1", huffman_codes, code_lengths)

    def display_table(self, chars, freqs, huffman_codes, code_lengths):
        print("+-----------+-----------+----------------+----------------+----------------+")
        print("| Character | Frequency | Huffman Code   | Total Bits     | Encoded Bits   |")
        print("+-----------+-----------+----------------+----------------+----------------+")

        total_bits = 0
        initial_bits = 0
        total_frequency = 0

        for ch, freq in zip(chars, freqs):
            original_bits = code_lengths.get(ch, 0) 
            encoded_bits = freq * code_lengths.get(ch, 0)  

            print(f"| {ch:<9} | {freq:<9} | {huffman_codes.get(ch, '-'): <14} | {original_bits:<14} | {encoded_bits:<14} |")
            initial_bits += original_bits
            total_bits += encoded_bits
            total_frequency +=freq

        print("+-----------+-----------+----------------+----------------+----------------+")
        print(f"| {'Total':<9} | {total_frequency:<9} | {'':<14} | {initial_bits:<14} | {total_bits:<14} |")
        print("+-----------+-----------+----------------+----------------+----------------+")

    def visualize_tree(self, root):
        os.environ["PATH"] += os.pathsep + '/usr/bin'

        def add_edges(graph, node, counter):
            if node.left:
                left_id = counter[0]
                graph.node(str(left_id), f"{node.left.data}\n{node.left.freq}", shape="circle", style="filled", color="yellow", fontcolor="white", fillcolor="darkviolet", width="0.8", height="0.8", fixedsize="true")
                graph.edge(str(counter[1]), str(left_id), '0', color="blue")
                counter[0] += 1
                add_edges(graph, node.left, [counter[0], left_id])

            if node.right:
                right_id = counter[0]
                graph.node(str(right_id), f"{node.right.data}\n{node.right.freq}", shape="circle", style="filled", color="yellow", fontcolor="white", fillcolor="darkviolet", width="0.8", height="0.8", fixedsize="true")
                graph.edge(str(counter[1]), str(right_id), '1', color="blue")
                counter[0] += 1
                add_edges(graph, node.right, [counter[0], right_id])


        dot = Digraph(node_attr={'margin': '2', 'color': 'lightgrey', 'style': 'filled', 'shape': 'box', 'bgcolor': 'white'}, edge_attr={'color': 'blue'}, graph_attr={'size': '40,40'})


        if root.data == '':
            dot.node('0', f"{root.data}\n{root.freq}", shape="circle", style="filled", color="yellow", fontcolor="white", fillcolor="darkviolet", width="1.0", height="1.0", fixedsize="true", fontweight="bold", fontsize="16", labeljust="c", labelloc="t")
        else:
            dot.node('0', f"{root.data}\n{root.freq}", shape="circle", style="filled", color="yellow", fontcolor="white", fillcolor="darkviolet", width="0.8", height="0.8", fixedsize="true")

        add_edges(dot, root, [2, 0])

  
        dot.render('huffman_tree', format='png', view=True)

    def run_huffman_coding(self):
        n = int(input("Enter the number of characters: "))
        chars = []
        freqs = []

        for i in range(n):
            char = input(f"Enter character {i + 1}: ")
            freq = int(input(f"Frequency for '{char}': "))
            chars.append(char)
            freqs.append(freq)

        min_heap = [Node(chars[i], freqs[i]) for i in range(n)]
        heapq.heapify(min_heap)

        while len(min_heap) > 1:
            left = heapq.heappop(min_heap)
            right = heapq.heappop(min_heap)
            top = Node(' ', left.freq + right.freq)
            top.left = left
            top.right = right
            heapq.heappush(min_heap, top)

        huffman_codes = {}
        code_lengths = {}
        self.print_codes(min_heap[0], "", huffman_codes, code_lengths)

        self.display_table(chars, freqs, huffman_codes, code_lengths)
        self.visualize_tree(min_heap[0])
        
             
def huffman_menu():
    clear_screen()
    huffman_coding = HuffmanCoding()
    huffman_coding.run_huffman_coding()
    pause_for_output()



class Item:
    def __init__(self, profit, weight, index):
        self.profit = profit
        self.weight = weight
        self.index = index
        self.pw_ratio = profit / weight

def fractional_knapsack(capacity, items):
   
    items.sort(key=lambda x: x.pw_ratio, reverse=True)

    total_profit = 0.0
    fractions = [0] * len(items)

    for item in items:
        if capacity == 0:
            break  

      
        if item.weight <= capacity:
            capacity -= item.weight
            total_profit += item.profit
            fractions[item.index] = 1.0  
        else:
          
            fraction = capacity / item.weight
            total_profit += item.profit * fraction
            fractions[item.index] = fraction  
            capacity = 0 

    return total_profit, fractions

def knapsack():
    capacity = float(input("Enter the maximum capacity of the knapsack: "))
    n = int(input("Enter the number of items: "))
    items = []

    for i in range(n):
        profit = float(input(f"Profit for item {i + 1}: "))
        weight = float(input(f"Weight for item {i + 1}: "))
        items.append(Item(profit, weight, i))

    
    print("\nItems:")
    print("+------+--------+--------+-------------+")
    print("| Item | Profit | Weight | P/W Ratio   |")
    print("+------+--------+--------+-------------+")
    for i in range(n):
        print(f"| {i + 1:<4} | {items[i].profit:<6} | {items[i].weight:<6} | {items[i].pw_ratio:<11.2f} |")
    print("+------+--------+--------+-------------+")

    max_profit, fractions = fractional_knapsack(capacity, items)

    print("\nFractions of items carried in the knapsack:")
    for i in range(n):
        print(f"Item {i + 1}: {fractions[i]:.2f}") 

    print(f"\nMaximum Profit: {max_profit:.2f}")
    pause_for_output()

def knapsack_menu():
    clear_screen()
    knapsack()

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []
        self.vertex_map = {}  
        self.reverse_map = {}  
        self.vertex_labels = []  

    def add_edge(self, u, v, w):
        if u not in self.vertex_map:
            idx = len(self.vertex_map)
            self.vertex_map[u] = idx
            self.reverse_map[idx] = u
            self.vertex_labels.append(u) 
        if v not in self.vertex_map:
            idx = len(self.vertex_map)
            self.vertex_map[v] = idx
            self.reverse_map[idx] = v
            self.vertex_labels.append(v) 
        
        self.graph.append([self.vertex_map[u], self.vertex_map[v], w])

    def display_graph(self):
        print("Graph:")
        for u, v, w in self.graph:
            print(f"{self.reverse_map[u]} -- {self.reverse_map[v]} == {w}")
        print()

    def save_graph_data(self, mst):
        data = {
            "vertices": self.vertex_labels,
            "edges": self.graph,
            "mst": mst
        }
        with open('graph_data.json', 'w') as f:
            json.dump(data, f)
        time.sleep(1)  
        open_browser()
        pause_for_output()

    
class Kruskal(Graph):
    def __init__(self, vertices):
        super().__init__(vertices)
        self.parent = []
        self.rank = []
        self.initialize_kruskal()

    def initialize_kruskal(self):
        self.parent = list(range(len(self.vertex_map))) 
        self.rank = [0] * len(self.vertex_map)  

    def find(self, i):
        if self.parent[i] == i:
            return i
        return self.find(self.parent[i])

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if self.rank[root_x] < self.rank[root_y]:   
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

    def run(self):
        self.graph = sorted(self.graph, key=lambda item: item[2])
        self.initialize_kruskal()  
        mst = []
        for u, v, w in self.graph:
            x = self.find(u)
            y = self.find(v)
            if x != y:
                mst.append([u, v, w])
                self.union(x, y)
        self.display_mst(mst)

    def display_mst(self, mst):
        print("Kruskal's MST:")
        for u, v, w in mst:
            print(f"{self.reverse_map[u]} -- {self.reverse_map[v]} == {w}")
        print()
        self.cost(mst)
        self.save_graph_data(mst)

    def cost(self, mst):
        minimum_cost = sum([w for u, v, w in mst])
        print("Edges in the MST:")
        for u, v, weight in mst:
            print(f"{self.reverse_map[u]} -- {self.reverse_map[v]} == {weight}")
        print(f"Minimum Spanning Tree Cost: {minimum_cost}")


class Prims(Graph):
    def __init__(self, vertices):
        super().__init__(vertices)
    
    def run(self, start_vertex):
        
        if start_vertex not in self.vertex_map:
            print(f"Start vertex {start_vertex} not in graph.")
            return

        start_idx = self.vertex_map[start_vertex]
        
        
        mst_edges = []           
        visited = [False] * self.V
        min_heap = [(0, start_idx, start_idx)]  

        total_weight = 0
        
        print(f"Starting Prim's algorithm from vertex: {start_vertex}")
        
        while min_heap:
            weight, u, v = heapq.heappop(min_heap)

           
            if visited[v]:
                continue

           
            visited[v] = True
            if u != v:  
                mst_edges.append((self.reverse_map[u], self.reverse_map[v], weight))
                total_weight += weight
                print(f"Selected edge {self.reverse_map[u]} -- {self.reverse_map[v]} == {weight}")

            for edge in self.graph:
                src, dest, edge_weight = edge
                if src == v and not visited[dest]:
                    heapq.heappush(min_heap, (edge_weight, v, dest))
                    print(f"Considering edge {self.reverse_map[v]} -- {self.reverse_map[dest]} == {edge_weight}")
                elif dest == v and not visited[src]:
                    heapq.heappush(min_heap, (edge_weight, v, src))
                    print(f"Considering edge {self.reverse_map[v]} -- {self.reverse_map[src]} == {edge_weight}")

        print("\nMinimum Spanning Tree (MST) constructed by Prim's Algorithm:")
        for u, v, weight in mst_edges:
            print(f"{u} -- {v} == {weight}")
        print(f"Total weight of MST: {total_weight}")

        self.save_graph_data(mst_edges)

class Boruvka(Graph):
    def __init__(self, vertices):
        super().__init__(vertices)
    
    def run(self):
        print("Starting Borůvka's algorithm")

        num_components = self.V
        cheapest = [-1] * self.V 
        MST_edges = []
        total_cost = 0
        component = list(range(self.V))  

        while num_components > 1:
           
            cheapest = [-1] * self.V
            for u, v, weight in self.graph:
                set_u = component[u]
                set_v = component[v]

                if set_u != set_v: 
                    if cheapest[set_u] == -1 or self.graph[cheapest[set_u][0]][2] > weight:
                        cheapest[set_u] = (u, v, weight)
                    
                    if cheapest[set_v] == -1 or self.graph[cheapest[set_v][0]][2] > weight:
                        cheapest[set_v] = (u, v, weight)
            for i in range(self.V):
                if cheapest[i] != -1:
                    u, v, weight = cheapest[i]
                    MST_edges.append((self.reverse_map[u], self.reverse_map[v], weight))
                    print(f"Selected edge {self.reverse_map[u]} -- {self.reverse_map[v]} == {weight}")
                
                    total_cost += weight

                    
                    component_u = component[u]
                    component_v = component[v]
                    for j in range(self.V):
                        if component[j] == component_v:
                            component[j] = component_u

                    num_components -= 1

        print("\nMinimum Spanning Tree (MST) constructed by Borůvka's Algorithm:")
        for u, v, weight in MST_edges:
            print(f"{u} -- {v} == {weight}")
        print(f"Total cost of MST: {total_cost}")     
        self.save_graph_data(MST_edges)



class Dijkstra(Graph):
    def __init__(self, vertices):
        super().__init__(vertices)
    
    def run(self, start_vertex):
        if start_vertex not in self.vertex_map:
            print(f"Start vertex {start_vertex} not in graph.")
            return

        start_idx = self.vertex_map[start_vertex]
        distances = [float('inf')] * self.V  
        distances[start_idx] = 0  
        previous = [None] * self.V  
        min_heap = [(0, start_idx)]  

        print(f"Starting Dijkstra's algorithm from vertex: {start_vertex}")

        while min_heap:
            current_distance, u = heapq.heappop(min_heap)
    
            if current_distance > distances[u]:
                continue

            for edge in self.graph:
                src, dest, weight = edge
                if src == u:
                    v = dest
                elif dest == u:
                    v = src
                else:
                    continue
                
                distance = current_distance + weight

                if distance < distances[v]:
                    distances[v] = distance
                    previous[v] = u
                    heapq.heappush(min_heap, (distance, v))
                    print(f"Updated distance of {self.reverse_map[v]} to {distance} via {self.reverse_map[u]}")

        print("\nShortest paths from start vertex:")
        for i, d in enumerate(distances):
            print(f"Distance to {self.reverse_map[i]}: {d}")
            pause_for_output()
        print("\nPath reconstruction:")
        for end_idx in range(self.V):
            if distances[end_idx] == float('inf'):
                print(f"No path to {self.reverse_map[end_idx]}")
                continue

            path = []
            current = end_idx
            while current is not None:
                path.append(self.reverse_map[current])
                current = previous[current]
            path.reverse()
            print(f"Path to {self.reverse_map[end_idx]}: {' -> '.join(path)}")

        self.save_graph_data(distances, previous)

    def save_graph_data(self, distances, previous):
        data = {
            "vertices": self.vertex_labels,
            "distances": distances,
            "paths": []
        }

        for end_idx in range(self.V):
            if distances[end_idx] == float('inf'):
                data["paths"].append(f"No path to {self.reverse_map[end_idx]}")
                continue

            path = []
            current = end_idx
            while current is not None:
                path.append(self.reverse_map[current])
                current = previous[current]
            path.reverse()
            data["paths"].append(" -> ".join(path))
            pause_for_output()

        with open('graph_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        time.sleep(1) 
        open_browser()


class Dials(Graph):
    def __init__(self, vertices, max_weight=15):
        super().__init__(vertices)
        self.max_weight = max_weight 

    def run(self, start_vertex):
        if start_vertex not in self.vertex_map:
            print(f"Start vertex {start_vertex} not in graph.")
            return

        start_idx = self.vertex_map[start_vertex]

        distances = {vertex: math.inf for vertex in self.vertex_map}
        distances[start_vertex] = 0
        predecessor = {vertex: None for vertex in self.vertex_map}
        
        buckets = [[] for _ in range(self.max_weight + 1)]

        buckets[0].append(start_vertex)

        print(f"Starting Dial's algorithm from vertex: {start_vertex}")

        while any(buckets):
            for d in range(self.max_weight + 1):
                if buckets[d]:
                    current_vertex = buckets[d].pop(0)  
                    break

            for edge in self.graph:
                u, v, weight = edge
                u_label = self.reverse_map[u]
                v_label = self.reverse_map[v]

                if u_label == current_vertex:
                    neighbor = v_label
                elif v_label == current_vertex:
                    neighbor = u_label
                else:
                    continue 

                if distances[current_vertex] + weight < distances[neighbor]:
                    distances[neighbor] = distances[current_vertex] + weight
                    predecessor[neighbor] = current_vertex
                    new_distance = min(distances[neighbor], self.max_weight)
                    buckets[new_distance].append(neighbor)
                    print(f"Updated distance of {neighbor} to {distances[neighbor]} via {current_vertex}")
                    pause_for_output() 

        total_cost = sum(dist for dist in distances.values() if dist != math.inf)
        print(f"Total cost: {total_cost}")

        graph_data = {
            "vertices": self.vertex_map,
            "edges": [(u, v, w) for u, v, w in self.graph],
            "distances": distances,
            "predecessor": predecessor,
            "mst": [], 
            "total_cost": total_cost  
        }

        with open('dials_graph_data.json', 'w') as f:
            json.dump(graph_data, f)

        print("\nGraph data saved to 'graph_data.json'.")

def prompt_user_for_input():
    V = int(input("Enter the number of vertices: "))
    print("Select algorithm:")
    print("1) Kruskal's Algorithm")
    print("2) Prim's Algorithm")
    print("3) Borůvka's Algorithm")  
    print("4) Dijkstra's Algorithm")  
    print("5) Dial's Algorithm")  
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        graph = Kruskal(V)
    elif choice == 2:
        graph = Prims(V)
    elif choice == 3:
        graph = Boruvka(V)  
    elif choice == 4:
        graph = Dijkstra(V) 
    elif choice == 5:
        graph = Dials(V) 
    else:
        print("Invalid choice")
        return None, None
        
    E = int(input("Enter the number of edges: "))
    print("Enter the edges (vertex1 vertex2 weight):")
    for _ in range(E):
        u, v, w = input("Edge (vertex1 vertex2 weight): ").split()
        graph.add_edge(u, v, int(w))
        
    return graph, choice

def greedy():
    g, choice = prompt_user_for_input()
    
    if g is None:
        return  
    
    g.display_graph()
    
    if choice == 1:
        g.run()  
    elif choice == 2:
        start_vertex = input("Enter the starting vertex: ")
        g.run(start_vertex) 
    elif choice == 3:
        g.run() 
    elif choice == 4:
        start_vertex = (input("Enter the starting vertex: "))
        g.run(start_vertex)  
    elif choice == 5:
        start_vertex = (input("Enter the starting vertex: "))
        g.run(start_vertex)  
    
def main():

    http_process = start_http_server()
    calculator = Calculator()
    des = DES()
    
    try:
        while True:
            clear_screen()
            show_main_menu()
            main_choice = int(input("\nEnter your choice: \n"))
            
            if main_choice == 1:
                calculator.calculator_menu()
            elif main_choice == 2:
                conversion_menu()
            elif main_choice == 3:
                bitwise_menu()
            elif main_choice == 4:
                prime_factorization_menu()
            elif main_choice == 5:
                prime_menu()
            elif main_choice == 6:
                gcd_lcm_menu(calculator)
            elif main_choice == 7:
                egyptian_fraction_menu(calculator)
            elif main_choice == 8:
                calculator.fibonacci_menu()
            elif main_choice == 9:
                calculator.euclidean_menu()
            elif main_choice == 10:
                prime_menu()
            elif main_choice == 11:
                calculator.modular_menu()
            elif main_choice == 12:
                caesar_cipher_menu()
            elif main_choice == 13:
                rsa_menu()
            elif main_choice == 14:
                diffie_hellman_menu()
            elif main_choice == 15:
                aes_menu()
            elif main_choice == 16:
                des.des_menu()
            elif main_choice == 17:
                activity_menu()
            elif main_choice == 18:
                job_sequencing_menu()
            elif main_choice == 19:
                huffman_menu()
            elif main_choice == 20:
                knapsack_menu()
            elif main_choice == 23:
                greedy()
            elif main_choice == 00:
                print("Exiting the program...")
                break
            else:
                print("Invalid choice! Please choose again.")
                pause_for_output()
    except KeyboardInterrupt:
        print("\nProgram interrupted (Ctrl+C). Exiting...")
    finally:    
       
        if http_process:
            terminate_http_server(http_process)



if __name__ == "__main__":
    main()
   