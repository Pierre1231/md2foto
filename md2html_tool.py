#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Author: HUANG Jingyi
File: md2html_tool.py
Date:  2025-02-20 15:15:37
Email: pierrehuang1998@gmail.com
Description: 
"""

import os

try:
    from markdown import markdown
except ModuleNotFoundError as e:
    os.system("pip install markdown")
    os.system("pip install python-markdown-math")
    os.system("pip install markdown_checklist")
    from markdown import markdown

try:
    from pymdownx import superfences
except ModuleNotFoundError as e:
    os.system("pip install pymdown-extensions")
    from pymdownx import superfences


class mdtox:
    def __init__(self, md_text, encoding='utf-8'):
        self.md_text = md_text
        self.encoding = encoding
        self.__args()

    def __args(self):
        self.html = '''
        <!DOCTYPE html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, minimal-ui">
                <title>{}</title>
            </head>
            <body>
                <article class="markdown-body" id="markdown-body">
                    {}
                </article>
            </body>
        </html>
        '''

        # 扩展配置
        self.extensions = [
            'toc',  # 目录，[toc]
            'extra',  # 缩写词、属性列表、释义列表、围栏式代码块、脚注、在HTML的Markdown、表格
        ]
        third_party_extensions = [
            'mdx_math',  # KaTeX数学公式，$E=mc^2$和$$E=mc^2$$
            'markdown_checklist.extension',  # checklist，- [ ]和- [x]
            'pymdownx.magiclink',  # 自动转超链接，
            'pymdownx.caret',  # 上标下标，
            'pymdownx.superfences',  # 多种块功能允许嵌套，各种图表
            'pymdownx.betterem',  # 改善强调的处理(粗体和斜体)
            'pymdownx.mark',  # 亮色突出文本
            'pymdownx.highlight',  # 高亮显示代码
            'pymdownx.tasklist',  # 任务列表
            'pymdownx.tilde',  # 删除线
        ]
        self.extensions.extend(third_party_extensions)
        self.extension_configs = {
            'mdx_math': {
                'enable_dollar_delimiter': True  # 允许单个$
            },
            'pymdownx.superfences': {
                "custom_fences": [
                    {
                        'name': 'mermaid',  # 开启流程图等图
                        'class': 'mermaid',
                        'format': superfences.fence_div_format
                    }
                ]
            },
            'pymdownx.highlight': {
                'linenums': True,  # 显示行号
                'linenums_style': 'pymdownx-inline'  # 代码和行号分开
            },
            'pymdownx.tasklist': {
                'clickable_checkbox': True,  # 任务列表可点击
            }
        }

    def to_html(self, html_name):

        title = 'rendered'
        html_text = markdown(self.md_text, output_format='html', extensions=self.extensions,
                             extension_configs=self.extension_configs)  # MarkDown转HTML
        self.html = self.html.format(title, html_text)

        try:
            with open(html_name, 'w', encoding=self.encoding) as file_html:
                file_html.write(self.html)
        except Exception as e:
            print("<Error>", e)
            return False

        return True

