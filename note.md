### 本地运行

添加环境变量后运行autocheckin.py 方法如下

###  **方法一：在命令行中运行脚本时临时设置**

适合临时运行程序：

```bash
TOKEN="your_token_value" DEBUG="True" python your_script.py
```

这样设置的环境变量只在这一条命令中有效。

------

### ✅ **方法二：在 `.env` 文件中设置 + 使用 `python-dotenv` 读取（推荐）**

这种方式更方便调试和管理。

1. 安装 `python-dotenv`：

```bash
pip install python-dotenv
```

1. 在你的项目目录下创建一个 `.env` 文件，内容如下：

```bash
ini复制编辑TOKEN=your_token_value
DEBUG=True
```

1. 修改你的 `main` 函数文件，在开头导入并加载 `.env` 文件：

```bash
from dotenv import load_dotenv
load_dotenv()
```

完整例子变成这样：

```bash
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    token = os.getenv("TOKEN")
    debug = os.getenv("DEBUG", False)
    configure_logger(debug=debug)
    ...
```

------

### ✅ **方法三：通过系统环境变量永久设置（适合长期使用）**

#### Linux / macOS（例如放在 `.bashrc` 或 `.zshrc`）:

```bash
export TOKEN=your_token_value
export DEBUG=True
```

然后运行：

```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

#### Windows（CMD 示例）:

```bash
set TOKEN=your_token_value
set DEBUG=True
python your_script.py
```