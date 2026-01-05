# What IP address does the attack seem to be originating from?
```bash
unzip logs.zip
cd apache2
cat access.log
# 192.168.0.106
```
# Which vulnerabilities were exploited?
```bash
cat access.log
# 192.168.0.106 - - [16/Feb/2023:01:35:23 +0500] "GET /view.php?image=../../../etc/passwd HTTP/1.1" 200 203 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
# ...
# 192.168.0.106 - - [16/Feb/2023:01:37:01 +0500] "POST /users.php HTTP/1.1" 200 1050 "-" "sqlmap/1.6.11#stable (https://sqlmap.org)"
```

# What web browser and its version the attacker used ?
```bash
cat access.log
# "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
```

# What is the name and version of the automated tool they used ?
```bash
cat access.log
# sqlmap
```

# Which file was the attacker trying to access but couldn't due to limited server access?
```bash
cat modsec_audit.log
# 16/Feb/2023:01:35:30.820725 +0500
```

# An important secret was compromised. Can you figure it out? Hint: The secret you're looking for is not in a .sql or a .php file.
```bash
cat modsec_audit.log
# 16/Feb/2023:01:37:25.573810 +0500
```

# What is the flag in the message left for the administrator ?

```bash
cat modsec_audit.log
# 16/Feb/2023:01:38:28.659927 +0500
```