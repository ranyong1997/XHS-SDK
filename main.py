from asyncio import run
from source import XHS

csv_file = None


async def main():
    """通过代码设置参数，适合二次开发"""
    # 示例链接
    link = ""
    link1 = ""
    link2 = ""
    link3 = ""
    link4 = ""
    multiple_links = f"{link} {link1} {link2} {link3} {link4}"
    # 实例对象
    work_path = "G:\\"  # 作品数据/文件保存根路径，默认值：项目根路径
    folder_name = "Download"  # 作品文件储存文件夹名称（自动创建），默认值：Download
    user_agent = ""  # 请求头 User-Agent
    cookie = ""  # 小红书网页版 Cookie，无需登录
    proxy = None  # 网络代理
    timeout = 5  # 请求数据超时限制，单位：秒，默认值：10
    chunk = 1024 * 1024 * 10  # 下载文件时，每次从服务器获取的数据块大小，单位：字节
    max_retry = 5  # 请求数据失败时，重试的最大次数，单位：秒，默认值：5
    record_data = True  # 是否记录作品数据至文件
    image_format = "PNG"  # 图文作品文件下载格式，支持：PNG、WEBP
    folder_mode = True  # 是否将每个作品的文件储存至单独的文件夹
    async with XHS() as xhs:
        pass  # 使用默认参数
    async with XHS(
            work_path=work_path,
            folder_name=folder_name,
            user_agent=user_agent,
            cookie=cookie,
            proxy=proxy,
            timeout=timeout,
            chunk=chunk,
            max_retry=max_retry,
            record_data=record_data,
            image_format=image_format,
            folder_mode=folder_mode,
    ) as xhs:  # 使用自定义参数
        download = True  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        print(await xhs.extract(link, download))  # 下载单个作品
        # print(await xhs.extract(multiple_links, download))  # 支持传入多个作品链接


if __name__ == '__main__':
    run(main())
