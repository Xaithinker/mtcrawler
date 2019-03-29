
"""
抓取常用的代理并更新

1. 从一些免费代理网站抓取代理，周期性抓取
2. 使用Redis 作缓存。每隔约60s清库，因代理可用值大多为一分钟
3. TODO: 支持其他代理。模块化代理池调用
"""

from .xicidaili import Proxy, rediss

__all__ = ['Proxy', 'rediss']

