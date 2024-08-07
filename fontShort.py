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