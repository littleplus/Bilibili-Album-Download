# Bilibili相簿下载(Bilibili Album Download)

## 中文介绍

### 快速食用

- 下载 `bilibili_album.py` 到任意一个文件夹
    `python bilibili_album.py <bilibili user id>`

### 注意事项

- 默认下载文件夹为，与脚本同级目录下，以Bilibili用户ID命名的文件夹
- 默认文件命名为，'绘画作品ID' + '_b' + '序号'.'图片格式'
- 目前脚本为单线程下载方式，单个用户图片数量多的话，需要时间可能有点长
- 本脚本大概率不会再修改，如果有运行问题，可以提issues。但不保证会改

## English Version

### Quick Start

- Download `bilibili_album.py` to any directory
    `python bilibili_album.py <bilibili user id>`

### Attentions

- The default download folder is a folder named after the Bilibili user ID at the same level as the script
- The default file name is, 'Album ID' + '_b' + 'index'.'Image format'
- Currently, the script is a single-threaded download method; if the number of images for a single user is large, it may take quite a long time.
- This script will probably not be modified again; if there are running errors, you can raise issues, but there is no guarantee to change.
