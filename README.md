[![GitHub issues](https://img.shields.io/github/issues/layerqa/aiopayok?style=for-the-badge)](https://github.com/layerqa/aiopayok/issues)
[![GitHub license](https://img.shields.io/github/license/layerqa/aiopayok?style=for-the-badge)](https://github.com/layerqa/aiopayok/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/aiopayok?style=for-the-badge)](https://pypi.org/project/aiopayok/)
## AIOPayok

> payok.io asynchronous python wrapper

``` python
import asyncio

from aiopayok import Payok


payok = Payok("API_ID", "API_KEY")


async def main() -> None:
    print(await payok.get_balance())

asyncio.run(main())

```

### Installing

``` bash
pip install aiopayok
```

### Resources

- Check out the docs at https://payok.io/cabinet/documentation/doc_main.php to learn more about PayOk,
