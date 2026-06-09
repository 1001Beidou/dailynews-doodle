#!/usr/bin/env python3
"""
日报生成脚本
将收集的新闻整理成美观的日报格式（HTML 和 Markdown）
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class ReportGenerator:
    def __init__(self, news_file: str = 'data/news.json'):
        self.news_file = news_file
        self.news = self.load_news()
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.date_cn = datetime.now().strftime('%Y年%m月%d日')
    
    def load_news(self) -> List[Dict]:
        """加载收集的新闻"""
        if os.path.exists(self.news_file):
            with open(self.news_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def generate_html(self) -> str:
        """生成 HTML 格式的日报"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日科技新闻 - {self.date_cn}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .summary {{
            background: #f5f7fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }}
        
        .summary h2 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .news-section {{
            margin-bottom: 35px;
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-icon {{
            font-size: 24px;
        }}
        
        .news-item {{
            padding: 15px;
            margin-bottom: 12px;
            background: #f9f9f9;
            border-radius: 8px;
            border-left: 3px solid #667eea;
            transition: all 0.3s ease;
        }}
        
        .news-item:hover {{
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
            transform: translateX(5px);
        }}
        
        .news-item h3 {{
            color: #333;
            margin-bottom: 8px;
            font-size: 16px;
            word-break: break-word;
        }}
        
        .news-item a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .news-item a:hover {{
            text-decoration: underline;
        }}
        
        .news-meta {{
            font-size: 12px;
            color: #999;
            margin-top: 8px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .tagline {{
            font-size: 13px;
            color: #666;
            margin-top: 8px;
            font-style: italic;
        }}
        
        .footer {{
            background: #f5f7fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #e0e0e0;
        }}
        
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        @media (max-width: 600px) {{
            .header h1 {{
                font-size: 24px;
            }}
            
            .content {{
                padding: 15px;
            }}
            
            .news-item {{
                padding: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 每日科技新闻</h1>
            <p>{self.date_cn}</p>
        </div>
        
        <div class="content">
            <div class="summary">
                <h2>📊 今日汇总</h2>
                <p>共收集 <strong>{len(self.news)}</strong> 条科技新闻，来自以下源：</p>
                <p style="margin-top: 10px; color: #666;">
                    🔵 Hacker News &nbsp;•&nbsp; 
                    🟢 Product Hunt &nbsp;•&nbsp; 
                    ⭐ GitHub Trending &nbsp;•&nbsp;
                    🚀 Tech Crunch
                </p>
            </div>
"""
        
        # 按来源分组
        sources = {}
        for news in self.news:
            source = news.get('source', 'Unknown')
            if source not in sources:
                sources[source] = []
            sources[source].append(news)
        
        # 定义图标
        icons = {
            'Hacker News': '🔵',
            'Product Hunt': '🟢',
            'GitHub Trending': '⭐',
            'Tech Crunch': '🚀'
        }
        
        for source, news_list in sources.items():
            icon = icons.get(source, '📌')
            html += f'<div class="news-section">\n'
            html += f'    <div class="section-title">\n'
            html += f'        <span class="section-icon">{icon}</span>\n'
            html += f'        <span>{source}</span>\n'
            html += f'    </div>\n'
            
            for idx, item in enumerate(news_list, 1):
                title = item.get('title', item.get('name', 'Untitled'))
                url = item.get('url', '#')
                
                html += f'    <div class="news-item">\n'
                html += f'        <h3>{idx}. <a href="{url}" target="_blank">{title}</a></h3>\n'
                
                # 添加描述或标语
                if item.get('description'):
                    html += f'        <p class="tagline">{item["description"]}</p>\n'
                elif item.get('tagline'):
                    html += f'        <p class="tagline">{item["tagline"]}</p>\n'
                
                # 添加元数据
                meta = []
                if item.get('score'):
                    meta.append(f'❤️ {item["score"]} likes')
                if item.get('votes'):
                    meta.append(f'👍 {item["votes"]} votes')
                if item.get('stars'):
                    meta.append(f'⭐ {item["stars"]} stars')
                if item.get('comments'):
                    meta.append(f'💬 {item["comments"]} comments')
                if item.get('language'):
                    meta.append(f'🔤 {item["language"]}')
                
                if meta:
                    html += f'        <div class="news-meta">\n'
                    for m in meta:
                        html += f'            <span class="meta-item">{m}</span>\n'
                    html += f'        </div>\n'
                
                html += f'    </div>\n'
            
            html += '</div>\n'
        
        html += """
        <div class="footer">
            <p>✨ 由 Daily Tech News Aggregator 生成</p>
            <p style="margin-top: 10px;">
                <a href="https://github.com/1001Beidou/dailynews-doodle" target="_blank">查看完整报告</a>
            </p>
        </div>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def generate_markdown(self) -> str:
        """生成 Markdown 格式的日报"""
        md = f"""# 📰 每日科技新闻日报

**日期**: {self.date_cn}

---

## 📊 今日汇总

共收集 **{len(self.news)}** 条科技新闻，来自以下源：

- 🔵 Hacker News
- 🟢 Product Hunt  
- ⭐ GitHub Trending
- 🚀 Tech Crunch

---

"""
        
        # 按来源分组
        sources = {}
        for news in self.news:
            source = news.get('source', 'Unknown')
            if source not in sources:
                sources[source] = []
            sources[source].append(news)
        
        # 定义图标
        icons = {
            'Hacker News': '🔵',
            'Product Hunt': '🟢',
            'GitHub Trending': '⭐',
            'Tech Crunch': '🚀'
        }
        
        for source, news_list in sources.items():
            icon = icons.get(source, '📌')
            md += f"## {icon} {source}\n\n"
            
            for idx, item in enumerate(news_list, 1):
                title = item.get('title', item.get('name', 'Untitled'))
                url = item.get('url', '#')
                
                md += f"### {idx}. [{title}]({url})\n\n"
                
                # 添加描述或标语
                if item.get('description'):
                    md += f"> {item['description']}\n\n"
                elif item.get('tagline'):
                    md += f"> {item['tagline']}\n\n"
                
                # 添加元数据
                meta = []
                if item.get('score'):
                    meta.append(f"❤️ {item['score']} likes")
                if item.get('votes'):
                    meta.append(f"👍 {item['votes']} votes")
                if item.get('stars'):
                    meta.append(f"⭐ {item['stars']} stars")
                if item.get('comments'):
                    meta.append(f"💬 {item['comments']} comments")
                if item.get('language'):
                    meta.append(f"🔤 {item['language']}")
                
                if meta:
                    md += f"**{' | '.join(meta)}**\n\n"
        
        md += f"""---

✨ 由 [Daily Tech News Aggregator](https://github.com/1001Beidou/dailynews-doodle) 生成

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return md
    
    def save_reports(self):
        """保存所有格式的报告"""
        os.makedirs('reports', exist_ok=True)
        
        # 保存 HTML
        html_path = f'reports/daily_report_{self.date}.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_html())
        print(f"✅ HTML 报告已保存: {html_path}")
        
        # 保存 Markdown
        md_path = f'reports/daily_report_{self.date}.md'
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown())
        print(f"✅ Markdown 报告已保存: {md_path}")
        
        # 保存最新报告软链接
        with open('reports/daily_report.html', 'w', encoding='utf-8') as f:
            f.write(self.generate_html())
        with open('reports/daily_report.md', 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown())
        print(f"✅ 最新报告已更新")


def main():
    generator = ReportGenerator()
    generator.save_reports()


if __name__ == '__main__':
    main()
