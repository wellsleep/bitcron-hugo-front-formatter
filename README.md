# bitcron-hugo-front-formatter
从 bitcron 简化的 MD 格式转为标准 Hugo Front Matter 的小脚本

Bitcron 的简化 MD 风格为：

文件名：YYYY-MM-DD-标题
```
title: xxx
author: abc
这里是正文
```

这种简化风格在导入到 Hugo 的时候会出现 Front Matter 不兼容导致导入失败。
本 ~~低劣的~~ 脚本用于批量将简化格式的 MD 文档转为 Hugo 可接受的风格（其实是 jekyll 风格...）：

文件名：YYYY-MM-DD-标题
```
---
title: xxx
author: abc
date: YYYY-MM-DD
---
这里是正文
```

可能尚有考虑不周之处，可自行修改。

Python 3.8.1 上测试通过
