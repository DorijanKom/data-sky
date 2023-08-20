import socket

from django_redis.client import DefaultClient
from django_redis.exceptions import ConnectionInterrupted
from redis.exceptions import ConnectionError, ResponseError, TimeoutError


class CustomRedisClient(DefaultClient):
    _main_exceptions = (TimeoutError, ResponseError, ConnectionError, socket.timeout)

    def execute_redis_command(self, method, key, *args, **options):
        nkey = self.make_key(key)
        tried = []

        while True:
            try:
                client, index = self.get_client(write=True, show_index=True)
                return client.execute_command(method, nkey, *args, **options)

            except CustomRedisClient._main_exceptions as e:
                if not self._slave_read_only and len(tried) < len(self._server):
                    tried.append(index)
                    client = None
                    continue
                raise ConnectionInterrupted(connection=client, parent=e)

    def sadd(self, key, *values):
        "Add ``value(s)`` to set ``key``"
        return self.execute_redis_command("SADD", key, *values)

    def scard(self, key):
        "Return the number of elements in set ``key``"
        return self.execute_redis_command("SCARD", key)

    def spop(self, key):
        "Remove and return a random member of set ``key``"
        return self.execute_redis_command("SPOP", key)

    def rpush(self, name, *values):
        "Push ``values`` onto the tail of the list ``name``"
        return self.execute_redis_command("RPUSH", name, *values)

    def lrange(self, name, start, end):
        """
        Return a slice of the list ``name`` between
        position ``start`` and ``end``

        ``start`` and ``end`` can be negative numbers just like
        Python slicing notation
        """
        return self.execute_redis_command("LRANGE", name, start, end)
