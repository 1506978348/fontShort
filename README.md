### 字体瘦身
* 配置信息(config.json)
```json
{	
	// 文本内容(可能为多语言表导出的内容)
    "txtFile": "gameText.txt",
    // 字体文件
    "fontFile": "江城圆体 600w_1.ttf",
    // 默认文字(英文字符，阿拉伯数字等)
    "defaultText": "",
    // 导出的相对路径
    "exportPath": "../client/assets/Bundles/Game/font/",
    // 裁剪后导出的字体名称
    "exportName": "font.ttf"
}
```
* 文本内容(gameText.txt)
	文件内为游戏中使用到的文字，多语言项目为多语言表导出文件。
* 脚本(fontShort.py)
	注释较全面，可自行理解。如有不解，请搭配AI。
```python
import re
import json
from fontTools.ttLib import TTFont
from fontTools import subset

    

config = 'config.json' # 配置文件路径

# config配置
textFile = ''
fontFile = ''
defaultText = ''
exportPath = ''
exportName = ''

# 文本内容
gameText = ''


# 加载config文件
def _loadConfig():
    with open(config, 'r', encoding='utf-8') as file:
        content = file.read()
        jsonObj = json.loads(content)
        global textFile
        global fontFile
        global defaultText
        global exportPath
        global exportName

        textFile = jsonObj['txtFile']
        fontFile = jsonObj['fontFile']
        defaultText = jsonObj['defaultText']
        exportPath = jsonObj['exportPath']
        exportName = jsonObj['exportName']

# 加载TXT文件
def _loadText():
    with open(textFile, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
    return content


# 去重
def _removeDuplicates(s):
    return ''.join(set(s))


# 检查字体文件中缺失的字
def _checkFontExits(str):
    noneStr = ""
    
    font = TTFont(fontFile)
    glyf = font["glyf"]

    for i in str:
        code = i.encode("unicode-escape").decode()
        if "\\u" in code:
            code = "uni" + code[2:].upper()
        if not glyf.has_key(code):
            dd = re.findall('[\u4e00-\u9fa5]', i)
            if(len(dd) > 0):
                noneStr += dd[0]
    if(noneStr == ""):
        return
    print("<---------------------------------------->")
    print("当前字体中缺失字: " + noneStr)
    print("<---------------------------------------->")

# 导出字体ttf
def _exportFont(textStr):
    font = subset.load_font(fontFile, subset.Options())
    exportFile = exportPath + exportName
    
    subsetter = subset.Subsetter()
    subsetter.populate(text = textStr)
    subsetter.subset(font)

    # 生成输出文件
    subset.save_font(font, exportFile, subset.Options())

    font.close()
    print("输出字体文件成功: " + exportFile)


def _main():
    _loadConfig()
    originText = defaultText + _loadText().replace('\n', '')
    print("去重前: ", originText)
    print("<-------------------->")
    gameText = _removeDuplicates(originText)
    print("去重后: ", gameText)

    _exportFont(gameText)

    _checkFontExits(gameText)

    print("subset done!")
    print("输入回车键继续")
    input()

_main()
```
* 文件结构
	![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/dcb9ad9323084cacbe140c153e5709d7.png)
* 脚本执行
	可以看出当前字体内还缺失文字
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9e507454c06d4ed89f7affced9b41f90.png)