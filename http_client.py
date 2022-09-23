import asyncio
import atexit
from aiohttp import ClientTimeout, ClientSession, TCPConnector


@atexit.register
def close_session():
    asyncio.get_event_loop().run_until_complete(HttpClient.close_session())


class HttpClient:
    """
    一个应用中共用一个session,用于提高效率
    """
    _connector = TCPConnector(limit=2000)
    _session = ClientSession(timeout=ClientTimeout(60),
                             raise_for_status=True,
                             connector=_connector)

    @classmethod
    async def close_session(cls):
        """
        切记不要在代码中手动调用
        Returns:

        """
        await cls._session.close()

    @classmethod
    async def get(cls, url, return_type="json", **kwargs):
        """

        Args:
            url: 请求的url
            return_type: json, raw, text三种
            **kwargs:

        Returns:

        """
        return await cls._request("get", url, return_type=return_type, **kwargs)

    @classmethod
    async def post(cls, url, return_type="json", **kwargs):
        """

        Args:
            url:
            return_type: return_type: json, raw, text三种
            **kwargs:

        Returns:

        """
        return await cls._request("post", url, return_type=return_type, **kwargs)

    @classmethod
    async def put(cls, url, return_type="json", **kwargs):
        return await cls._request("put", url, return_type=return_type, **kwargs)

    @classmethod
    async def delete(cls, url, return_type="json", **kwargs):
        return await cls._request("delete", url, return_type=return_type, **kwargs)

    @classmethod
    async def _request(cls, method, url, return_type, **kwargs):
        try:
            trace_info = kwargs.pop("trace_info", {})
            trace_request_ctx = {"trace_info": trace_info, "request_ctx": kwargs}
            async with cls._session.request(method,
                                            url,
                                            **kwargs,
                                            trace_request_ctx=trace_request_ctx) as resp:
                resp.raise_for_status()
                if return_type == "json":
                    return await resp.json(content_type=None)
                if return_type == "raw":
                    return await resp.read()
                if return_type == "text":
                    return await resp.text()
                raise Exception(f"not accepted return_type {return_type}")
        except Exception as e:
            _waiters = len(cls._connector._waiters)
            _acquired = len(cls._connector._acquired)
            limit = cls._connector.limit
            timeout = cls._session.timeout.total
            print(
                "%r, %s %s, kwargs %s, connector [_acquired %s, _waiters %s, limit %s, timeout %s]",
                e, method, url, kwargs, _acquired, _waiters, limit, timeout)
            raise e

    @classmethod
    async def request_get_resp(cls, method, url, **kwargs):
        """
        返回原始resp对象
        Args:
            method: http请求类型
            url: 请求的url
            **kwargs:

        Returns:

        """
        trace_info = kwargs.pop("trace_info", {})
        trace_request_ctx = {"trace_info": trace_info, "request_ctx": kwargs}
        return await cls._session.request(method, url, **kwargs, trace_request_ctx=trace_request_ctx)
