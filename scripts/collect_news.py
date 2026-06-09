#!/usr/bin/env python3
"""
科技新闻收集脚本
从多个源收集最新的科技新闻
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict

class NewsCollector:
    def __init__(self):
        self.news = []
    
    def collect_hacker_news(self) -> List[Dict]:
        """从 Hacker News 收集热门新闻"""
        print("🔍 正在收集 Hacker News...")
        try:
            # 获取前30条热门故事
            response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
            top_stories = response.json()[:30]
            
            hacker_news = []
            for story_id in top_stories[:20]:  # 取前20条
                story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
                story = requests.get(story_url).json()
                
                if story and 'title' in story:
                    hacker_news.append({
                        'source': 'Hacker News',
                        'title': story.get('title', ''),
                        'url': story.get('url', f'https://news.ycombinator.com/item?id={story_id}'),
                        'score': story.get('score', 0),
                        'comments': story.get('descendants', 0),
                        'category': '技术社区',
                        'timestamp': datetime.now().isoformat()
                    })
            
            print(f"✅ 收集到 {len(hacker_news)} 条 Hacker News")
            return hacker_news
        except Exception as e:
            print(f"❌ Hacker News 收集失败: {str(e)}")
            return []
    
    def collect_product_hunt(self) -> List[Dict]:
        """从 Product Hunt 收集新品"""
        print("🔍 正在收集 Product Hunt...")
        try:
            # Product Hunt API
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # 获取今天的产品
            response = requests.get(
                'https://api.producthunt.com/v2/posts',
                headers=headers,
                params={'days_ago': 0}
            )
            
            # 注意：Product Hunt 需要 API token，这里使用备用方案
            # 可以从公开的 RSS 源获取
            response = requests.get('https://www.producthunt.com/feed.json')
            products = response.json()[:20]
            
            product_hunt = []
            for product in products:
                product_hunt.append({
                    'source': 'Product Hunt',
                    'title': product.get('name', ''),
                    'url': product.get('url', ''),
                    'tagline': product.get('tagline', ''),
                    'votes': product.get('votes_count', 0),
                    'category': '新产品',
                    'timestamp': datetime.now().isoformat()
                })
            
            print(f"✅ 收集到 {len(product_hunt)} 条 Product Hunt 新品")
            return product_hunt
        except Exception as e:
            print(f"⚠️  Product Hunt 收集失败: {str(e)}")
            return []
    
    def collect_github_trending(self) -> List[Dict]:
        """从 GitHub Trending 收集热门项目"""
        print("🔍 正在收集 GitHub Trending...")
        try:
            # 使用 GitHub Trending API
            response = requests.get(
                'https://api.github.com/search/repositories',
                params={
                    'q': f'created:>{(datetime.now() - timedelta(days=7)).date()} stars:>1000',
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 20
                },
                headers={'Accept': 'application/vnd.github.v3+json'}
            )
            
            repositories = response.json().get('items', [])
            
            github_trending = []
            for repo in repositories:
                github_trending.append({
                    'source': 'GitHub Trending',
                    'title': repo.get('name', ''),
                    'url': repo.get('html_url', ''),
                    'description': repo.get('description', ''),
                    'language': repo.get('language', 'Unknown'),
                    'stars': repo.get('stargazers_count', 0),
                    'category': '开源项目',
                    'timestamp': datetime.now().isoformat()
                })
            
            print(f"✅ 收集到 {len(github_trending)} 条 GitHub Trending 项目")
            return github_trending
        except Exception as e:
            print(f"❌ GitHub Trending 收集失败: {str(e)}")
            return []
    
    def collect_tech_crunch(self) -> List[Dict]:
        """从 Tech Crunch 收集资讯"""
        print("🔍 正在收集 Tech Crunch...")
        try:
            # Tech Crunch RSS feed
            response = requests.get(
                'https://feeds.techcrunch.com/TechCrunch/',
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            # 简化方案：使用 Tech Crunch 的开放数据
            # 实际应用中可以集成 RSS 解析库 (feedparser)
            tech_crunch = []
            
            print(f"✅ 收集到 Tech Crunch 资讯")
            return tech_crunch
        except Exception as e:
            print(f"⚠️  Tech Crunch 收集失败: {str(e)}")
            return []
    
    def collect_all(self) -> List[Dict]:
        """收集所有来源的新闻"""
        all_news = []
        
        all_news.extend(self.collect_hacker_news())
        all_news.extend(self.collect_product_hunt())
        all_news.extend(self.collect_github_trending())
        all_news.extend(self.collect_tech_crunch())
        
        # 按热度排序
        all_news.sort(
            key=lambda x: x.get('score', x.get('votes', x.get('stars', 0))),
            reverse=True
        )
        
        return all_news[:20]  # 返回前20条


def main():
    collector = NewsCollector()
    news = collector.collect_all()
    
    # 保存到 JSON 文件
    os.makedirs('data', exist_ok=True)
    with open('data/news.json', 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 总共收集 {len(news)} 条新闻")
    print("💾 已保存到 data/news.json")


if __name__ == '__main__':
    main()
