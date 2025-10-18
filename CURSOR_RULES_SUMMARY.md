# AKShare Cursor Rules 生成总结

## 📁 生成的文件

已成功为 AKShare 项目生成完整的 Cursor Rules 配置:

```
.cursor/
├── README.md                          # Cursor 配置总览
└── rules/
    ├── README.md                      # 规则文档索引 (4.9 KB)
    ├── QUICK_REFERENCE.md             # 快速参考卡片 (5.9 KB)
    ├── 00-project-overview.mdc        # 项目概述 (1.8 KB) ✅ 自动应用
    ├── 01-python-style.mdc            # Python 代码风格 (2.8 KB) 📝 *.py
    ├── 02-api-development.mdc         # 接口开发指南 (4.3 KB)
    ├── 03-documentation.mdc           # 文档编写规范 (3.1 KB) 📝 *.md, *.rst
    ├── 04-contribution.mdc            # 贡献指南 (3.8 KB)
    ├── 05-common-patterns.mdc         # 常用代码模式 (6.7 KB)
    ├── 06-dependencies.mdc            # 依赖管理 (5.3 KB)
    └── 07-testing-debugging.mdc       # 测试调试指南 (9.9 KB)

总计: 10 个文件, 约 48 KB
```

## 📋 规则清单

### 1️⃣ 自动应用规则

**00-project-overview.mdc** ✅
- 在所有 AI 对话中自动加载
- 包含项目简介、结构、核心理念
- 提供项目基础上下文信息

### 2️⃣ 文件类型规则

**01-python-style.mdc** (*.py)
- Python 代码风格规范
- 文档字符串格式
- 命名规范和类型注解
- Ruff 格式化标准

**03-documentation.mdc** (*.md, *.rst)
- Markdown 和 RST 格式规范
- 接口文档模板
- 中文书写规范
- 更新日志格式

### 3️⃣ 按需引用规则

**02-api-development.mdc**
- 数据接口开发完整流程
- 函数命名和实现模板
- 分页数据处理
- 数据质量要求
- 触发: "如何开发新接口"

**04-contribution.mdc**
- Git 工作流程
- 代码提交规范
- Pull Request 流程
- 贡献类型指南
- 触发: "如何贡献代码"

**05-common-patterns.mdc**
- HTTP 请求模式 (同步/异步)
- DataFrame 操作
- 数据清洗和转换
- JavaScript 执行
- HTML 解析
- 触发: "如何发送请求"、"数据处理方法"

**06-dependencies.mdc**
- 核心依赖列表和说明
- 常用库使用指南
- 依赖版本管理
- 平台特定配置
- 触发: "如何使用 pandas"、"添加依赖"

**07-testing-debugging.mdc**
- 接口测试方法
- 数据验证技巧
- 调试工具和技巧
- 常见问题排查
- 性能测试方法
- 触发: "如何测试"、"调试方法"

## 🎯 核心特性

### ✨ 全面覆盖

- **项目概述**: 理解 AKShare 的定位和架构
- **代码规范**: Python 和文档的格式标准
- **开发指南**: 从零开发新数据接口的完整流程
- **最佳实践**: 常用代码模式和设计模式
- **依赖管理**: 核心库的使用方法
- **测试调试**: 问题排查和质量保证
- **协作流程**: Git 工作流和 PR 规范

### 🔧 实用工具

- **快速参考卡片**: 常用命令、代码片段、速查表
- **代码模板**: 可直接使用的函数模板
- **规则索引**: 快速找到需要的规则
- **文件引用**: 规则之间相互引用,形成知识网络

### 📚 文档完善

- 每个规则都包含详细说明和示例
- 使用表格、列表、代码块等多种格式
- 中文编写,符合项目风格
- 包含触发方式和使用场景

## 🚀 使用方法

### 对于开发者

1. **查看快速参考**: `.cursor/rules/QUICK_REFERENCE.md`
2. **了解所有规则**: `.cursor/rules/README.md`
3. **开发时**: Cursor AI 会自动应用相关规则
4. **遇到问题**: 询问相关问题触发对应规则

### 对于 AI 助手

规则会根据以下情况自动加载:

- ✅ **始终加载**: 00-project-overview.mdc
- 📝 **编辑 Python 文件**: 01-python-style.mdc
- 📝 **编辑文档文件**: 03-documentation.mdc
- 🔍 **关键词触发**: 其他规则根据用户问题引用

### 示例对话

```
用户: "我要开发一个获取股票数据的接口"
AI: [引用 02-api-development.mdc 和 05-common-patterns.mdc]
    根据 AKShare 的接口开发规范...

用户: "如何处理分页数据?"
AI: [引用 05-common-patterns.mdc]
    使用以下模式处理分页数据...

用户: "遇到中文乱码怎么办?"
AI: [引用 07-testing-debugging.mdc]
    检查并设置正确的编码...
```

## 📊 规则统计

- **总文件数**: 10 个
- **规则数**: 8 个 (.mdc 文件)
- **辅助文档**: 2 个 (README, QUICK_REFERENCE)
- **总大小**: 约 48 KB
- **代码示例**: 50+ 个
- **覆盖主题**: 7 大类

## ✅ 规则质量

### 内容质量

- ✅ 基于项目实际代码分析
- ✅ 参考官方文档和 CONTRIBUTING.md
- ✅ 包含实际可运行的代码示例
- ✅ 涵盖常见问题和解决方案
- ✅ 符合项目 Ruff 规范

### 结构质量

- ✅ 使用正确的 frontmatter 元数据
- ✅ Markdown 格式规范
- ✅ 合理的文件组织和命名
- ✅ 清晰的引用关系
- ✅ 完善的索引和导航

### 实用性

- ✅ 提供即用型代码模板
- ✅ 包含快速参考卡片
- ✅ 分层设计 (概述→详细)
- ✅ 问题导向的组织方式
- ✅ 中文编写,易于理解

## 🎓 学习路径

推荐的规则阅读顺序:

1. **入门** → QUICK_REFERENCE.md
2. **了解项目** → 00-project-overview.mdc
3. **学习规范** → 01-python-style.mdc
4. **开发接口** → 02-api-development.mdc
5. **参考模式** → 05-common-patterns.mdc
6. **测试调试** → 07-testing-debugging.mdc
7. **贡献代码** → 04-contribution.mdc

## 🔄 维护建议

### 定期更新

- 当项目规范变化时更新规则
- 添加新的常见问题和解决方案
- 补充更多代码示例

### 扩展方向

可以考虑添加:
- 特定模块的详细规则 (如 stock/, fund/)
- 性能优化专题规则
- 数据源对接规范
- API 设计最佳实践

### 版本控制

- 规则文件纳入 Git 版本控制
- 在 CHANGELOG 中记录规则变更
- 保持与项目版本同步

## 📖 相关资源

- **项目文档**: https://akshare.akfamily.xyz/
- **GitHub**: https://github.com/akfamily/akshare
- **Cursor 文档**: https://cursor.com/docs
- **Ruff**: https://github.com/astral-sh/ruff

## 🎉 总结

为 AKShare 项目成功生成了一套完整、实用的 Cursor Rules:

- ✅ 8 个核心规则文件,覆盖开发全流程
- ✅ 2 个辅助文档,便于快速查阅
- ✅ 50+ 个代码示例,可直接使用
- ✅ 自动应用 + 手动触发,灵活高效
- ✅ 中文编写,符合项目风格
- ✅ 基于实际代码,贴近开发实践

这些规则将帮助 Cursor AI 更好地理解 AKShare 项目,为开发者提供更准确、更有针对性的代码建议和辅助。

---

**生成日期**: 2025-10-17  
**生成工具**: Cursor AI (Claude Sonnet 4.5)  
**项目**: AKShare - 开源财经数据接口库

