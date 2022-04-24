import aiofiles
import asyncio
import os
import queue

q = queue.Queue(maxsize=10000)


class Logger:

    def __init__(self):
        self.service_logfile = os.path.abspath(os.path.join(os.getcwd(), "logs", "service.access.log"))

    def output(self, log_msg: str):
        try:
            q.put_nowait(log_msg)
            self._to_files()

        except Exception as e:
            pass

    async def _to_write(self, msg):
        async with aiofiles.open(self.service_logfile, mode='a', newline='\n') as f:
            await f.write(msg + "\n")

    def _to_files(self):
        msg = q.get()
        task_list = [self._to_write(msg)]
        done, _ = asyncio.run(asyncio.wait(task_list))

