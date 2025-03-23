# Our encryption is secret


## Description  
In this challenge, participants are given a series of password-protected ZIP files. Each archive contains a text file with a single character, and the goal is to extract all characters to recover the final flag. However, the password for each ZIP file is not given and must be computed.

## Scenario  
You and your friend communicate using ZIP archives secured with numeric passwords. While this method is convenient and portable, it's slowly destroying your numpads… Maybe it’s time to reverse engineer this pattern and retrieve the hidden message.

## Write-up  
The challenge folder contains 19 ZIP files: `0.zip`, `1.zip`, ..., `18.zip`. Each ZIP file contains a file named `character.txt` that holds a single letter.

At first, we try manually extracting `0.zip` and `1.zip`. We find that:
- `0.zip` is unlocked with password `1`
- `1.zip` is unlocked with password `9`

From `2.zip` onwards, the password is not obvious, but after some experimentation and analysis, a pattern emerges.

Each password appears to be derived using a recursive formula involving **odd prime numbers**, with exponentiation and multiplication:
- Start with base password `9` and base multiplier `2`
- For each step `i ≥ 2`, use the i-th odd prime number `p` to compute:

```
password = previous_password * (p ** 3) + (base ** 3)
base = base * p
```

The list of odd primes used is:

```
[3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
```

Using this pattern, we can compute the correct password for each ZIP file, extract the `character.txt`, and reconstruct the flag.

## Solve script  

```python
import os
import pyzipper

# Folder containing the ZIP files
directory = "challenge_files_our_encryption_is_secret"
zip_files = [os.path.join(directory, f"{i}.zip") for i in range(19)]

# List of odd prime numbers
prime_impaire = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]

# Store extracted characters
extracted_letters = []

def extract_zip(zip_file, password):
    try:
        with pyzipper.AESZipFile(zip_file) as zf:
            zf.pwd = str(password).encode('utf-8')
            with zf.open('character.txt') as f:
                return f.read().decode('utf-8').strip()
    except Exception as e:
        print(f"Failed to extract {zip_file} with password {password}: {e}")
        return None

def main():
    for i in range(19):
        if i == 0:
            password = 1
        elif i == 1:
            password = 9
        else:
            temp_password = 9
            temp_base = 2
            for k in range(2, i + 1):
                idx = k - 2
                prime = prime_impaire[idx]
                temp_password = temp_password * (prime ** 3) + (temp_base ** 3)
                temp_base *= prime
            password = temp_password

        letter = extract_zip(zip_files[i], password)
        if letter:
            extracted_letters.append(letter)

    print("Flag:", ''.join(extracted_letters))

if __name__ == '__main__':
    main()
```

## Flag  
```
CSC{Y0u_d3c0mpR3ss3d_my_h34rt}
```
