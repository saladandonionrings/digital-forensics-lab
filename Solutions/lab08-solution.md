# Clipboard flag
```bash
vol.py -f memdump_challenge.mem --profile=Win7SP1x64 clipboard
# flag{s0m3_stuff_c0p13d_1n_th3_cl1pb0ard}
```

# Internet flag 

```bash
vol.py -f memdump_challenge.mem --profile=Win7SP1x64 iehistory
# flag{1nt3rn3t_3xpl0r3r_h1st0ry_1n_m3m0ry_dump}
```

# Environment variable flag
```bash
vol.py -f memdump_challenge.mem --profile=Win7SP1x64 envars | grep flag
# flag{3nv1r0nm3nt_v4r14bl3_c4n_4ls0_b3_3xtr4ct3d_fr0m_m3m0ry_dump}
```

# Command execution flag
```bash
vol.py -f memdump_challenge.mem --profile=Win7SP1x64 consoles
# C:\Users\w>echo ZmxhZ3tnMDBkXzBsZF9jMG5zMGwzX2gxc3Qwcnl9 > flag.txt && notepad.exe flag.txt
echo "ZmxhZ3tnMDBkXzBsZF9jMG5zMGwzX2gxc3Qwcnl9" | base64 -d
# flag{g00d_0ld_c0ns0l3_h1st0ry}
```

# MSPaint flag
```bash
# find pid of paint
vol.py -f memdump_challenge.mem --profile=Win7SP1x64 pslist | grep -i mspaint
# 2768
vol.py -f memdump_challenge.mem --profile=Win7SP1x64 memdump -p 2768 -D ./
```