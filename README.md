# 半佛视频风格生成器

## 项目背景
半佛在2020年凭借众多沙雕表情包视频 + 魔性的文案迅速出圈。魔性的文案不能直接复制，但是沙雕表情包的视频可以直接生成。不妨做一个视频生成器，快快速生成此类视频风格的视频。简直自媒体的福音，抖音的狂欢。

### 思路：
1. 输入断句后的文案
2. 将文案根据短句分割，每句作为一条字幕
3. 根据字幕搜索表情包并选择设置
4. 利用语音合成手段合成配音
5. 重复3、4步骤，直到所有的字幕均完成表情包设定、字幕设定、配音设定
6. 合成视频并加入背景音乐
7. 导出成品

## 安装
1. 安装python3.8.3
2. 安装requirements.txt依赖
3. 运行`python main.py`

## 使用
1. 确定文件名，点击set按钮可以进行文案输入（输入完成暂不支持编辑）
2. 点击last和next可分别跳转到上一句以及下一句文案，预览区可预览字幕，搜索区可搜索相关图片/表情包
3. 所有字幕均设置完毕可进行genVideo。
4. 软件每5秒保存一次工程文件。崩溃时可重新拖放加载工程文件。工程文件位置：`material/{ProgectName}/*.bfs`
5. 工程所用到的素材默认会存放至`material/{ProgectName}/audio/`以及`material/{ProgectName}/img/`
6. 可将工程文件拖放入软件加载上一次的工程内容。需要注意的是加载工程要求素材文件夹必须存在！
7. 可将txt格式的文案拖入软件！
8. 可将表情包图片/gif文件拖入软件，用于设置当前字幕的表情包！

## TODO
- [ ] 优化gif显示
- [ ] 表情包尺寸的统一问题
- [x] 编辑保存防止异常退出工作丢失
- [ ] 支持修改文案
- [x] 文件名自定义
- [x] 使用的图片与未使用的图片缓存分开，依据文件名归档
- [x] 使用过的配音缓存分类归档

## Reference
[一键生成半佛仙人视频，表情包之王你也可以！](https://www.bilibili.com/video/BV1oz411e7Jk)

[MoviePy](https://zulko.github.io/moviepy/)

[斗图啦](https://www.doutula.com/article/list/)

[百度图片](https://image.baidu.com/)

[百度在线语音合成](https://cloud.baidu.com/product/speech/tts_online)
## License
[GNU General Public License v3.0](LICENSE)