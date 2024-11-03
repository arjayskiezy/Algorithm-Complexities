import os
import math
from sympy import symbols, simplify, Mod
from sympy.parsing.sympy_parser import parse_expr

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_for_output():
    input("\nPress Enter to continue...")   

def show_main_menu():
    print("\nMain Menu:")
    print("1) Calculator")
    print("2) Conversion")
    print("3) Bitwise Operations")
    print("4) Prime Numbers")
    print("5) Factorization")
    print("6) GCD & LCM Calculator")
    print("7) Egyptian Fraction")
    print("8) Fibonacci")
    print("9) Euclidean Algorithm")
    print("10) Sieve of Eratosthenes")
    print("11) Modular Arithmetic")
    print("16) Exit")

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
        while b:
            a, b = b, a % b
        return a

    def calculate_lcm(self, a, b):
        return abs(a * b) // self.calculate_gcd(a, b)
    
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
        """Generate Fibonacci sequence up to N terms."""
        sequence = [0, 1]
        while len(sequence) < n:
            sequence.append(sequence[-1] + sequence[-2])
        return sequence[:n]
        
    def sieve_menu(self):
        """Sieve of Eratosthenes for prime numbers."""
        while True:
            clear_screen()
            print("\nSieve of Eratosthenes Menu:")
            print("1) Generate prime numbers up to a given number")
            print("2) Back to Main Menu")

            choice = int(input("Enter your choice: "))
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
        print("Welcome to the Modular Arithmetic Calculator!")
        try:
            expr = input("Enter an expression (e.g., 3 - 2*5**6 + 3*(4)**5 + 1): ")
            modulus = int(input("Enter the modulus: "))
            result = self.modular_arithmetic(expr, modulus)
            print(f"The result of ({expr}) mod {modulus} is: {result}")
        except ValueError:
            print("Invalid input. Please enter a valid expression and modulus.")
        
    def modular_arithmetic(self, expression, modulus):
        
        parsed_expr = parse_expr(expression)
        
        mod_expr = Mod(simplify(parsed_expr), modulus)
        
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
        return [denominator // numerator]
        

    while numerator != 0:
      
        unit_fraction = -(-denominator // numerator)  
        egyptian_fractions.append(unit_fraction)
        
        
        new_numerator = numerator * unit_fraction - denominator
        new_denominator = denominator * unit_fraction
        
   
        if new_numerator != 0:
            gcd = Calculator.calculate_gcd(0,abs(new_numerator), new_denominator)
            numerator = new_numerator // gcd
            denominator = new_denominator // gcd
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

        conv_choice = int(input("Enter your choice: "))
        
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

def factorization_menu():
    while True:
        clear_screen()
        print("\nFactorization Menu:")
        print("1) Factorize a number")
        print("2) Back to Main Menu")
        
        factor_choice = int(input("Enter your choice: "))
        
        if factor_choice == 2:
            break
        elif factor_choice == 1:
            number = int(input("\nEnter the number to factorize: "))
            factors = find_factors(number)
            print(f"Factors of {number}: {factors}")
            pause_for_output()

def find_factors(n):
    return [i for i in range(1, n + 1) if n % i == 0]

def gcd_lcm_menu(calculator):
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
                print(f"GCD of {a} and {b} is: {calculator.calculate_gcd(a, b)}")
            else:
                print(f"LCM of {a} and {b} is: {calculator.calculate_lcm(a, b)}")
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

def main():
    calculator = Calculator()
    
    while True:
        clear_screen()
        show_main_menu()
        main_choice = int(input("Enter your choice: "))
        
        if main_choice == 1:
            calculator.calculator_menu()
        elif main_choice == 2:
            conversion_menu()
        elif main_choice == 3:
            bitwise_menu()
        elif main_choice == 4:
            prime_menu()
        elif main_choice == 5:
            factorization_menu()
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
        elif main_choice == 16:
            print("Exiting the program...")
            break
        else:
            print("Invalid choice! Please choose again.")
            pause_for_output()

if __name__ == "__main__":
    main()