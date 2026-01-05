# What are the MD5 and SHA1 hashes of the note.txt file?
```bash
wget https://github.com/al3ks1s/AD1-tools/releases/download/v1.0/ad1tools_1.0.0-1_amd64.deb
sudo dpkg -i ad1tools_1.0.0-1_amd64.deb

sudo ad1mount -i files/Image.ad1 -m /mnt/lab06

cd /mnt/lab06
md5sum note.txt && sha1sum note.txt
# c91e969e9184267c35ddc3ff45f795d3  note.txt
# c61dce75ba83f186471297e2e0568ddd0cefe022  note.txt
```
# What's the MFT record number of the note.txt file? The answer may vary depending on the method used.

```bash
pip install analyzeMFT
analyzemft -f \$MFT -o mft-report.csv
grep -ai "note.txt" mft-report.csv
# 40
```

# Can you determine the parent directory of the file named $Txf? You can use either analyzeMFT or MFTECmd to inspect the contents of the $MFT file to answer this question.
```bash
open mft-report.csv
# Line 25, column 6 : Record ID of parent : 27
# Record ID 27 : $RmMetadata
```

# The meme.jpeg image was originally downloaded from a twitter URL. Can you use MFTECmd to determine the original URL?
```bash
dd if=/mnt/lab06/\$MFT bs=1024 skip=39 count=1 | strings
# HostUrl=https://pbs.twimg.com/media/FadAHVAUUAAVp2Q?format
```

# Can you analyze the $Boot file and determine the volume serial number in raw hexadecimal format?
```bash
sudo dd if=/mnt/lab06/\$Boot bs=1 skip=72 count=8 | hexdump -C
# 7f 7a 42 44 b7 42 44 f6
```