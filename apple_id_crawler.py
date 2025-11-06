"""
CC宝盒苹果ID爬虫 - 集成版
专门用于爬取 https://ccbaohe.com/appleID/ 并自动更新到网站后台
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from typing import List, Dict, Optional
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AppleIDCrawler:
    """苹果ID爬虫类 - 集成网站后台API"""
    
    def __init__(self, api_url: str = None):
        """
        初始化爬虫
        
        Args:
            api_url: 网站后台API地址（data_sync.php的URL）
        """
        self.base_url = "https://ccbaohe.com/appleID/"
        self.api_url = api_url  # 例如: "http://your-domain.com/data_sync.php"
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://ccbaohe.com/'
        })
        
        self.accounts = []
    
    def fetch_page(self) -> Optional[BeautifulSoup]:
        """获取网页内容"""
        try:
            logger.info(f"正在访问: {self.base_url}")
            response = self.session.get(self.base_url, timeout=15)
            response.raise_for_status()
            # 确保使用UTF-8编码
            if response.encoding.lower() not in ['utf-8', 'utf8']:
                response.encoding = 'utf-8'
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"请求失败: {e}")
            return None
    
    def extract_accounts(self, soup: BeautifulSoup) -> List[Dict]:
        """从页面中提取账号信息"""
        accounts = []
        
        # 方法1: 通过HTML结构提取（更可靠）
        accounts = self._extract_by_structure(soup)
        
        # 方法2: 如果方法1失败，使用正则表达式
        if not accounts:
            content = soup.get_text()
            pattern = r'#####\s*([^\n【]+)【([^】]+)】.*?账号状态[：:]\s*([^\n]+).*?检测时间[：:]\s*([^\n]+).*?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            matches = re.finditer(pattern, content, re.DOTALL)
            
            for match in matches:
                account_name = match.group(1).strip()
                region = match.group(2).strip()
                status = match.group(3).strip()
                check_time = match.group(4).strip()
                email = match.group(5).strip()
                
                password = self._extract_password(soup, account_name, email)
                
                account_info = {
                    'account': account_name,
                    'email': email,
                    'password': password,
                    'region': self._map_region(region),
                    'status': self._map_status(status),
                    'check_time': check_time,
                    'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                accounts.append(account_info)
        
        return accounts
    
    def _map_region(self, region: str) -> str:
        """映射地区代码"""
        region_map = {
            '美国': 'US',
            '中国': 'CN',
            '中国大陆': 'CN',
            '香港': 'HK',
            '台湾': 'TW',
            '日本': 'JP',
            '韩国': 'KR',
            '新加坡': 'SG',
            '英国': 'GB',
            '俄罗斯': 'RU',
            '越南': 'VN',
            '马来西亚': 'MY'
        }
        return region_map.get(region, 'US')
    
    def _map_status(self, status: str) -> str:
        """映射状态"""
        if '正常' in status:
            return '正常'
        elif '被锁' in status or '锁定' in status:
            return '被锁'
        else:
            return '共享账号'
    
    def _extract_password(self, soup: BeautifulSoup, account_name: str, email: str) -> str:
        """尝试提取密码"""
        password = ""
        
        # 方法1: 查找包含邮箱的元素，然后查找密码相关的data属性
        email_elements = soup.find_all(string=re.compile(re.escape(email)))
        
        for elem in email_elements:
            parent = elem.find_parent()
            if parent:
                current = parent
                for _ in range(5):
                    if current:
                        password_attr = (current.get('data-password') or 
                                        current.get('data-pwd') or 
                                        current.get('data-pass'))
                        if password_attr:
                            password = password_attr
                            break
                        
                        copy_btn = current.find(string=re.compile('复制密码'))
                        if copy_btn:
                            btn_parent = copy_btn.find_parent()
                            if btn_parent:
                                password_attr = (btn_parent.get('data-password') or 
                                                btn_parent.get('data-pwd') or
                                                btn_parent.get('data-pass'))
                                if password_attr:
                                    password = password_attr
                                    break
                                
                                onclick = btn_parent.get('onclick', '')
                                pwd_match = re.search(r'["\']([^"\']{6,})["\']', onclick)
                                if pwd_match:
                                    password = pwd_match.group(1)
                                    break
                        
                        current = current.find_parent()
                    
                    if password:
                        break
                
                if password:
                    break
        
        # 方法2: 从JavaScript代码中提取密码
        if not password:
            scripts = soup.find_all('script')
            for script in scripts:
                script_text = script.string or ""
                if email in script_text:
                    pwd_patterns = [
                        r'["\']([^"\']{6,})["\']',
                        r'password["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                        r'pwd["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                    ]
                    for pattern in pwd_patterns:
                        matches = re.findall(pattern, script_text)
                        if matches:
                            password = matches[-1]
                            break
        
        return password
    
    def _decode_cf_email(self, cf_email_element) -> str:
        """解码Cloudflare保护的邮箱"""
        try:
            # 尝试从data-cfemail属性获取
            cf_email = cf_email_element.get('data-cfemail', '')
            if not cf_email:
                # 尝试从href中提取
                href = cf_email_element.get('href', '')
                if 'email-protection#' in href:
                    cf_email = href.split('email-protection#')[-1]
            
            if cf_email:
                # Cloudflare邮箱解码算法
                # 将十六进制字符串转换为字节
                r = int(cf_email[:2], 16)
                email = ''.join([chr(int(cf_email[i:i+2], 16) ^ r) for i in range(2, len(cf_email), 2)])
                return email
        except:
            pass
        
        # 如果解码失败，返回空字符串
        return ""
    
    def _extract_by_structure(self, soup: BeautifulSoup) -> List[Dict]:
        """通过HTML结构提取账号信息 - 基于实际HTML结构"""
        accounts = []
        
        # 查找所有card元素（每个账号一个card）
        cards = soup.find_all('div', class_='card', attrs={'style': True})
        logger.info(f"找到 {len(cards)} 个card元素")
        
        for card in cards:
            try:
                # 提取h5标签中的账号名和地区
                h5 = card.find('h5', class_='my-0')
                if not h5:
                    continue
                
                # 从h5中提取账号名和地区
                h5_text = h5.get_text()
                account_name = ""
                region = ""
                
                # 提取账号名和地区（从span中）
                spans = h5.find_all('span')
                for span in spans:
                    text = span.get_text().strip()
                    # 提取账号名
                    if '@' in text or '***' in text:
                        account_name = text
                    # 提取地区（从span中查找【地区】格式）- 支持多种编码
                    # 注意：排除"CC宝盒"等品牌名称
                    if not region:
                        # 方法1: 标准【】格式
                        region_match = re.search(r'【([^】]+)】', text)
                        if region_match:
                            potential_region = region_match.group(1).strip()
                            # 过滤掉品牌名称
                            if potential_region and 'CC宝盒' not in potential_region and 'ccbaohe' not in potential_region.lower():
                                region = potential_region
                        else:
                            # 方法2: 可能是编码问题，尝试查找包含地区关键词的文本
                            region_keywords = ['香港', '美国', '中国', '台湾', '日本', '韩国', '新加坡', '英国', '俄罗斯', '越南', '马来西亚']
                            for keyword in region_keywords:
                                if keyword in text and 'CC宝盒' not in text:
                                    region = keyword
                                    break
                
                # 如果从span中没找到地区，再从整个h5文本中查找（排除CC宝盒）
                if not region:
                    # 方法1: 标准【】格式
                    region_match = re.search(r'【([^】]+)】', h5_text)
                    if region_match:
                        potential_region = region_match.group(1).strip()
                        # 过滤掉品牌名称
                        if potential_region and 'CC宝盒' not in potential_region and 'ccbaohe' not in potential_region.lower():
                            region = potential_region
                    else:
                        # 方法2: 查找地区关键词（排除CC宝盒）
                        region_keywords = ['香港', '美国', '中国', '台湾', '日本', '韩国', '新加坡', '英国', '俄罗斯', '越南', '马来西亚']
                        for keyword in region_keywords:
                            if keyword in h5_text and 'CC宝盒' not in h5_text:
                                region = keyword
                                break
                
                # 如果没找到账号名，从h5文本中提取
                if not account_name:
                    account_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', h5_text)
                    if not account_match:
                        account_match = re.search(r'([a-zA-Z0-9]+\*\*\*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', h5_text)
                    if account_match:
                        account_name = account_match.group(1)
                
                # 如果账号名包含***，尝试从card-body中获取完整邮箱
                card_body = card.find('div', class_='card-body')
                if not card_body:
                    continue
                
                # 提取邮箱（Cloudflare保护）
                email = ""
                cf_email_elem = card_body.find('a', class_='__cf_email__')
                if cf_email_elem:
                    email = self._decode_cf_email(cf_email_elem)
                
                # 如果解码失败，尝试从data-cfemail属性解码
                if not email:
                    cf_email_span = card_body.find('span', class_='__cf_email__')
                    if cf_email_span:
                        email = self._decode_cf_email(cf_email_span)
                
                # 提取密码（从按钮的onclick中）- 改进版
                password = ""
                password_buttons = card_body.find_all('button')
                
                for btn in password_buttons:
                    btn_text = btn.get_text().strip()
                    onclick = btn.get('onclick', '')
                    
                    # 检查是否是密码按钮（更宽松的条件）
                    is_password_btn = (
                        '密码' in btn_text or 
                        'copy(' in onclick.lower() or
                        ('复制' in btn_text and len(onclick) > 10)
                    )
                    
                    if is_password_btn and onclick:
                        # 尝试多种模式匹配密码（按优先级）
                        patterns = [
                            (r"copy\(['\"]([^'\"]+)['\"]\)", "copy('密码')"),
                            (r"copy\(['\"]?([A-Za-z0-9]{4,20})['\"]?\)", "copy(密码)宽松"),
                            (r"copy\(['\"]([^'\"]+)['\"]", "copy('密码（不完整）"),
                            (r"copy\(([^\)]+)\)", "copy(密码)"),
                            (r"['\"]([A-Za-z0-9]{6,})['\"]", "引号中的字母数字"),
                            (r"['\"]([^'\"]{4,20})['\"]", "引号中4-20字符"),
                        ]
                        
                        for pattern, desc in patterns:
                            pwd_match = re.search(pattern, onclick)
                            if pwd_match:
                                potential_pwd = pwd_match.group(1).strip()
                                # 更严格的过滤
                                if (len(potential_pwd) >= 4 and 
                                    len(potential_pwd) <= 30 and
                                    not potential_pwd.startswith('http') and
                                    not potential_pwd.startswith('window') and
                                    not potential_pwd.startswith('return') and
                                    not potential_pwd.startswith('if') and
                                    not 'function' in potential_pwd.lower() and
                                    not potential_pwd.startswith('__') and
                                    re.match(r'^[A-Za-z0-9_\-]+$', potential_pwd)):  # 只包含字母数字下划线横线
                                    password = potential_pwd
                                    break
                        
                        if password:
                            break
                
                # 如果还没找到，尝试从所有按钮中查找（不限制按钮文本）
                if not password:
                    for btn in password_buttons:
                        onclick = btn.get('onclick', '')
                        if 'copy(' in onclick.lower() and len(onclick) > 20:
                            # 尝试提取
                            pwd_match = re.search(r"copy\(['\"]?([A-Za-z0-9]{4,20})['\"]?\)", onclick)
                            if pwd_match:
                                potential_pwd = pwd_match.group(1).strip()
                                if (re.match(r'^[A-Za-z0-9_\-]+$', potential_pwd) and
                                    not potential_pwd.startswith('http')):
                                    password = potential_pwd
                                    break
                
                # 提取状态
                status = "正常"
                status_elem = card_body.find('p', class_='card-title')
                if status_elem:
                    status_text = status_elem.get_text()
                    if '账号状态' in status_text:
                        status_match = re.search(r'账号状态[：:]\s*([^\n]+)', status_text)
                        if status_match:
                            status = status_match.group(1).strip()
                
                # 提取检测时间
                check_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 查找所有card-text元素
                time_elems = card_body.find_all('p', class_='card-text')
                for time_elem in time_elems:
                    time_text = time_elem.get_text().strip()
                    # 检查是否包含时间信息
                    if '检测时间' in time_text or '更新' in time_text or re.search(r'\d{4}-\d{2}-\d{2}', time_text):
                        # 尝试多种时间格式
                        time_patterns = [
                            r'检测时间[：:]\s*([^\n]+)',  # 检测时间：2025-11-07 01:34:08
                            r'检测时间[：:]\s*([0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2})',  # 完整时间格式
                            r'([0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2})',  # 直接匹配时间格式
                            r'(\d+分钟前更新)',  # 30分钟前更新
                            r'(\d+小时前更新)',  # 1小时前更新
                        ]
                        for pattern in time_patterns:
                            time_match = re.search(pattern, time_text)
                            if time_match:
                                check_time = time_match.group(1).strip()
                                break
                        if check_time != datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                            break
                
                # 如果地区为空，尝试从card-body中查找（但要排除状态区域）
                if not region:
                    # 只从card-body的文本中查找，但要排除状态区域（card-title）
                    # 先排除状态区域
                    status_elem = card_body.find('p', class_='card-title')
                    card_body_text = card_body.get_text()
                    if status_elem:
                        # 从card_body_text中移除状态区域的文本
                        status_text = status_elem.get_text()
                        card_body_text = card_body_text.replace(status_text, '')
                    
                    region_match = re.search(r'【([^】]+)】', card_body_text)
                    if region_match:
                        potential_region = region_match.group(1).strip()
                        # 过滤掉品牌名称
                        if potential_region and 'CC宝盒' not in potential_region and 'ccbaohe' not in potential_region.lower():
                            region = potential_region
                
                # 只保留账号和密码都成功获取的记录
                if email or account_name:
                    # 如果没有邮箱，使用账号名
                    if not email:
                        email = account_name
                    
                    # 如果密码为空或未获取，跳过此账号
                    if not password or password.strip() == "":
                        logger.info(f"跳过账号（密码未获取）: {email} ({region or '未知'})")
                        continue
                    
                    # 只添加账号和密码都成功的记录
                    accounts.append({
                        'account': account_name,
                        'email': email,
                        'fullEmail': email,
                        'password': password,
                        'region': self._map_region(region) if region else 'US',
                        'regionName': region if region else '美国',
                        'status': self._map_status(status),
                        'checkTime': check_time if check_time else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    logger.info(f"✅ 提取账号: {email} ({region or '未知'}) 密码: {password[:10]}...")
            
            except Exception as e:
                logger.warning(f"提取账号时出错: {e}")
                continue
        
        return accounts
    
    def _extract_password_from_container(self, container, email: str) -> str:
        """从容器中提取密码 - 从按钮onclick中提取"""
        password = ""
        
        # 查找所有包含"复制密码"的按钮
        buttons = container.find_all('button')
        for btn in buttons:
            btn_text = btn.get_text()
            if '复制密码' in btn_text:
                onclick = btn.get('onclick', '')
                if onclick and 'copy(' in onclick:
                    # 提取copy('密码')中的密码
                    pwd_match = re.search(r"copy\(['\"]([^'\"]+)['\"]\)", onclick)
                    if pwd_match:
                        password = pwd_match.group(1)
                        break
        
        return password
    
    def crawl(self) -> List[Dict]:
        """执行爬取"""
        logger.info("开始爬取苹果ID账号...")
        
        soup = self.fetch_page()
        if not soup:
            logger.error("无法获取网页内容")
            return []
        
        accounts = self.extract_accounts(soup)
        self.accounts = accounts
        
        logger.info(f"成功提取 {len(accounts)} 个账号")
        return accounts
    
    def _load_vpn_ads(self) -> List[Dict]:
        """加载VPN广告数据（从文件或使用默认值）"""
        import os
        # 尝试从文件读取
        vpn_file = 'vpn_ads.json'
        if os.path.exists(vpn_file):
            try:
                with open(vpn_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and 'vpn_ads' in data:
                        return data['vpn_ads']
            except:
                pass
        
        # 如果没有文件，返回空数组（保持原样，不修改）
        return []
    
    def format_for_api(self, max_accounts: int = None) -> Dict:
        """
        格式化数据为API格式（符合网站要求）
        
        Args:
            max_accounts: 每个分组最大账号数（None表示使用所有账号）
        """
        import time
        
        # 转换为现有系统的格式
        formatted_accounts = []
        accounts_to_format = self.accounts[:max_accounts] if max_accounts else self.accounts
        
        for i, acc in enumerate(accounts_to_format, 1):
            # 获取地区信息
            region_text = acc.get('regionName', '').strip() or acc.get('region', '').strip()
            # 如果region为空，默认使用"美国"
            if not region_text:
                region_text = '美国'
            
            # 映射地区代码
            region_name_map = {
                '美国': 'US', '中国': 'CN', '香港': 'HK', '台湾': 'TW',
                '日本': 'JP', '韩国': 'KR', '新加坡': 'SG', '英国': 'GB',
                '俄罗斯': 'RU', '越南': 'VN', '马来西亚': 'MY'
            }
            region_code = region_name_map.get(region_text, 'US')
            region_name = region_text  # 使用region_text（如果为空则已经是"美国"）
            
            formatted_accounts.append({
                'id': f'1-{i}',
                'fullEmail': acc.get('fullEmail') or acc.get('email', ''),
                'password': acc.get('password', ''),
                'status': acc.get('status', '正常'),
                'checkTime': acc.get('checkTime') or acc.get('crawl_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'region': region_code,
                'regionName': region_name
            })
        
        # 加载VPN广告数据（保持原样，不修改）
        vpn_ads = self._load_vpn_ads()
        
        # 生成Unix时间戳
        timestamp = int(time.time())
        
        # 返回符合网站要求的格式
        return {
            'timestamp': timestamp,
            'data': {
                'accounts': {
                    'group1': formatted_accounts,
                    'group2': []  # group2保持为空
                },
                'vpn_ads': vpn_ads  # VPN广告部分保持原样，不修改
            }
        }
    
    def sync_to_api(self) -> bool:
        """
        同步数据到网站后台API
        
        Returns:
            是否同步成功
        """
        if not self.api_url:
            logger.warning("未配置API URL，跳过同步")
            return False
        
        try:
            formatted_data = self.format_for_api()
            
            logger.info(f"正在同步 {len(formatted_data['data']['accounts']['group1'])} 个账号到API...")
            
            response = self.session.post(
                f"{self.api_url}?type=accounts",
                json=formatted_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                logger.info(f"✅ 数据同步成功！时间戳: {result.get('timestamp')}")
                return True
            else:
                logger.error(f"❌ 同步失败: {result.get('error', '未知错误')}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"❌ API同步失败: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ 同步过程出错: {e}")
            return False
    
    def save_to_json(self, filename: str = 'apple_ids.json'):
        """保存到JSON文件"""
        data = {
            'total': len(self.accounts),
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_url': self.base_url,
            'accounts': self.accounts
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"已保存 {len(self.accounts)} 个账号到 {filename}")
    
    def save_to_simple_json(self, filename: str = 'apple_ids_simple.json'):
        """保存简化版JSON（仅账号密码）"""
        simple_data = []
        for acc in self.accounts:
            simple_data.append({
                'email': acc.get('fullEmail') or acc.get('email', ''),
                'password': acc.get('password', ''),
                'region': acc.get('region', 'US')
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(simple_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"已保存简化数据到 {filename}")


def main():
    """主函数"""
    import sys
    
    # 从命令行参数或环境变量获取API URL
    api_url = None
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        # 可以从配置文件读取
        api_url = os.environ.get('API_URL')
    
    crawler = AppleIDCrawler(api_url=api_url)
    accounts = crawler.crawl()
    
    if accounts:
        # 保存本地文件
        crawler.save_to_json('apple_ids.json')
        crawler.save_to_simple_json('apple_ids_simple.json')
        
        # 同步到API（如果配置了）
        if api_url:
            crawler.sync_to_api()
        
        print(f"\n爬取完成！共提取 {len(accounts)} 个账号")
        print("\n前5个账号示例:")
        for i, acc in enumerate(accounts[:5], 1):
            email = acc.get('fullEmail') or acc.get('email', '')
            print(f"{i}. {email} | {acc.get('region', 'US')} | {acc.get('status', '正常')}")
    else:
        print("未提取到账号信息，请检查网站结构或网络连接")


if __name__ == '__main__':
    import os
    main()
