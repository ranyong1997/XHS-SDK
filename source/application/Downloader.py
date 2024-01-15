from pathlib import Path
from aiohttp import ClientError
from source.module import ERROR
from source.module import Manager
from source.module import logging
from source.module import retry as re_download

__all__ = ['Download']


class Download:

    def __init__(self, manager: Manager):
        self.manager = manager
        self.folder = manager.folder
        self.temp = manager.temp
        self.proxy = manager.proxy
        self.chunk = manager.chunk
        self.session = manager.download_session
        self.retry = manager.retry
        self.prompt = manager.prompt
        self.folder_mode = manager.folder_mode
        self.video_format = "mp4"
        self.image_format = manager.image_format

    async def run(self, urls: list, name: str, type_: str, log, bar) -> Path:
        path = self.__generate_path(name)
        match type_:
            case "视频":
                await self.__download(urls[0], path, f"{name}", self.video_format, log, bar)
            case "图文":
                for index, url in enumerate(urls, start=1):
                    await self.__download(url, path, f"{name}_{index}", self.image_format, log, bar)
            case _:
                raise ValueError
        return path

    def __generate_path(self, name: str):
        """
        生成下载文件的路径，创建文件夹并返回path对象
        @param name:
        @return: path
        """
        path = self.manager.archive(self.folder, name, self.folder_mode)
        path.mkdir(exist_ok=True)
        return path

    @re_download
    async def __download(self, url: str, path: Path, name: str, format_: str, log, bar):
        """
        下载核心方法，异步下载文件，并根据文件Content-Type生成的后缀，最后将下载的文件移动到目标路径
        @param url:
        @param path:
        @param name:
        @param format_:
        @param log:
        @param bar:
        @return:
        """
        try:
            async with self.session.get(url, proxy=self.proxy) as response:
                suffix = self.__extract_type(
                    response.headers.get("Content-Type", "")) or format_
                temp = self.temp.joinpath(name)
                file = path.joinpath(name).with_suffix(f".{suffix}")
                if self.manager.is_exists(file):
                    logging(log, self.prompt.skip_download(name))
                    return True
                with temp.open("wb") as f:
                    async for chunk in response.content.iter_chunked(self.chunk):
                        f.write(chunk)
            self.manager.move(temp, file)
            logging(log, self.prompt.download_success(name))
            return True
        # 异常处理
        except ClientError as error:
            # 如果出现ClientError的错误，会临时删除文件，并记录错误记录
            self.manager.delete(temp)
            logging(log, error, ERROR)
            logging(log, self.prompt.download_error(name), ERROR)
            return False

    @staticmethod
    def __extract_type(content: str) -> str:
        """
        从 HTTP 头部的 Content-Type 中提取文件类型，如果无法提取，则返回空字符串
        @param content:
        @return:
        """
        return "" if content == "application/octet-stream" else content.split("/")[-1]
