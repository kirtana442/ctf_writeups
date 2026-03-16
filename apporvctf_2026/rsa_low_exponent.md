Challenge Overview

The challenge provided an RSA encryption script along with the public parameters and ciphertext.

# enc.py
```bash
from Crypto.Util.number import *

e = 3

while True:
    p = getPrime(1024)
    q = getPrime(1024)
    N = p*q
    phi = (p-1)*(q-1)

    if GCD(phi, e) == 1:
        break

d = inverse(e, phi)

with open("flag.txt", "rb") as f:
    m = bytes_to_long(f.read())

assert m < N 

c = pow(m, e, N)

print("N = ", N)
print("e = ", e)
print("c = ", c)

```
# Understanding the Vulnerability

The script performs standard RSA encryption:

c = m^e mod N

Where:

N = p × q

e = 3

However, the encryption does not use padding.

This introduces a classic RSA weakness when using small public exponents.

The Key Observation

If the plaintext message satisfies:

m^e < N

then the modular reduction does not occur.

Instead of:

c = m^3 mod N

we effectively get:

c = m^3

Which means we can simply compute:

m = ∛c

This attack is known as the RSA cube root attack, a special case of low-exponent RSA vulnerabilities.

Exploiting the Vulnerability

Since the plaintext flag is small compared to the 2048-bit modulus N, the condition holds:

m^3 < N

Therefore:

c = m^3

To recover the message, we compute the integer cube root of the ciphertext.

Exploit Script
```bash
from sympy import integer_nthroot

c = 5959848254333830910624523071067197529743942832931749422613446095759596470869632698744448445022974243192082623200541274049999046045462632699888118125553180389758240097512080800465269924123706310996597928101365256237876736940573969864179631586328876422479408805381027940806738410297399027560825960052951200511768291312433697743253773594534719688371211151318607767527029263892621127356788516738086153844247429662752321125

m, exact = integer_nthroot(c, 3)

flag = m.to_bytes((m.bit_length() + 7) // 8, 'big')
print(flag.decode())
```

# Recovered Flag
```bash
apoorvctf{3ncrypt1ng_w1th_RSA_c4n_b3_4_d4ng3r0us_cl1ff_83}
```

# Real-World Mitigation

Secure RSA implementations prevent this attack by:

Using padding schemes such as
RSAES-OAEP

Padding ensures that the plaintext becomes large and randomized, preventing direct root attacks.

# Conclusion

This challenge demonstrates why raw RSA encryption is insecure when used with:

small public exponents

no padding

The attack works because the ciphertext was simply the cube of the plaintext, allowing direct recovery via integer cube root.