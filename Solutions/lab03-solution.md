# Docm : Extract the embedded secret
```bash
olevba YearlyBonus.docm

# Decoding the flag
# 1. 'b' contains the raw decimal values (ASCII) found in the doShenanigans() subroutine.
# 2. the VBA code showed '+3', manual analysis of the output showed the 
#    base values were still offset from the standard 'flag{' structure.
# 3. Applying a total offset of '+10' (3 from VBA + 7 hidden) aligns the bytes to 
#    the correct ASCII characters.
# 4. chr() converts the numbers back to letters, and .join() builds the final string.
python3 -c "b = [77, 101, 109, 34, 22, 111, 101, 107, 22, 104, 91, 87, 98, 98, 111, 22, 97, 100, 101, 109, 22, 111, 101, 107, 104, 22, 109, 87, 111, 22, 87, 104, 101, 107, 100, 90, 22, 87, 22, 76, 56, 57, 22, 99, 87, 89, 104, 101, 22, 89, 94, 87, 98, 98, 91, 100, 93, 91, 36, 0, 0, 79, 101, 107, 104, 22, 92, 98, 87, 93, 22, 95, 105, 48, 22, 92, 98, 87, 93, 113, 105, 107, 89, 94, 85, 99, 42, 89, 104, 38, 85, 99, 107, 89, 94, 85, 109, 38, 109, 23, 115]; print(''.join([chr(x + 10) for x in b if x != 0]))"
# Wow, you really know your way around a VBC macro challenge.Your flag is: flag{such_m4cr0_much_w0w!}
```

# PPTX : Extract the hidden image from Presentation.pptx and recover the source's name and location.
```bash
unzip Presentation.pptx -d Presentation
cd Presentation/ppt/media
exiftool image1.jpg
# ...
# GPS Position                    : 34 deg 12' 39.33", 118 deg 26' 11.15"
# Artist                          : Michael Scott
```

# Audio Steganography : Find the flag
```bash
audacity super_secret_audio.wav
```
- In the track control panel (the box on the left of the audio wave), click the "..." next to the track name (super_secret_audio) and select "Spectogram"

flag{h1dd3n_1n_th3_n01s3}