# In Crypto We Trust 

## Category  
Cryptography

## Description  
You're a cryptanalyst in pain, examining the encrypted data,  
searching for subtle patterns used by this black hat.  
What could it be?

## Files Provided  
- `k3y` (a file containing the ciphertext as byte pairs)

## Write-up  

The file contains a ciphertext where each **character of the plaintext is hidden across pairs of bytes**.  
Knowing that the flag starts with `CSC{`, I used the known ASCII bytes for these characters:

```
C  -> 0x43  
S  -> 0x53  
C  -> 0x43  
{  -> 0x7b
```

By XORing the ciphertext byte pairs with the known plaintext start, I recovered a **repeating 4-byte key**:

```
[0x58, 0x33, 0x75, 0x35]
```

I then XORed each byte of the ciphertext using this key in a loop:

```python
# key = [0x58, 0x33, 0x75, 0x35]
# For every pair (cipher1, cipher2):
#   plaintext_char = cipher1 XOR key[i % 4]
```

This gave me the decoded ASCII:

```
CSC{Th1s_k3Y_W34_34sY_T0_Br34k}
```

## Flag  
```
CSC{Th1s_k3Y_W34_34sY_T0_Br34k}
```
