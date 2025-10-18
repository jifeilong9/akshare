#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
验证 Cursor Rules 文件格式
确保所有 .mdc 文件包含正确的 frontmatter
"""

import os
import re
from pathlib import Path


def validate_mdc_file(file_path: Path) -> dict:
    """验证单个 .mdc 文件"""
    result = {
        "file": file_path.name,
        "valid": True,
        "errors": [],
        "warnings": [],
        "metadata": {},
    }
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查 frontmatter
        frontmatter_pattern = r"^---\n(.*?)\n---"
        match = re.match(frontmatter_pattern, content, re.DOTALL)
        
        if not match:
            result["valid"] = False
            result["errors"].append("缺少 frontmatter (--- ... ---)")
            return result
        
        frontmatter = match.group(1)
        result["metadata"]["raw"] = frontmatter
        
        # 解析 frontmatter
        for line in frontmatter.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                result["metadata"][key.strip()] = value.strip()
        
        # 检查必需的元数据
        has_always_apply = "alwaysApply" in result["metadata"]
        has_description = "description" in result["metadata"]
        has_globs = "globs" in result["metadata"]
        
        if not (has_always_apply or has_description or has_globs):
            result["warnings"].append(
                "建议至少包含 alwaysApply, description 或 globs 之一"
            )
        
        # 检查内容结构
        content_after_frontmatter = content[match.end():].strip()
        
        if not content_after_frontmatter:
            result["errors"].append("frontmatter 后没有内容")
            result["valid"] = False
        
        if not content_after_frontmatter.startswith("#"):
            result["warnings"].append("内容应该以 Markdown 标题开始")
        
        # 统计信息
        result["stats"] = {
            "lines": len(content.split("\n")),
            "chars": len(content),
            "size_kb": round(len(content.encode("utf-8")) / 1024, 2),
        }
        
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"读取文件错误: {str(e)}")
    
    return result


def main():
    """验证所有规则文件"""
    import sys
    import io
    
    # 设置输出编码为 UTF-8
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    rules_dir = Path(__file__).parent
    mdc_files = list(rules_dir.glob("*.mdc"))
    
    print("=" * 60)
    print("Cursor Rules 验证工具")
    print("=" * 60)
    print(f"\n找到 {len(mdc_files)} 个 .mdc 文件\n")
    
    all_valid = True
    total_size = 0
    
    for mdc_file in sorted(mdc_files):
        result = validate_mdc_file(mdc_file)
        
        print(f"[FILE] {result['file']}")
        print(f"   大小: {result['stats']['size_kb']} KB")
        print(f"   行数: {result['stats']['lines']}")
        
        # 显示元数据
        if "alwaysApply" in result["metadata"]:
            print(f"   [AUTO] 自动应用: {result['metadata']['alwaysApply']}")
        if "description" in result["metadata"]:
            print(f"   [DESC] 描述: {result['metadata']['description']}")
        if "globs" in result["metadata"]:
            print(f"   [GLOB] 匹配: {result['metadata']['globs']}")
        
        # 显示错误
        if result["errors"]:
            all_valid = False
            print(f"   [ERROR] 错误:")
            for error in result["errors"]:
                print(f"      - {error}")
        
        # 显示警告
        if result["warnings"]:
            print(f"   [WARN] 警告:")
            for warning in result["warnings"]:
                print(f"      - {warning}")
        
        if result["valid"] and not result["warnings"]:
            print("   [OK] 验证通过")
        
        total_size += result["stats"]["size_kb"]
        print()
    
    # 总结
    print("=" * 60)
    print("验证总结")
    print("=" * 60)
    print(f"总文件数: {len(mdc_files)}")
    print(f"总大小: {round(total_size, 2)} KB")
    print(f"状态: {'[PASS] 全部通过' if all_valid else '[FAIL] 存在错误'}")
    print()
    
    # 检查 README
    readme_path = rules_dir / "README.md"
    quick_ref_path = rules_dir / "QUICK_REFERENCE.md"
    
    if readme_path.exists():
        print("[OK] 找到 README.md")
    else:
        print("[WARN] 缺少 README.md")
    
    if quick_ref_path.exists():
        print("[OK] 找到 QUICK_REFERENCE.md")
    else:
        print("[WARN] 缺少 QUICK_REFERENCE.md")
    
    return 0 if all_valid else 1


if __name__ == "__main__":
    exit(main())

