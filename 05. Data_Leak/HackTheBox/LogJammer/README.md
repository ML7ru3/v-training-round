# LogJammer

Mô tả đề tài: You have been presented with the opportunity to work as a junior DFIR consultant for a big consultancy. However, they have provided a technical assessment for you to complete. The consultancy Forela-Security would like to gauge your knowledge of Windows Event Log Analysis. Please analyse and report back on the questions they have asked.

Nhiệm vụ của đề bài này là sẽ đọc file Event Log và trả lời các câu hỏi.

## Questions

### When did the cyberjunkie user first successfully log into his computer? (UTC)

Với câu hỏi này, cái thứ ta cần chắc sẽ là đọc file logs ở `Security.evtx` và filter với EventID = 4624, và thế là ta có được câu trả lời.


