# Forensics Writeup – Hidden Image in Network Capture

## Challenge Overview

The challenge provided a **PCAP file** containing several TCP packets that appeared to carry normal system log messages. The challenge description hinted:

> *Most packets are status updates but one is different.*

Example messages in the TCP stream:

* Network latency seems stable.
* Did you check the logs?
* Let's push the update tomorrow.
* Backup completed successfully.
* System health check OK.

These messages appear to be **decoy log outputs** intended to hide the real payload within the network traffic.

---

# Step 1 – Inspect Packet Sizes

To locate the anomalous packet, packet lengths were extracted using `tshark`.

```bash
tshark -r challenge.pcap -T fields -e frame.len | sort | uniq
```

Output:

```
5754
66
74
90
92
96
97
98
```

Most packets were small control packets, but **one packet was significantly larger (5754 bytes)**.

Filtering that packet:

```bash
tshark -r challenge.pcap -Y "frame.len == 5754"
```

Result:

```
Frame 14
```

This packet was likely carrying the hidden artifact.

---

# Step 2 – Extract the Packet Payload

The TCP payload of the suspicious packet was extracted.

```bash
tshark -r challenge.pcap -Y "frame.number == 14" -T fields -e data > hex.txt
```

Convert the hex data back into binary:

```bash
xxd -r -p hex.txt > output.bin
```

---

# Step 3 – Identify Embedded File

Running `file` initially showed:

```bash
file output.bin
```

```
output.bin: data
```

However, inspecting the hex revealed content consistent with a **JPEG file**, including recognizable JPEG Huffman table strings such as:

```
456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz
```

These strings are characteristic of **JPEG compression tables**.

---

# Step 4 – Repair the Corrupted JPEG Header

A valid JPEG file begins with the magic bytes:

```
FF D8
```

However, the extracted file began with:

```
3F D8
```

This prevented tools from recognizing it as a valid JPEG.

Using `hexedit`, the first byte was corrected:

```
3F → FF
```

After fixing the header, the file was renamed:

```bash
mv output.bin output.jpg
```

Verification:

```bash
file output.jpg
```

```
JPEG image data
```

---

# Step 5 – Inspect the Image

Opening the image revealed a visible flag:

```
apoorvctf{this_aint_it_brother}
```

However, the text explicitly indicated that this was a **false flag**.

---

# Step 6 – Extract Hidden Data via Steganography

Since the image likely contained hidden data, `steghide` was used to extract embedded content.

```bash
steghide extract -sf output.jpg
```

This revealed the **actual flag** hidden within the image.

---

# Final Flag

```
apoorvctf{b1ts_wh1sp3r_1n_th3_l0w3st_b1t}
```

---

# Key Takeaways

### 1. Decoy Traffic

The repeated log messages in the TCP stream served as **misdirection** to hide the real payload.

### 2. Packet Size Anomaly

Identifying a **large outlier packet** helped locate the embedded artifact.

### 3. File Signature Repair

The extracted payload contained a **corrupted JPEG header**, which had to be manually fixed.

### 4. Steganography

The visible image contained a **decoy flag**, while the real flag was hidden using steganographic techniques and extracted using `steghide`.

---

# Tools Used

* Wireshark
* tshark
* xxd
* hexedit
* file
* steghide

---

# Conclusion

The challenge required analyzing network traffic to locate an anomalous packet, extracting and repairing a corrupted JPEG file, and finally performing steganographic analysis to recover the hidden flag.
