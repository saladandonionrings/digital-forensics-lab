# What command would we use to list all .txt files in the current directory?

```bash
ls *.txt
```

# What command can we use to read the contents of the file /etc/passwd?

```bash
cat /etc/passwd
```

# What command would search for the string 'Error' in all files in the /var/log directory?

```bash
grep -r Error /var/log
```

# What is the command to calculate the SHA1 hash of /etc/passwd?

```bash
sha1sum /etc/passwd
```

# According to the 'file' command, what is the architecture of /usr/bin/cat?

```text
ELF 64-bit
```

# What command displays all printable strings of length ≥ 8 in /bin/bash?

```bash
strings -n 8 /bin/bash
```

# Based on the provided 'file' output for image.jpg, what is the actual file type?

```text
ELF executable
```

# What command finds files modified in the last 30 minutes in the /home directory?

```bash
find /home -mmin -30
```

# What command displays all active TCP connections on the system?

```bash
netstat -at
```

# Flag in image
For a valid PNG file, the first 8 bytes must be: `89 50 4E 47 0D 0A 1A 0A`, we need to change the first bytes.

```bash
hexedit challenge.png
# copy paste 89 50 4E 47 0D 0A 1A 0A on line 00000000
# save
open challenge.png
# flag{d1g1tal_f0r3ns1cs_101}
```
