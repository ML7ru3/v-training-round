# GhostTrace

Mô tả nội dung: You are a blue team analyst tasked with investigating a suspected breach in an Active Directory environment named Main.local. The network includes a Domain Controller (DC01 and two client machines (Client02 and Client03)). A user on Client03 received a phishing email, leading to a series of attacks that compromised the domain. Your job is to analyze the provided Windows Event Logs and Sysmon logs from Client02, Client03, and DC01 to reconstruct the attack chain, identify the attacker’s actions, and uncover critical artifacts such as credentials, hashes, and persistence mechanisms.

Sau khi tải và giải nén file đó ra, ta nhận được file Windows Event Logs, có thể đọc qua Window Event Viewer của cả 3 máy: Client 01, 02 và Client 03. Trong những file Event Viewer đó thì ta nhận được logs của từng máy. Nhiệm vụ của chúng ta là xem 3 file đó và trả lời các câu hỏi như trên.

Bối cảnh (dịch ở trên): CLient 03 nhận được phishing email và một loạt chain attack đã tấn công vào máy đó. Nhiệm vụ là đọc file logs đó để reconstruct lại attack chain, xem là attacker muốn làm gì và sau đó nhận được những gì.

## Questions

**What is the name of the malicious phishing attachment downloaded by the user on Client02?**

