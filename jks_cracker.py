import subprocess
import os
import sys
import itertools
import concurrent.futures

def try_password_combination(jks_file, password):
    try:
        command = f'keytool -list -keystore "{jks_file}" -storepass "{password}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Password found: {password}")
            return password
    except Exception as e:
        print(f"An error occurred: {e}")

    return None

def try_password_combinations(jks_file, password_list):
    if not os.path.exists(jks_file):
        print("JKS file not found.")
        return None
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for r in range(1, len(password_list) + 1):
            for combination in itertools.permutations(password_list, r):
                password = ''.join(combination)
                futures.append(executor.submit(try_password_combination, jks_file, password))
        
        for future in concurrent.futures.as_completed(futures):
            found_password = future.result()
            if found_password:
                return found_password
    
    print("No valid password combination found.")
    return None

# Define the list of passwords to try
passwords_to_try = []

# Path to the JKS file
jks_file_path = ''

found_password = try_password_combinations(jks_file_path, passwords_to_try)

if found_password:
    print(f"Found password: {found_password}")
    input()
else:
    print("None of the password combinations worked.")
    input()
