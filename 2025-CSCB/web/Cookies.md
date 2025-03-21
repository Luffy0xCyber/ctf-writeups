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

We reverse engineered the signature logic from the TypeScript code and identified the following signature generation process:

```
signature = (((value ^ secret_key) ^ timestamp) ^ secret_key)
```

Since XOR is commutative and associative, we simplify:

```
signature = value ^ timestamp
```

This is because:
```
(value ^ secret ^ timestamp ^ secret) = value ^ timestamp
```

So, to forge a session as `admin`:
1. Extract the timestamp from the existing cookie.
2. XOR `admin` with the timestamp string to generate the new signature.
3. Reconstruct the cookie as:

```
admin|timestamp|new_signature
```

### Python Script

```python
def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes([x ^ y for x, y in zip(a, b)])

# Original values
old_value = b"guest"
new_value = b"admin"
timestamp = b"2025-03-14T12:09:19.838Z"

# Reproduce the original signature by XORing guest with timestamp
# Then, generate the new signature by XORing admin with the same timestamp
# Padding the shorter input if necessary
def pad(b1, b2):
    length = max(len(b1), len(b2))
    return b1.ljust(length, b'_'), b2.ljust(length, b'_')

old_value_p, timestamp_p = pad(old_value, timestamp)
original_signature = xor_bytes(old_value_p, timestamp_p)

new_value_p, _ = pad(new_value, timestamp)
new_signature = xor_bytes(new_value_p, timestamp_p)

# Convert signature to base64 if required by the server (depends on implementation)
import base64
sig_b64 = base64.b64encode(new_signature).decode()

print(f"Forged cookie: admin|{timestamp.decode()}|{sig_b64}")
```

## Final Forged Cookie  
```
admin|2025-03-14T12:09:19.838Z|<generated_signature>
```

Replace the session cookie in your browser with the forged one to access the protected page.

## Flag  
```
CSC{I_LOV3_COOK13S}
```
