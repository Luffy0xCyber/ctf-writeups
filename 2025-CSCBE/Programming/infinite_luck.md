# Infinite Luck

## Category  
Programming

## Description  
I've made a fair at-home casino game with Python.  
I know it's fair because I use random numbers.  
Math isn't my strongest subject, but I think the odds are about 1 in a million.  
Are you lucky or can you beat the house?

Note: Challenge files were updated on 14/03/2025 at 13:25 (line 11 was changed).

## Files Provided  
- `tester.py` (script I created to generate banner lines for all possible seeds).
- `solver.py` (script I modified to solve the challenge once the seed is found).

The scripts are in the folder **Script_infinite_luck**.

## Write-up  

When connecting to the server using `nc`, a banner is printed before the game begins.  
This banner contains pseudo-random characters that are generated from a fixed seed using Python’s `random` module.

Since the seed affects both the banner and the random number generation, the idea was to recover this seed in order to reproduce the challenge’s internal state.

### Step 1 — Finding the seed

I wrote a script called `tester.py` to generate the banner output for all seeds from 1 to 1,000,000.  
I redirected its output to a file:

```bash
python3 tester.py > seeds.txt
```

Then I copied the first line of the banner shown when connecting to the challenge, and searched for it:

```bash
grep "line-of-the-banner" seeds.txt
```

This gave me the correct seed used by the server.

### Step 2 — Solving the challenge

Once I found the seed, I used my `solver.py` script to:
- Reseed the random number generator
- Rebuild the same banner (for confirmation)
- Generate and print the 1,000 random numbers expected by the server

I then pasted the full output into the challenge input and received the flag.

## Flag  
```
csc{y0u_4r3_4_v3ry_lucky_p3rs0n}
```
