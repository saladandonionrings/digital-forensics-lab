# Lab09

```bash
❯ tar xvf secrets.tar

# grep
❯ grep -i "flag" 27b200a787553581f1a9e42556052f7e38113539224093834b7f48a03693c879.json
# flag3=flag{3nv1r0nm3nt_v4r1abl3s_1ns1d3_c0nta1n3rs}
# flag{th1s_w4s_4n0th3r_34sy_0n3}
# flag{th1s_w4s_4n_34sy_0n3}

# layer flag
❯ find . -name "layer.tar" -exec tar -xOf {} flag2-part1.txt \; 2>/dev/null

❯ find . -name "layer.tar" -exec tar -xOf {} flag2-part2.txt \; 2>/dev/null
# flag{dr34d_1t_run_f0r_1t_d3st1ny_4rr1v3s_4ll_7h3_s4m3}

# corrupted secret
❯ find . -name "layer.tar" -exec tar -xOf {} var/log/secret.txt \; 2>/dev/null
ZmxhZ3tjMG5ncjR0c18wbl9mMW5kMW5nX3RoM19uMHRfczBfdzNsbF9oMWRkM25fczNjcjN0fQ==

❯ echo "ZmxhZ3tjMG5ncjR0c18wbl9mMW5kMW5nX3RoM19uMHRfczBfdzNsbF9oMWRkM25fczNjcjN0fQ" | base64 -d
# flag{c0ngr4ts_0n_f1nd1ng_th3_n0t_s0_w3ll_h1dd3n_s3cr3t}
```