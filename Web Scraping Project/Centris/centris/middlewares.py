from random import randint
import requests
import base64
import random
from scrapy.exceptions import IgnoreRequest

class ScrapeOpsFakeUserAgentMiddleware:
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_ENDPOINT', 'https://headers.scrapeops.io/v1/user-agents')
        self.scrapeops_fake_user_agent = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.user_agents_list = []
        self._scrapeops_fake_user_agent_enabled()
        self._get_user_agents_list()
    
    def _get_user_agents_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results:
            payload['num_results'] = self.scrapeops_num_results
        
        try:
            response = requests.get(self.scrapeops_endpoint, params=payload)
            json_response = response.json()
            self.user_agents_list = json_response.get('result', [])
            if len(self.user_agents_list) == 0:
                print("⚠️ No User Agents Found! Please Check Your API Key or ScrapeOps Endpoint URL")
        except Exception as e:
            print(f"❌ Failed to get User Agents: {e}")
    
    def _get_random_user_agent(self):
        if len(self.user_agents_list) == 0:
            self._get_user_agents_list()
        
        random_index = randint(0, len(self.user_agents_list) - 1)
        return self.user_agents_list[random_index]
    
    def _scrapeops_fake_user_agent_enabled(self):
        self.scrapeops_fake_user_agent = bool(self.scrapeops_fake_user_agent)
    
    def process_request(self, request, spider):
        if self.scrapeops_fake_user_agent:
            random_user_agent = self._get_random_user_agent()
            request.headers['User-Agent'] = random_user_agent
            # print("***** New Header Attached *****")
            # print(request.headers['User-Agent'])

class MyProxyMiddleware:
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.proxy_list = settings.get('ROTATING_PROXY_LIST', [])
        self.proxy_user = settings.get('PROXY_USER', None)
        self.proxy_password = settings.get('PROXY_PASSWORD', None)

    def process_request(self, request, spider):
        if self.proxy_list:
            proxy = self._get_random_proxy()
            request.meta['proxy'] = proxy

            if self.proxy_user and self.proxy_password:
                proxy_credentials = f"{self.proxy_user}:{self.proxy_password}"
                encoded_credentials = base64.b64encode(proxy_credentials.encode('utf-8')).decode('utf-8')
                request.headers['Proxy-Authorization'] = f'Basic {encoded_credentials}'
            spider.logger.info(f"🔥 Proxy Attached: {proxy}")
            
    def process_exception(self, request, exception, spider):
        if isinstance(exception, IgnoreRequest):
            spider.logger.warning(f"🚨 Proxy Failed: {request.meta.get('proxy', 'Unknown')}")
            new_proxy = self._get_random_proxy()
            request.meta['proxy'] = new_proxy
            spider.logger.info(f"🔄 Retrying with Proxy: {new_proxy}")
            return request

    def _get_random_proxy(self):
        return random.choice(self.proxy_list) if self.proxy_list else None