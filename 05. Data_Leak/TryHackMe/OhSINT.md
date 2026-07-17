# OhSINT

Trong Room này cho trước một hình ảnh và nhiệm vụ của room này là chúng ta phải trích xuất những thông tin bên ngoài từ chính bức ảnh đó.

![](../assets/WindowsXP_1551719014755.jpg)

## Questions

**What is this user's avatar of?** - cat

Khi sử dụng `exiftool` ta biết được người chụp bức ảnh chính là OWoodflint. Khi mà tra tên người này trên google thì ra được một tài khoản X (hoặc là Twitter) với avatar là một con mèo.

![](../assets/question1_ohsint.png)

Đây là kết quả sau khi search:

![](../assets/poc1_ohsint.png)

**What city is this person in?** - London

Khi vào trang cá nhân của người dùng trên ta nhận được một đoạn code như sau: `Bssid: B4:5D:50:AA:86:41`.

![](../assets/poc2_ohsint.png)

Tiếp tục tra đoạn code nó lên trên google thì ta được địa chỉ chính xác của người dùng đó ở đâu.

![](../assets/BSSIDcode.png)

**What is the SSID of the WAP he connected to?**

Sau khi tra cứu thì cụm từ "SSID of the WAP" thì nó chỉ là public name của Wifi người dùng đó.
