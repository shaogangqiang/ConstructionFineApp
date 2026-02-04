"""
GitHub 自动化上传脚本
安全提示：Token 只保存在你的电脑上，不会上传到任何地方
"""
import os
import requests

# ==================== 配置区域 ====================

# 你的 GitHub Token（替换成你刚生成的）
GITHUB_TOKEN = "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"

# 你的 GitHub 用户名（替换成你的）
GITHUB_USERNAME = "your-username"

# 仓库名称
REPO_NAME = "ConstructionFineApp"

# 项目文件所在路径（确认这个路径）
PROJECT_PATH = r"C:\Users\l\clawd\ConstructionFineApp"

# =======================================================

def create_repo():
    """创建仓库"""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": REPO_NAME,
        "description": "施工现场罚款系统 - 安卓APP",
        "private": False,
        "auto_init": False
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            print(f"✅ 仓库创建成功！")
            return True
        elif response.status_code == 422:
            print(f"⚠️  仓库已存在，继续上传文件...")
            return True
        else:
            print(f"❌ 创建仓库失败：{response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误：{str(e)}")
        return False

def upload_file(file_path, content=None):
    """上传文件"""
    # 获取相对路径
    rel_path = os.path.relpath(file_path, PROJECT_PATH)
    
    # GitHub API 路径需要用 Unix 风格
    gh_path = rel_path.replace("\\", "/")
    
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{gh_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 读取文件内容
    if content is None:
        with open(file_path, 'rb') as f:
            content = f.read()
    
    import base64
    content_base64 = base64.b64encode(content).decode()
    
    data = {
        "message": f"Upload {gh_path}",
        "content": content_base64
    }
    
    try:
        response = requests.put(url, json=data, headers=headers)
        if response.status_code in [200, 201]:
            print(f"✅ 上传成功：{gh_path}")
            return True
        else:
            print(f"❌ 上传失败 {gh_path}：{response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误：{str(e)}")
        return False

def upload_directory():
    """上传整个目录"""
    if not os.path.exists(PROJECT_PATH):
        print(f"❌ 项目路径不存在：{PROJECT_PATH}")
        return False
    
    print(f"\n📁 开始上传项目文件...")
    print(f"项目路径：{PROJECT_PATH}\n")
    
    success_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(PROJECT_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            
            # 跳过不需要上传的文件
            skip_files = ['.pyc', '__pycache__', '.DS_Store']
            if any(skip in file for skip in skip_files):
                continue
            
            total_count += 1
            if upload_file(file_path):
                success_count += 1
    
    print(f"\n📊 上传完成！")
    print(f"成功：{success_count}/{total_count}")
    print(f"失败：{total_count - success_count}/{total_count}")
    
    return success_count > 0

def main():
    """主函数"""
    print("=" * 50)
    print("   GitHub 自动化上传脚本")
    print("=" * 50)
    print(f"\n👤 用户名：{GITHUB_USERNAME}")
    print(f"📦 仓库名：{REPO_NAME}")
    print(f"📁 项目路径：{PROJECT_PATH}")
    print()
    
    # 提示用户修改配置
    if GITHUB_USERNAME == "your-username":
        print("⚠️  请先修改脚本中的配置：")
        print("   - GITHUB_USERNAME：你的GitHub用户名")
        print("   - 确认 PROJECT_PATH 正确")
        print("\n修改后重新运行脚本！")
        return
    
    input("按回车键开始...")
    print()
    
    # 第1步：创建仓库
    print("📝 第1/2步：创建仓库...")
    if not create_repo():
        return
    
    print()
    
    # 第2步：上传文件
    print("📤 第2/2步：上传文件...")
    print()
    if upload_directory():
        print("\n" + "=" * 50)
        print("   ✅ 所有操作完成！")
        print("=" * 50)
        print(f"\n📱 接下来的步骤：")
        print(f"   1. 访问你的仓库：https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
        print(f"   2. 点击顶部的 'Actions' 标签")
        print(f"   3. 等待3-5分钟自动编译")
        print(f"   4. 编译完成后下载 APK")
        print()
    else:
        print("\n❌ 上传失败，请检查：")
        print("   1. Token 是否正确")
        print("   2. 用户名是否正确")
        print("   3. 项目路径是否正确")
        print("   4. 网络连接是否正常")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
