# 📋 在 GitHub 上直接创建 build.yml 文件

## 超简单 3 步骤

---

## 第1步：打开仓库的创建文件页面

复制这个链接到浏览器打开：
```
https://github.com/你的GitHub用户名/ConstructionFineApp/new/.github/workflows
```

把 `你的GitHub用户名` 替换成你注册GitHub时的用户名。

如果链接打不开，按照下面操作：

1. 打开你的仓库页面：`https://github.com/你的GitHub用户名/ConstructionFineApp`
2. 在仓库名称右边，点击 **"Add file"**（添加文件）按钮
3. 选择 **"Create new file"**（创建新文件）

---

## 第2步：设置文件名和路径

在创建新文件页面：

### 1. 输入文件名

在顶部的输入框中，输入：
```
.github/workflows/build.yml
```

### 2. 检查路径

输入框上方应该显示：
```
ConstructionFineApp / .github / workflows / build.yml
```

如果显示正确，继续下一步！

---

## 第3步：粘贴代码

复制下面的完整代码，粘贴到大的代码输入框中：

```yaml
name: Build Android APK

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer cython
        pip install -r requirements.txt

    - name: Show buildozer version
      run: buildozer --version

    - name: Build with buildozer
      run: |
        buildozer android debug

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: fineapp-apk
        path: bin/*.apk
        retention-days: 90

    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/')
      uses: softprops/action-gh-release@v1
      with:
        files: bin/*.apk
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 第4步：提交文件

### 1. 填写提交信息

在页面底部的 **"Commit changes"** 区域：

- **"Commit message"** 输入框，输入：
  ```
  Add GitHub Actions workflow
  ```

- **"Extended description"**（可选，可以不填）

### 2. 提交文件

点击绿色的 **"Commit changes"**（提交更改）按钮

---

## 第5步：等待自动编译（3-5分钟）

### 1. 打开 Actions 页面

在仓库页面，点击顶部的 **"Actions"** 标签

### 2. 查看编译进度

你会看到一个名为 **"Build Android APK"** 的 workflow：
- ⚙️ 状态图标是黄色 = 正在编译
- ✅ 状态图标是绿色 = 编译成功
- ❌ 状态图标是红色 = 编译失败

### 3. 等待完成

通常需要 3-5 分钟，请耐心等待！

---

## 第6步：下载 APK

### 1. 进入编译完成的 workflow

点击状态为绿色的 **"Build Android APK"** workflow

### 2. 滚动到页面底部

找到 **"Artifacts"**（工件）部分

### 3. 展开 artifact

点击 **"fineapp-apk"** 展开它

### 4. 下载 APK

点击 APK 文件名，开始下载

---

## 第7步：安装到手机

1. 将下载的 APK 文件传输到手机
2. 在手机上点击 APK 文件
3. 允许安装未知来源的应用
4. 安装完成，打开使用！

---

## ⚠️ 常见问题

### Q1：找不到 "Add file" 按钮？

**A：**
- 确保你登录了 GitHub
- 确保你打开的是你自己的仓库（不是别人的）
- 仓库名称是 `ConstructionFineApp`

### Q2：路径显示不对？

**A：**
- 文件名必须是：`.github/workflows/build.yml`
- 如果显示其他路径，点击文件名输入框，重新输入
- 或者先创建 `.github` 文件夹，然后创建 `workflows` 子文件夹，最后创建 `build.yml`

### Q3：编译失败？

**A：**
1. 在 Actions 页面，点击失败的 workflow
2. 查看错误信息
3. 把错误告诉我，我帮你解决

### Q4：Actions 页面是空的？

**A：**
- 说明 workflow 文件没有创建成功
- 重新按照上面的步骤创建
- 确保文件路径正确：`.github/workflows/build.yml`

---

## 📊 文件路径检查

在文件输入框中，应该显示这个完整路径：

```
ConstructionFineApp/.github/workflows/build.yml
```

如果不一致，请重新输入文件名！

---

## 🎯 完成后

创建完成后：
1. ✅ GitHub 会自动开始编译
2. ✅ 3-5 分钟后编译完成
3. ✅ 下载 APK 安装到手机

有问题随时告诉我！🔮
