import requests

# 配置
GITLAB_URL = 'https://dev.cgdg.com:50023/api/v4'
PRIVATE_TOKEN = 'glpat-avHi145MtTR2xKNnNV7y'  # 替换为您的GitLab API访问令牌

def check_token_permissions():
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    url = f'{GITLAB_URL}/user'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_info = response.json()
        print("用户名:", user_info['username'])
        print("权限级别:", user_info['state'])
        print("访问令牌有效。")
    else:
        print("访问令牌无效或权限不足。")
        print("状态码:", response.status_code)
        print("响应内容:", response.text)

if __name__ == '__main__':
    check_token_permissions()
