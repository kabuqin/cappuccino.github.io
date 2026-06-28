---
title: "Shopify Help Center AI 助手 Markdown 渲染缺陷导致 CSRF 与 RXSS 组合攻击"
draft: false
type: post
tags: ["CVE", "XSS", "SHOPIFY"]
date: 2026-06-23
---

## Shopify Help Center AI 助手 Markdown 渲染缺陷导致 CSRF 与 RXSS 组合攻击

该报告（#2509022）披露了 Shopify 帮助中心（`help.shopify.com`）的 AI 聊天助手在处理 Markdown 图片渲染时存在缺陷，攻击者可利用跨站请求伪造（CSRF）在受害者会话中植入恶意 Markdown 图片链接，最终触发反射型 XSS（RXSS），进而泄露用户个人信息并劫持支持对话。

---

### 漏洞概述

Shopify 帮助中心的 AI 聊天机器人在向用户展示问候语时，支持 Markdown 语法以丰富对话体验。在问候语的生成过程中，部分用户可控的输入会被直接反射到页面中。攻击者通过一个 CSRF 请求，可在受害者的会话中设置包含恶意 Markdown 图片的问候语。当受害者后续访问搜索页面时，该问候语被渲染，其中的 Markdown 图片链接因 `target="_blank"` 属性，需要用户使用鼠标中键点击才能触发 XSS（但攻击者可通过社会工程诱导用户执行该操作）。一旦触发，恶意脚本将窃取受害者个人信息，并尝试将攻击者邮箱添加为受害者已有支持对话的订阅者，从而获取对话内容或参与其中。

---

### 根本原因

1. **CSRF 漏洞**：`https://help.shopify.com/en/search` 端点接受 `POST` 请求，其中 `greeting` 参数可被攻击者任意设置，且该请求缺乏有效的 CSRF 防护（如 anti-CSRF token 或同源校验），使得攻击者可以跨站诱导已登录用户发起该请求，将恶意问候语存入受害者会话。

2. **Markdown 渲染缺陷**：问候语中的 Markdown 图片语法（`![alt](url)`）会被解析并渲染为 HTML 链接（`<a>` 标签），且该链接带有 `target="_blank"` 属性，用户点击时会在新标签页打开。攻击者将 `javascript:` 伪协议作为图片 URL，构造出可执行代码的链接。虽然浏览器对 `javascript:` 协议在新窗口中的执行有所限制（需要用户主动点击），但攻击者通过 `mouse wheel click`（鼠标中键点击）即可绕过部分限制，触发 XSS。

3. **XSS 载荷的编码与混淆**：攻击者将完整的 JavaScript 载荷进行 Base64 编码，并放置在 `javascript:eval(atob('...'))` 中，以规避简单过滤。

---

### 攻击链路（完整复现）

**步骤 1：攻击者构造 CSRF 页面**  
攻击者制作一个恶意 HTML 页面，包含一个隐藏表单，向 `https://help.shopify.com/en/search?_data=routes%2F%28%24locale%29.search` 发起 POST 请求，参数如下：
- `query`：任意搜索词（如 `Is this XSS?`）
- `greeting`：值为 Markdown 图片语法，其中图片 URL 为 `javascript:eval(atob('<Base64 编码的载荷>'))`

该页面同时包含第二个表单，用于在 2 秒后自动发起 GET 请求，以便受害者访问搜索页面时触发渲染。

**步骤 2：诱导受害者访问 CSRF 页面**  
攻击者将恶意页面链接发送给已登录 Shopify 帮助中心的受害者。当受害者访问该页面时，表单自动提交（利用浏览器跨域 POST 的默认行为），在受害者会话中设置了带有恶意问候语的搜索状态。

**步骤 3：受害者跳转至搜索页面**  
CSRF 页面在提交后，会通过第二个表单或 JavaScript 自动重定向受害者到 `https://help.shopify.com/en/search?q=Is%20this%20XSS%3F`。此时，帮助中心的 AI 聊天问候语被渲染为 Markdown 图片链接，内容类似：`![Mouse wheel click here for more info...](javascript:eval(atob('...')))`。由于该链接带有 `target="_blank"`，受害者需要“鼠标中键点击”该链接才能在新标签页中触发 XSS。

**步骤 4：触发 XSS 并执行恶意载荷**  
一旦受害者中键点击该链接，`javascript:` 协议被执行，Base64 解码后的载荷开始运行。载荷的功能包括：
- 向攻击者控制的服务器发送请求，泄露当前用户的个人信息（如邮箱、姓名等），这些信息可通过 `window.__remixContext.state.loaderData.root.userInfo` 获取。
- 调用 GraphQL API 查询受害者最近的支持对话（`conversations(last: 1)`），获取对话 ID。
- 使用该对话 ID，通过 GraphQL 变更（mutation）`subscriberCreate`，将攻击者控制的邮箱（`saltymermaid@wearehackerone.com`）添加为该对话的订阅者，从而允许攻击者接收对话通知并参与其中。

**步骤 5：攻击者接管对话**  
攻击者成功订阅后，可接收该对话的所有后续消息，甚至可能通过 Shopify 的客服系统回复，进一步获取敏感信息或进行社会工程。

---

### 影响与危害

- **危害等级**：**高**（可导致用户 PII 泄露及支持对话被第三方监控，涉及隐私侵犯和账户关联风险）
- **攻击门槛**：中低（需要受害者点击链接并执行一次中键点击，但攻击者可通过诱导性文案提高成功率）
- **泄露数据**：
  - 用户个人信息（根据 `userInfo` 内容，可能包括邮箱、姓名、用户 ID 等）
  - 用户与 Shopify 客服的历史对话记录（通过订阅获取）
- **后续利用**：攻击者可阅读受害者的客服对话，甚至冒充受害者与客服沟通，进而可能执行账户恢复、密码重置等进一步操作，扩大影响范围。

---

### 修复建议

1. **CSRF 防护**：在 `/en/search` 端点的 `POST` 请求中引入 anti-CSRF token，或使用 SameSite 属性限制跨站请求。

2. **输入过滤与输出编码**：对用户可控的 `greeting` 参数进行严格过滤，禁止或转义 `javascript:`、`data:` 等危险协议，并在渲染 Markdown 图片链接时，对 URL 进行协议白名单检查（仅允许 `http`/`https`）。

3. **用户交互强化**：对于带有 `target="_blank"` 的链接，可在 `rel` 属性中添加 `noopener noreferrer`，并考虑禁用 `javascript:` 协议在 `href` 中的执行，或使用 Content Security Policy（CSP）限制脚本来源。

4. **敏感数据保护**：确保 `window.__remixContext` 等客户端全局对象不包含过多敏感信息，或对其进行脱敏处理。

---

### 小结

该漏洞展示了如何将两个中低风险问题（CSRF 和 Markdown 注入）串联，形成高风险的账户数据泄露链。Shopify 帮助中心的 AI 聊天功能在设计上未充分考虑用户输入的可信度，且缺乏对跨站请求的有效防护。在修复时，除了修补正则表达式和添加 token，还应全面审查所有用户可控内容在 Markdown 渲染中的处理方式，确保不会引入可执行代码。

---

**原文链接**：https://hackerone.com/reports/2509022
