---
title: "使用 Hugo + GitHub Pages 免费搭建技术博客"
date: 2026-06-27
draft: false
tags: ["Hugo", "GitHub Pages", "博客搭建", "自动化部署"]
---

```markdown

## 一、项目概述：为什么选择 Hugo + GitHub Pages？

对于技术博主来说，最理想的写作体验是“**用 Markdown 写作，Git 管理版本，一次推送自动上线**”。而 **Hugo + GitHub Pages + GitHub Actions** 的组合，恰好能完美实现这个流程。

这套方案的核心优势非常突出：

| 优势 | 说明 |
|------|------|
| **完全免费** | GitHub Pages 提供免费托管 + 全球 CDN 加速，无需购买服务器 |
| **极致性能** | Hugo 是Go语言写的静态生成器，构建速度毫秒级，生成纯HTML页面，访问极快 |
| **高安全性** | 没有数据库、没有服务端脚本，从根本上杜绝了SQL注入等常见漏洞 |
| **版本控制** | 所有文章和配置都用 Git 管理，历史变更清晰可查 |
| **写作纯粹** | 用 Markdown 写作，专注于内容本身 |

下面以开源项目 **[cappuccino.github.io](https://github.com/kabuqin/cappuccino.github.io)** 为参考，一步步带你搭建属于自己的技术博客。

---

## 二、技术选型

参考这个项目的技术栈：

- **框架**：[Hugo](https://gohugo.io/) —— 全球最快的静态网站生成器
- **主题**：[Gokarna](https://github.com/gokarna-theme/gokarna-hugo) —— 极简风格，专注于内容呈现
- **托管**：GitHub Pages —— 永久免费，自带SSL证书和CDN加速
- **自动化部署**：GitHub Actions —— 推送代码后自动构建并发布

你也可以选择其他主题，如 PaperMod、Ananke 等，Hugo 官方主题库有 2000+ 主题可供选择。

---

## 三、详细搭建步骤

### 第一步：安装 Hugo

**Mac（使用 Homebrew）**：
```bash
brew install hugo
```

**Windows（使用 Scoop）**：
```bash
scoop install hugo-extended
```

**Linux（直接下载二进制）**：
从 [Hugo Releases](https://github.com/gohugoio/hugo/releases) 下载对应版本，解压后放到 `/usr/local/bin/`。

安装完成后验证：
```bash
hugo version
```

### 第二步：创建 Hugo 站点

```bash
# 创建新站点（将 myblog 替换为你的博客名称）
hugo new site myblog
cd myblog

# 初始化 Git 仓库
git init
```

### 第三步：安装主题

以 Gokarna 主题为例：

```bash
# 将主题添加为 Git 子模块（方便后续更新）
git submodule add https://github.com/gokarna-theme/gokarna-hugo themes/gokarna
```

在 `hugo.toml`（或 `hugo.yaml`）中配置主题：
```toml
theme = "gokarna"
baseURL = "https://你的用户名.github.io/"
title = "你的博客名称"
languageCode = "zh-CN"
```

### 第四步：撰写第一篇文章

在 `content/posts/` 目录下创建 Markdown 文件：

```bash
hugo new posts/第一篇文章.md
```

打开文件，在顶部添加 Front Matter 元数据：
```yaml
---
title: "第一篇文章"
date: 2026-06-27
draft: false
tags: ["Hugo", "博客"]
---
这里是文章正文，使用 Markdown 语法写作...
```

> **注意**：`draft: true` 的文章在构建时不会被发布，写完后记得改为 `false`。

### 第五步：本地预览

```bash
hugo server -D
```

打开浏览器访问 `http://localhost:1313`，即可实时预览效果。修改内容后页面会自动刷新。

---

## 四、部署到 GitHub Pages

### 4.1 创建 GitHub 仓库

1. 登录 GitHub，点击右上角 **+** → **New repository**
2. 仓库名设置为 **`你的用户名.github.io`**（例如 `kabuqin.github.io`）
3. 选择 **Public**，不要勾选初始化 README

### 4.2 关联本地仓库并推送

```bash
git remote add origin https://github.com/你的用户名/你的用户名.github.io.git
git add .
git commit -m "初始化博客"
git push -u origin main
```

---

## 五、配置 GitHub Actions 自动部署

这是整个流程中最关键的一步——实现 **“推送即部署”** 。

### 5.1 创建 GitHub Actions 工作流

在项目根目录创建 `.github/workflows/deploy.yml`：

```yaml
name: Build and Deploy

on:
  push:
    branches:
      - main  # 当推送到 main 分支时触发
  workflow_dispatch:  # 支持手动触发

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive  # 拉取主题子模块
          fetch-depth: 0

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: '0.119.0'
          extended: true

      - name: Build
        run: hugo --minify  # 生成静态文件到 public/ 目录

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

这个工作流会自动完成：
1. 拉取代码（包括主题子模块）
2. 安装 Hugo
3. 执行 `hugo --minify` 构建静态文件
4. 将生成的 `public/` 目录部署到 GitHub Pages

### 5.2 启用 GitHub Pages

1. 进入仓库 → **Settings** → **Pages**
2. 在 **Source** 处选择 **GitHub Actions**
3. 配置完成，无需保存按钮，更改即时生效

### 5.3 推送触发部署

```bash
git add .
git commit -m "添加自动部署配置"
git push
```

推送后，前往仓库的 **Actions** 选项卡查看部署进度。绿色对勾表示部署成功。

访问 `https://你的用户名.github.io/` 即可看到你的博客。

---

## 六、日常写作流程

博客搭建完成后，日常写作只需三步：

1. **新建文章**：`hugo new posts/文章标题.md`
2. **写作**：用 Markdown 编写内容，修改 Front Matter 中的 `draft: false`
3. **发布**：`git add . && git commit -m "新增文章" && git push`

推送后 GitHub Actions 自动构建部署，几分钟后线上更新。

---

## 七、目录结构说明

参考项目的目录结构：

```
myblog/
├── content/
│   └── posts/          # 所有博客文章（Markdown）
├── static/             # 静态资源（图片、CSS等）
├── themes/             # 主题（通过 Git submodule 管理）
├── hugo.toml           # Hugo 配置文件
├── .github/
│   └── workflows/
│       └── deploy.yml  # GitHub Actions 自动部署配置
└── public/             # 构建生成的静态文件（自动生成，不提交）
```

---

## 八、进阶优化建议

1. **自定义域名**：在 `static/` 目录下创建 `CNAME` 文件，写入你的域名
2. **图片优化**：使用 ImageOptim 等工具压缩图片，添加懒加载
3. **SEO 优化**：在 `hugo.toml` 中配置 `enableRobotsTXT = true`
4. **统计分析**：接入 Google Analytics 或 Umami 等免费工具

---

## 总结

通过 **Hugo + GitHub Pages + GitHub Actions** 这套方案，你可以零成本搭建一个高性能、高安全性的技术博客。整个流程的核心是 **“内容即代码”**——用 Markdown 写作，用 Git 管理，推送即自动部署。

就像 [cappuccino.github.io](https://github.com/kabuqin/cappuccino.github.io) 这个项目一样，你只需要专注于写出优质的技术文章，剩下的构建和部署工作，全部交给自动化流程去完成。
