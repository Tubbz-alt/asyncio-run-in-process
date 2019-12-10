import asyncio
import os
from pathlib import (
    Path,
)

import pytest

from asyncio_run_in_process import (
    run_in_process,
)


@pytest.mark.asyncio
async def test_run_in_process_touch_file(touch_path):
    async def touch_file(path: Path):
        path.touch()

    assert not touch_path.exists()
    await asyncio.wait_for(run_in_process(touch_file, touch_path), timeout=2)
    assert touch_path.exists()


@pytest.mark.asyncio
async def test_run_in_process_with_result():
    async def return7():
        return 7

    result = await asyncio.wait_for(run_in_process(return7), timeout=2)
    assert result == 7


@pytest.mark.asyncio
async def test_run_in_process_with_error():
    async def raise_err():
        raise ValueError("Some err")

    with pytest.raises(ValueError, match="Some err"):
        await asyncio.wait_for(run_in_process(raise_err), timeout=2)


@pytest.mark.asyncio
async def test_run_in_process_pass_environment_variables():
    # sanity
    assert 'ASYNC_RUN_IN_PROCESS_ENV_TEST' not in os.environ

    async def return_env():
        return os.environ['ASYNC_RUN_IN_PROCESS_ENV_TEST']

    value = await run_in_process(
        return_env,
        subprocess_kwargs={'env': {'ASYNC_RUN_IN_PROCESS_ENV_TEST': 'test-value'}},
    )
    assert value == 'test-value'
