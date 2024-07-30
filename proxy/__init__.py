from abc import ABC, abstractmethod
from typing import Literal, Union
import requests
    

class ProxyABC(ABC):
    @abstractmethod
    def get_protocol(self) -> str | None:
        """
        :return: protocol if proxy is working or None if not
        """
        pass

    def to_user_format_string(self) -> str:
        """
        Convert the proxy configuration to a string in the format "ip:port[:username:password]".

        Returns:
            str: A string representation of the proxy configuration.
        """
        pass

    def to_selenium_wire_options(self) -> dict:
        """
        Returns proxy in selenium_wire options
        """
        pass


class EmptyProxy(ProxyABC):
    """
    Represents an empty proxy configuration with no specific values set.
    """
    def __init__(self):

        self.host: str | None = None
        self.port: int | None = None
        self.username: str | None = None
        self.userpass: str | None = None
        self.protocol: Literal["HTTP", "HTTPS", "SOCKS5"] | None = None

    def get_protocol(self) -> str | None:

        return None

    def to_user_format_string(self) -> str:

        return ""

    def to_selenium_wire_options(self) -> dict:

        return {}


class Proxy(ProxyABC):
    """
    Represents a proxy configuration with IP, port, protocol, and optional username and password.
    """

    def __init__(self,
                 host: str,
                 port: int,
                 username: str | None = None,
                 userpass: str | None = None):

        self.host = host
        self.port = port
        self.username = username
        self.userpass = userpass
        self.protocol = None

    def get_protocol(self) -> None | str:
        import logging
        logger = logging.getLogger(__name__)

        # Test proxy protocols (HTTP, HTTPS, SOCKS5) to determine which one is valid
        logger.info(f'checking proxy: {self.host, self.port}')
        proxies_str = f'{self.username}:{self.userpass}@{self.host}:{self.port}'
        logger.info("proxy string initialized")

        for protocol in ('socks5', 'https', 'http'):
            logger.info(f'checking proxy protocol')
            proxies = {"http": f"{protocol}://{proxies_str}",
                       'https': f"{protocol}://{proxies_str}",
                       "socks5": f"{protocol}://{proxies_str}"}
            logger.info("proxy protocol initialized")
            try:
                response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=6)
                logger.info(f'response status code: {response.status_code}')
                if response.status_code == 200:
                    logger.info(f'proxy {self.host}:{self.port} is working')
                    logger.info(f'proxy protocol for {self.host}:{self.port} is: {protocol}')
                    return protocol
            except Exception as error:
                continue

        return None

    @staticmethod
    def from_user_format_string(proxy_string: str) -> Union[EmptyProxy, 'Proxy']:
        splitted = proxy_string.split(':')



        try:
            if len(splitted) == 4:

                return Proxy(host=splitted[0],
                             port=int(splitted[1]),
                             username=splitted[2],
                             userpass=splitted[3])

            elif len(splitted) == 2:

                return Proxy(host=splitted[0],
                             port=int(splitted[1]))

            else:

                return EmptyProxy()
        except ValueError:

            return EmptyProxy()

    def to_user_format_string(self) -> str:
        proxy_string = f'{self.host}:{self.port}'


        if (self.username is not None
                and self.userpass is not None):
            proxy_string += f':{self.username}:{self.userpass}'

        return proxy_string

    def to_selenium_wire_options(self) -> dict:
        protocol = self.get_protocol()

        if protocol:

            return {'proxy': {'http': f'{protocol}://{self.username}:{self.userpass}@{self.host}:{self.port}',
                              'https': f'{protocol}://{self.username}:{self.userpass}@{self.host}:{self.port}',
                              'no_proxy': 'localhost,127.0.0.1'}}
        else:

            return {'proxy': {'http': f'http://{self.username}:{self.userpass}@{self.host}:{self.port}',
                              'https': f'https://{self.username}:{self.userpass}@{self.host}:{self.port}',
                              'no_proxy': 'localhost,127.0.0.1'}}
