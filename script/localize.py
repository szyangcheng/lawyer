"""Generate static language pages from the shared Jekyll build; no runtime translation."""
import argparse,json,re,shutil
from pathlib import Path
from urllib.parse import urlparse,unquote
from bs4 import BeautifulSoup,Comment,Doctype
from opencc import OpenCC
parser=argparse.ArgumentParser();parser.add_argument('--build',required=True);parser.add_argument('--source',required=True);args=parser.parse_args()
source=Path(args.source);build=Path(args.build);data=Path(__file__).parent/'i18n'
translations=json.loads((data/'en.json').read_text());articles=json.loads((data/'articles-en.json').read_text());cc=OpenCC('s2t')
extra={'跳至正文':'Skip to content','杨铖律师肖像':'Portrait of Yang Cheng','杨铖律师，首页':'Yang Cheng, home','主导航':'Main navigation','语言 / Language':'Language','输入关键词，如合同、隐私、充电桩':'Enter a keyword, e.g. contract or privacy','文章分类':'Article categories','阅读：':'Read: ','关于杨铖':'About Yang Cheng','友情链接':'Legal resources','中国人大网':'National People’s Congress of China','中国政府网':'Central People’s Government of China','中华人民共和国最高人民法院':'Supreme People’s Court of China','中华人民共和国最高人民检察院':'Supreme People’s Procuratorate of China','中国律师网':'All China Lawyers Association','深圳市律师协会':'Shenzhen Lawyers Association','北京市隆安律师事务所':'Long An Law Firm','我的知乎主页':'My Zhihu profile','搜索文章':'Search articles','文章搜索与分类已整合至文章列表。':'Search and filters are available in the article library.','前往搜索文章 →':'Search articles →','没有找到这个页面':'Page not found','链接可能已变更，也可以从文章列表查找需要的内容。':'The link may have changed. You can look for the content in the article library.','返回首页':'Home','浏览文章 →':'Browse articles →','AI相关文章':'Articles about AI','浏览全部文章 →':'View all articles →','企业与个人法律服务':'Legal services for businesses and individuals','个人权益':'Individual rights','公共事务':'Public affairs','科技与法律':'Technology & law','房产与生活':'Property & everyday life','企业与劳动':'Business & employment','律师随笔':'Personal reflections','随笔':'Reflections','原文链接':'Original article','随笔与动态':'Reflections & updates'}
translations.update(extra)
for title,a in articles.items():translations[title]=a['title']
# Translate original post summaries appearing on library/home cards.
import yaml
for p in (source/'_posts').glob('*.md'):
 chunks=p.read_text().split('---',2)
 if len(chunks)<3:continue
 meta=yaml.safe_load(chunks[1]) or {};title=meta.get('title') or p.stem[11:]
 if title in articles and meta.get('summary'):translations[meta['summary']]=articles[title]['summary']
def english(text):
 stripped=text.strip()
 if stripped in translations:result=translations[stripped]
 else:
  result=stripped
  for zh,en in sorted(translations.items(),key=lambda x:len(x[0]),reverse=True):
   if zh in result:result=result.replace(zh,en)
  result=re.sub(r'(\d{4})年(\d{2})月(\d{2})日',r'\1-\2-\3',result)
 return text[:len(text)-len(text.lstrip())]+result+text[len(text.rstrip()):]
htmls=[p for p in build.rglob('*.html') if p.relative_to(build).parts[0] not in ('en','zh-hant')]; routes={}
for p in htmls:
 rel=p.relative_to(build).as_posix();routes[p]='/' + (rel[:-10] if rel.endswith('index.html') else rel)
unknown=set()
for locale,prefix in [('zh-Hant','/zh-hant'),('en','/en')]:
 folder=source/prefix[1:]
 if folder.exists():shutil.rmtree(folder)
 for p in htmls:
  route=routes[p];soup=BeautifulSoup(p.read_text(),'html.parser')
  soup.html['lang']=locale
  reading=soup.select_one('.reading-page')
  if locale=='en' and reading:
   oldtitle=soup.h1.get_text();entry=articles[oldtitle];date=reading.select_one('time').get('datetime','')[:10]
   topic=reading.select_one('.eyebrow').get_text()
   reading.clear()
   content=BeautifulSoup('<a class="back-link" href="/articles/">← Articles & insights</a><header class="reading-header"><p class="eyebrow"></p><h1></h1><p class="article-meta">Yang Cheng · <time></time></p></header><aside class="archive-note">English title and summary. The full article remains in its original Chinese. This is an archived article, not an update on current law.</aside><div class="prose article-body"><p></p><p><a class="button" data-original="true">Read the original Chinese article ↗</a></p></div>','html.parser')
   content.h1.string=entry['title'];content.select_one('.eyebrow').string=english(topic);content.time.string=date;content.time['datetime']=date
   content.select_one('.article-body p').string=entry['summary'];content.select_one('[data-original]')['href']=route
   for child in list(content.contents):reading.append(child)
  for node in list(soup.find_all(string=True)):
   if isinstance(node,(Comment,Doctype)) or node.parent.name in ['script','style']:continue
   if node.find_parent(class_='language-bar'):continue
   text=str(node);translated=cc.convert(text) if locale=='zh-Hant' else english(text)
   node.replace_with(translated)
   if locale=='en' and re.search('[\u4e00-\u9fff]',translated) and translated.strip()!='铖':unknown.add(translated.strip())
  for tag in soup.find_all(True):
   for attr in ['alt','aria-label','placeholder','title']:
    if tag.has_attr(attr):tag[attr]=cc.convert(tag[attr]) if locale=='zh-Hant' else english(tag[attr])
   if tag.has_attr('href') and tag.name=='a' and not tag.find_parent(class_='language-bar') and not tag.has_attr('data-original'):
    href=tag['href'];u=urlparse(href)
    if href.startswith('/') and not href.startswith('//') and not href.startswith('/assets/') and href!='/feed.xml':tag['href']=prefix+href
  bar=soup.select_one('.language-bar')
  for a in bar.select('a'):
   lang=a['hreflang'];a['href']=('' if lang=='zh-Hans' else '/zh-hant' if lang=='zh-Hant' else '/en')+route
   a.attrs.pop('aria-current',None)
   if lang==locale:a['aria-current']='true'
  for tag in soup.select('link[rel="canonical"]'):tag['href']='https://yangchenglawyer.com'+prefix+route
  for tag in soup.select('meta[property="og:url"]'):tag['content']='https://yangchenglawyer.com'+prefix+route
  for tag in soup.select('meta[property="og:locale"]'):tag['content']='zh_TW' if locale=='zh-Hant' else 'en_US'
  for tag in soup.select('meta[name="description"], meta[property="og:description"], meta[property="og:title"], meta[name="twitter:title"]'):
   tag['content']=cc.convert(tag['content']) if locale=='zh-Hant' else english(tag['content'])
   if locale=='en' and re.search('[\u4e00-\u9fff]',tag['content']):tag['content']=soup.h1.get_text()+' · Yang Cheng, Partner and PRC Lawyer in Shenzhen.'
  for script in soup.select('script[type="application/ld+json"]'):
   script.string=json.dumps({'@context':'https://schema.org','@type':'WebPage','name':soup.h1.get_text() if soup.h1 else 'Yang Cheng','url':'https://yangchenglawyer.com'+prefix+route,'inLanguage':locale},ensure_ascii=False)
  if soup.title:soup.title.string=cc.convert(soup.title.get_text()) if locale=='zh-Hant' else english(soup.title.get_text())
  dest=folder/p.relative_to(build);dest.parent.mkdir(parents=True,exist_ok=True)
  dest.write_text('---\nlayout: null\npermalink: '+json.dumps(prefix+route,ensure_ascii=False)+'\n---\n'+str(soup))
print('Generated',len(htmls),'pages per language; untranslated English text:',sorted(unknown))

if unknown:raise SystemExit("Add missing English translations before publishing.")
