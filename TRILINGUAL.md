# 三语网站

简体保留原路径；繁体位于 `/zh-hant/`；英语位于 `/en/`。语言切换保留当前页面。

简体是维护原稿，繁体使用 OpenCC 生成。英语主要页面和媒体观点完整翻译；历史文章只提供英文标题、摘要和中文原文链接。三种语言共用 CSS、图片及交互脚本，不调用在线翻译服务。尚未审核的隆安文章没有纳入任何语言页面。

## 更新方式

1. 修改简体源文件。
2. 在 `script/i18n/en.json` 更新对应英文；历史文章标题与摘要在 `articles-en.json`。
3. 正常构建 Jekyll 到临时目录，再运行 `python script/localize.py --build 临时目录 --source 网站源码目录`。依赖见 `script/i18n/requirements.txt`。
4. 再次构建，检查三语链接后发布源码。生成的 `en/` 和 `zh-hant/` 必须提交到仓库，GitHub Pages 不需要安装 Python 依赖。

所有语言包含 canonical 与 hreflang。搜索引擎可单独索引各语言。英文摘要保留原发表语境，未重新核验历史法律文章。
