import os
import time
import requests
import subprocess
from requests.exceptions import RequestException

# 配置
GITLAB_URL = 'https://dev.cgdg.com:50023/api/v4'
GROUP_ID = '28'  # 替换为您的组ID
PRIVATE_TOKEN = 'glpat-avHi145MtTR2xKNnNV7y'  # 替换为您的新GitLab API访问令牌
CLONE_DIR = 'C:\\Users\\liuju\\Desktop\\allCode'  # 项目克隆到的目录
MAX_CLONE_COUNT = 999  # 最大克隆项目数量
SKIP_EXISTING_PROJECTS = True  # 是否跳过已存在的项目目录
CLONE_DELAY = 5  # 每次克隆后的延迟时间（秒）
MAX_RETRIES = 2  # 克隆失败时的最大重试次数

# 创建克隆目录
if not os.path.exists(CLONE_DIR):
    os.makedirs(CLONE_DIR)

# 获取组下所有项目，包括子组的项目
def get_projects(group_id):
    projects = []
    page = 1
    while True:
        url = f'{GITLAB_URL}/groups/{group_id}/projects?page={page}&per_page=100'
        headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            projects.extend(data)
            page += 1
        except RequestException as e:
            print(f"获取项目时出错: {e}")
            break
    return projects

# 递归获取子组下的所有项目
def get_all_projects(group_id):
    projects = get_projects(group_id)
    subgroups_url = f'{GITLAB_URL}/groups/{group_id}/subgroups'
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    try:
        response = requests.get(subgroups_url, headers=headers)
        response.raise_for_status()
        subgroups = response.json()
        for subgroup in subgroups:
            projects.extend(get_all_projects(subgroup['id']))
    except RequestException as e:
        print(f"获取子组时出错: {e}")
    return projects

# 替换URL中的IP地址为域名
def replace_ip_with_domain(url, old_ip, new_domain):
    if old_ip in url:
        return url.replace(old_ip, new_domain)
    return url

# 克隆项目
def clone_projects(projects, max_clone_count, skip_existing):
    cloned_count = 0
    for project in projects:
        if cloned_count >= max_clone_count:
            print(f"达到最大克隆项目数量: {max_clone_count}")
            break
        
        project_name = project['name']
        https_url = project['http_url_to_repo']
        
        # 替换URL中的IP地址为域名
        https_url = replace_ip_with_domain(https_url, 'http://10.149.4.154:8005', 'https://dev.cgdg.com:50023')
        
        project_dir = os.path.join(CLONE_DIR, project_name)
        
        # 检查项目目录是否已经存在
        if skip_existing and os.path.exists(project_dir) and os.listdir(project_dir):
            print(f"跳过 {project_name}，目录已经存在且不为空。")
            continue
        
        # 创建项目目录
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        
        print(f"正在克隆 {project_name} 到 {project_dir}...")
        
        # 重试机制
        retries = 0
        while retries < MAX_RETRIES:
            env = os.environ.copy()
            env["GIT_ASKPASS"] = "echo"
            env["GIT_USERNAME"] = "your-username"
            env["GIT_PASSWORD"] = PRIVATE_TOKEN
            result = subprocess.run(['git', 'clone', https_url, project_dir], capture_output=True, text=True, env=env)
            if result.returncode == 0:
                print(f"成功克隆 {project_name}")
                break
            else:
                print(f"克隆 {project_name} 时出错: {result.stderr}")
                retries += 1
                if retries < MAX_RETRIES:
                    print(f"重试 {project_name} ({retries}/{MAX_RETRIES})...")
                    time.sleep(CLONE_DELAY)
                else:
                    print(f"克隆 {project_name} 失败，重试次数已用完。")
        
        cloned_count += 1
        time.sleep(CLONE_DELAY)  # 每次克隆后添加延迟

# 主函数
def main():
    projects = get_all_projects(GROUP_ID)
    if not projects:
        print("未找到任何项目或发生错误。")
        return
    clone_projects(projects, MAX_CLONE_COUNT, SKIP_EXISTING_PROJECTS)
    print("所有项目均已成功克隆。")

if __name__ == '__main__':
    main()
