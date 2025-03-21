# DNS Scavenger Hunt 

## Category  
DNS

## Description  
> I sat up high, then took a dive,  
> Yet my message must survive.  
> Scrambled words, locked up tight,  
> Hidden well, out of sight.  
> A secret path, a site to see,  
> Find my letter at justnuisance.be!  
> Who am I?

(Note: You need to use the DNS server specified below.)

DNS Server:
```
dig @dns_scavenger_hunt.challenges.cybersecuritychallenge.be -p 53
```

## Write-up  

I started by querying all available records for the domain:

```
dig @dns_scavenger_hunt.challenges.cybersecuritychallenge.be -p 53 justnuisance.be ANY
```

Among the many records, I noticed a **submission TCP service**, hinting at a mail server.

I then queried the SRV records to get more details:

```
dig @dns_scavenger_hunt.challenges.cybersecuritychallenge.be _submission._tcp.justnuisance.be -t SRV
```

This confirmed that the domain was hosting an SMTP service.

Following the trail, I played around with the DNS records and eventually queried:

```
dig @dns_scavenger_hunt.challenges.cybersecuritychallenge.be _666._tcp.mail.justnuisance.be -t TLSA
```

This gave the following TLSA record:

```
_666._tcp.mail.justnuisance.be. 86400 IN TLSA 3 1 1 4353437B53633476336E36335F376831735F444E355F5337796C337D
```

The last part looked like a hex-encoded string.

## Extracting the Flag

Hex:
```
4353437B53633476336E36335F376831735F444E355F5337796C337D
```

I converted it to ASCII using:

```python
bytes.fromhex("4353437B53633476336E36335F376831735F444E355F5337796C337D").decode()
```

Result:
```
CSC{Sc4v3n63_7h1s_DN5_S7yl3}
```

## Flag  
```
CSC{Sc4v3n63_7h1s_DN5_S7yl3}
```
