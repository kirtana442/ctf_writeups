**Hint1:** **"Look** **inside** **TCP** **header** **options** **to**
**ﬁnd** **the** **key** **“**

**Description**

In a pixel-drifted, digitally decaying world, a once-powerful server is
failing, struggling to maintain its heartbeat in corrupt network traﬃc.
The server’s last narrative logs and corrupted pixel heart GIF pulses
ﬂicker through fragmented TCP streams. The cipher key "PulseXOR" is
hidden within suspicious TCP header options.

Files Provided:

> ● A **.pcap**ﬁle capturing the network traﬃc from the dying server.
>
> ● The pcap contains multiple TCP streams carrying narrative logs, GIF
> data chunks, and TCP header options with the XOR key

**Solution**

> 1\. Analyze the PCAP with Wireshark or similar: ● Follow TCP streams
> on speciﬁc ports:
>
> ● Narrative system logs on port 514.
>
> ● Pixel heart GIF data chunks on port 8080.
>
> ● XOR cipher key embedded in TCP header options on port 12345. ●
> Filter and isolate these streams for focused examination.
>
> 2\. Reconstruct the GIF:
>
> ● Follow tcp stream on port 8080, the corrupt GIF header (GFI89a
> instead of GIF89a - shows it's a GIF ﬁle)
>
> ● Convert to raw and save as a .gif ﬁle. ● Verify the GIF integrity by
> opening it.

<img src="./images/zhaym2uv.png"
style="width:1.94792in;height:2.64583in" /><img src="./images/2wlzv4r5.png"
style="width:2.33333in;height:2.33333in" />

> 3\. Retrieve the XOR Key:
>
> ● Inspect TCP header options for option number 254.
>
> ● The key "PulseXOR" is transported cleanly without corruption. ●
> Capture this key for further decoding or veriﬁcation.
>
> 4\. Decrypt or Use the Extracted Data:
>
> ● Use the XOR key to decode any additional encrypted data ( 3 base64
> encoded strings in comments of the GIF ﬁle)

<img src="./images/tx51aeyw.png"
style="width:3.29167in;height:2.4375in" /><img src="./images/gj50m4n3.png"
style="width:3.10417in;height:0.63542in" />

**Reference**

[<u>https://www.linkedin.com/pulse/2022-awake-pcap-ctf-challenge-ighor-tavares</u>](https://www.linkedin.com/pulse/2022-awake-pcap-ctf-challenge-ighor-tavares)
