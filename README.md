# auto_slides

自用 Reveal.js 演示模板，基于 Markdown 编写幻灯片内容。

```bash
npx serve docs
```

打开浏览器访问 `http://localhost:3000` 即可预览。

## 使用方式

所有幻灯片内容在 `docs/index.html` 中，使用 `<section data-markdown>` + `<textarea data-template>` 编写 Markdown。

- **属性**：转场动画、背景色、`data-state` 写在 `<section>` 上
- **内容**：用纯 Markdown 写列表、代码块、表格、引用
- **双栏 / 卡片**：用内嵌原始 HTML 实现复杂布局
- **演讲者备注**：`notes:` 写在每页末尾
- **代码高亮**：\`\`\` 代码块自动着色，`data-line-numbers` 支持逐步高亮

## 文件结构

| 文件 | 用途 |
|------|------|
| `docs/index.html` | 幻灯片骨架（Markdown 内容） |
| `docs/app.js` | ESM 加载 Reveal.js + 5 个插件 |
| `docs/styles.css` | 深色玻璃主题，背景图可见 |
| `docs/background.jpg` | 氛围背景图 |
