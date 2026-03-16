**Write-up:** **Strike** **Bank** **Employee** **Portal**
**Exploitation**

**1.** **Information** **Gathering** **&** **Reconnaissance**

The assessment began with analysis of a BeVigil report related to the
**Strike** **Bank** Android application. The report exposed multiple
sensitive assets, which collectively defined the initial attack surface.

**Leaked** **Assets** **Identified:**

> ● **Firebase** **URL**[**:**
> <u>https://strike-projectx-1993.firebaseio.com/</u>](https://strike-projectx-1993.firebaseio.com/)
> ● **Auth** **token** **in** **report** **base64** **decoded** **to**
>
> **GitHub** **Personal** **Access** **Token** **(PAT):**
> github_pat_11B2PT...
>
> ● **Server** **IP:** 15.206.47.5:8080 (identified from Dockerfile
> comments)
>
> <img src="./images/3ceckbfn.png" style="width:6.5in;height:1.46875in" /><img src="./images/gfykd2hk.png" style="width:6.5in;height:2.61458in" />
●
> **Initial** **Credentials:** support@strikebank.com / newPassword
> (observed in report logs)

<img src="./images/m5iflorj.png" style="width:6.5in;height:0.96875in" />

**2.** **GitHub** **Asset** **Analysis**

The exposed GitHub Personal Access Token was used to interact with the
GitHub API and enumerate private repositories associated with the
developer account. This led to the discovery of a repository containing
the source code for the bank’s employee portal.

Initial inspection of login.php showed that sensitive values had been
sanitized in the current version of the code:

<img src="./images/2pfczlna.png" style="width:6.5in;height:2.86458in" />
\$logins
= array('' =\> ''); // Credentials removed \$secret = ''; // Secret
removed

<img src="./images/qqogocmr.png" style="width:6.5in;height:3.5in" /><img src="./images/t1jd01fz.png" style="width:6.5in;height:1.16667in" />

Revealed ip and port from docker file

**3.** **Git** **Commit** **History** **Forensics**

Given that the production server remained active, it was likely running
an older build of the application or that repository sanitization had
been incomplete. Commit history was audited using the GitHub API to
identify previous versions of the code.

**Relevant** **Commits:**

> ● **c1d8478:** “Add login functionality with JWT authentication.” ●
> **aa5bb88:** “Change default JWT secret to an empty string.”

Reviewing commit c1d8478 revealed previously hardcoded sensitive data
that had not been purged from the repository history.

**Recovered** **Secret:**

> <img src="./images/fjrjxtmv.png" style="width:6.5in;height:0.30208in" /><img src="./images/2iyhx20d.png" style="width:6.5in;height:2.48958in" /><img src="./images/sjqrztcr.png" style="width:6.5in;height:2.03125in" /><img src="./images/fk2yhq4h.png" style="width:6.5in;height:1.94792in" />●
> **JWT** **Signing** **Secret:** Str!k3B4nkSup3rs3cr37

<img src="./images/bupj1igq.png" style="width:6.5in;height:3.41667in" />

**4.** **JWT** **Forgery** **&** **Privilege** **Escalation**

Analysis of index.php on the live server showed that authentication
relied on a JWT stored in the auth cookie. Authorization logic included
the following conditional check:

if (\$payload-\>username === 'admin') { echo \$flag;

}

Because the JWT used the HS256 algorithm and the signing secret was
known, it became possible to generate a valid token with an arbitrary
payload. This allowed impersonation of the admin user without requiring
valid credentials.

A PHP script (solve.php) was created to replicate the server’s Base64URL
encoding and HMAC-SHA256 signing process. The payload
{"username":"admin"} was signed using the recovered JWT secret.

<img src="./images/qnce34xa.png" style="width:6.5in;height:2.05208in" /><img src="./images/2oqnmiff.png" style="width:6.5in;height:1.11458in" />

**5.** **Final** **Execution**

The forged JWT was injected into the auth cookie and sent to the
application using curl.

curl -v http://15.206.47.5:8080/index.php --cookie "auth=\[FORGED_JWT\]"

The server verified the token signature using the compromised secret,
trusted the forged admin identity, and returned the protected flag in
the HTTP response.

**6.** **Lessons** **Learned**

> ● **Secrets** **Management:** Secrets must never be hardcoded in
> source code, even temporarily. Environment variables or dedicated
> secret managers should be used instead.
>
> ● **Git** **History** **Persistence:** Removing a secret in a later
> commit does not eliminate it from version history. Tools such as
> git-filter-repo or **BFG** **Repo-Cleaner** are required to fully
> purge sensitive data.
>
> ● **JWT** **Security:** JWT signing secrets should be long, randomly
> generated, securely stored, and rotated periodically to reduce the
> risk of token forgery.
