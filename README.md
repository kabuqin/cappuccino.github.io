# ☕ 卡布奇诺的技术笔记

> 关于 OSCP、内网渗透与生活的碎片

个人技术博客，记录渗透测试学习、漏洞复现与安全研究笔记。

## 🌐 访问地址

[https://kabuqin.github.io/cappuccino.github.io](https://kabuqin.github.io/cappuccino.github.io)

## 🛠 技术栈

- 框架：[Hugo](https://gohugo.io/)
- 主题：[Terminal](https://github.com/panr/hugo-theme-terminal)
- 部署：GitHub Pages + GitHub Actions

## 📂 目录结构

```
content/posts/   # 博客文章（Markdown）
static/          # 静态资源（图片等）
hugo.toml        # Hugo 配置文件
.github/         # GitHub Actions 自动部署
```

## ✍️ 新增文章

1. 在 `content/posts/` 下创建 `.md` 文件
2. 添加 Hugo Front Matter：
   ```yaml
   ---
   title: "文章标题"
   draft: false
   tags: ["标签"]
   ---
   ```
3. 推送到 `main` 分支，GitHub Actions 自动构建部署
