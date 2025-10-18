# Cursor AI 配置

本目录包含 Cursor AI 编辑器的配置和规则文件。

## 目录结构

```
.cursor/
├── README.md          # 本文件
└── rules/             # Cursor Rules 规则目录
    ├── README.md                   # 规则说明文档
    ├── QUICK_REFERENCE.md          # 快速参考卡片
    ├── 00-project-overview.mdc     # 项目概述 (自动应用)
    ├── 01-python-style.mdc         # Python代码风格 (*.py)
    ├── 02-api-development.mdc      # 接口开发指南
    ├── 03-documentation.mdc        # 文档编写规范 (*.md, *.rst)
    ├── 04-contribution.mdc         # 贡献指南
    ├── 05-common-patterns.mdc      # 常用代码模式
    ├── 06-dependencies.mdc         # 依赖管理
    └── 07-testing-debugging.mdc    # 测试调试指南
```

## Cursor Rules

Cursor Rules 是帮助 AI 理解项目上下文和编码规范的配置文件。

### 规则类型

1. **自动应用** (alwaysApply: true)
   - 在所有对话中自动加载
   - 例如: 项目概述

2. **文件匹配** (globs: "*.py")
   - 编辑匹配类型的文件时自动应用
   - 例如: Python 文件的代码风格规范

3. **手动触发** (description: "...")
   - 通过询问相关问题触发
   - 例如: "如何开发新接口?"

### 快速开始

1. **开发者**:
   - 查看 [rules/QUICK_REFERENCE.md](rules/QUICK_REFERENCE.md) 获取常用命令和代码片段
   - 查看 [rules/README.md](rules/README.md) 了解所有规则

2. **使用 Cursor AI**:
   - 规则会自动加载,无需手动操作
   - 询问相关问题时会引用对应规则
   - 例如: "我要开发一个新的数据接口"

### 规则维护

- 规则文件使用 `.mdc` 扩展名 (Markdown with Cursor extensions)
- 包含 YAML frontmatter 元数据
- 使用 Markdown 格式编写内容

示例结构:

```markdown
---
alwaysApply: true
description: "规则描述"
globs: "*.py"
---

# 规则标题

规则内容...
```

## 文件引用

在规则中引用项目文件使用以下格式:

```markdown
[文件名](mdc:相对路径)
```

例如:
- `[setup.py](mdc:setup.py)`
- `[项目文档](mdc:README.md)`

## 更多信息

- 📖 Cursor 文档: https://cursor.com/docs
- 🔧 AKShare 项目: https://github.com/akfamily/akshare
- 📚 规则详细说明: [rules/README.md](rules/README.md)

---

**创建日期**: 2025-10-17  
**用途**: 为 AKShare 项目提供 AI 辅助开发的上下文和规范

