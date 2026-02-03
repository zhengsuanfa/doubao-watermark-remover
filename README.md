# Doubao Watermark Remover

去除豆包 AI 生成图片中的水印"豆包AI生成"。

## 功能特点

- 自动检测并去除豆包水印
- 支持不同尺寸的图片
- 基于 Alpha 贴图的精确去除算法
- 水印位置自适应缩放

## 安装

### 方式 1：作为 Skill 安装

```bash
npx skills add zhengsuanfa/doubao-watermark-remover
```

### 方式 2：手动安装

```bash
git clone https://github.com/zhengsuanfa/doubao-watermark-remover.git
cd doubao-watermark-remover/scripts
pip install -r requirements.txt
```

## 使用方法

### 去除水印

```bash
python remove_watermark.py <输入图片> <输出图片>
```

**示例：**

```bash
python remove_watermark.py input.jpg output.jpg
```

### 捕获 Alpha 贴图（首次使用）

如果水印效果不理想，可以重新生成 Alpha 贴图：

1. 创建一张纯黑色图片（RGB: 0,0,0）
2. 让豆包添加水印
3. 运行捕获工具：

```bash
python capture_alpha_map.py <带水印的黑色图.png> <宽度> <高度>
```

**示例：**

```bash
python capture_alpha_map.py black_with_watermark.png 120 20
```

## 工作原理

豆包水印"豆包AI生成"位于图片**右下角**，使用 Screen 混合模式叠加白色文字。

本工具通过以下步骤去除水印：

1. 根据图片尺寸计算水印区域大小和位置
2. 加载 Alpha 贴图（从纯黑水印图提取）
3. 对水印区域进行背景替换修复

## 水印位置配置

| 图片尺寸 | 水印尺寸 | 右边距 | 下边距 |
|---------|---------|--------|--------|
| > 1024px | 按比例缩放 | 按比例缩放 | 5px |
| ≤ 1024px | 90×18 | 8px | 5px |

## 项目结构

```
doubao-watermark-remover/
├── SKILL.md                      # Skill 定义文件
├── README.md                     # 项目说明
├── assets/
│   └── doubao_alpha.png          # Alpha 贴图
├── references/
│   └── algorithm.md              # 算法详细说明
└── scripts/
    ├── remove_watermark.py       # 去水印脚本
    ├── capture_alpha_map.py      # Alpha 贴图捕获工具
    └── requirements.txt          # Python 依赖
```

## 依赖

- Python 3.9+
- Pillow >= 10.0.0

## 效果对比

| 原图 | 处理后 |
|-----|-------|
| ![原图片](https://github.com/zhengsuanfa/doubao-watermark-remover/raw/main/docs/before.jpg) | ![处理后](https://github.com/zhengsuanfa/doubao-watermark-remover/raw/main/docs/after.jpg) |

## 注意事项

- 仅去除可见的"豆包AI生成"文字水印
- 不影响图片其他部分的内容
- 对于不同尺寸的图片，水印区域会自动缩放

## 许可证

MIT License

## 作者

zhengsuanfa

## 相关链接

- [GitHub 仓库](https://github.com/zhengsuanfa/doubao-watermark-remover)
- [Skills CLI](https://skills.sh/)
