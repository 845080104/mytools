# GitLab Clone Tool

一个用于克隆GitLab项目的Python脚本工具。

## 介绍

该工具使用GitLab API获取指定组及其子组中的所有项目，并克隆这些项目到本地目录中。您可以通过配置文件设置克隆的最大项目数量以及是否跳过已存在的项目。

## 功能

- 使用GitLab API获取项目列表
- 支持克隆指定组及其子组中的所有项目
- 支持最大克隆项目数量限制
- 支持跳过已存在的项目
- 支持克隆失败时的重试机制

## 配置

您可以通过修改脚本中的以下变量来配置工具：

- `GITLAB_URL`: GitLab API的基础URL
- `GROUP_ID`: 要克隆的GitLab组ID
- `PRIVATE_TOKEN`: GitLab API访问令牌
- `CLONE_DIR`: 克隆项目到的本地目录
- `MAX_CLONE_COUNT`: 最大克隆项目数量
- `SKIP_EXISTING_PROJECTS`: 是否跳过已存在的项目目录
- `CLONE_DELAY`: 每次克隆后的延迟时间（秒）
- `MAX_RETRIES`: 克隆失败时的最大重试次数

## 使用方法

### 安装依赖

在运行脚本之前，请确保已安装所需的Python库。您可以使用以下命令安装这些库：

\`\`\`sh
pip install requests
\`\`\`

### 修改配置

修改 `clone_projects.py` 脚本中的配置变量以符合您的需求：

\`\`\`python
GITLAB_URL = 'https://dev.cgdg.com:50023/api/v4'
GROUP_ID = '28'  # 替换为您的组ID
PRIVATE_TOKEN = 'your-new-private-token'  # 替换为您的GitLab API访问令牌
CLONE_DIR = 'C:\\Users\\liuju\\Desktop\\allCode'  # 项目克隆到的目录
MAX_CLONE_COUNT = 10  # 最大克隆项目数量
SKIP_EXISTING_PROJECTS = True  # 是否跳过已存在的项目目录
CLONE_DELAY = 5  # 每次克隆后的延迟时间（秒）
MAX_RETRIES = 3  # 克隆失败时的最大重试次数
\`\`\`

### 运行脚本

打开终端或命令行工具，导航到脚本所在的目录，运行以下命令：

\`\`\`sh
python clone_projects.py
\`\`\`

## 注意事项

- 请确保您的GitLab访问令牌具有足够的权限（例如，`Developer` 级别或更高）。
- 如果您的GitLab账户启用了双因素认证（2FA），请确保使用的是个人访问令牌（Personal Access Token），而不是用户名和密码。

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
"""