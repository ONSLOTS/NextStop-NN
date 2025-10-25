import slowapi
import slowapi.util

limiter = slowapi.Limiter(key_func=slowapi.util.get_remote_address)