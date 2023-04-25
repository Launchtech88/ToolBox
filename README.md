# Pycharm配置Qt Designer
1. 下载并安装 Qt Designer <https://build-system.fman.io/qt-designer-download>
2. Pycharm中依次点击File->Settings->Tools->External Tools 点击+号
```
Name: Qt Designer
Description: Qt Designer
Program: D:\QtDesigner\designer.exe
Arguments: 
Working directory: $FileDir$
```
3. 设置Qt Editor(用来直接对已创建的ui文件进行编辑)
```
Name: Qt Editor
Description: Qt Editor
Program: D:\QtDesigner\designer.exe
Arguments: $FileName$
Working directory: $FileDir$
```
4. 配置pyuic5(用来把ui文件转化为py文件)
```
Name: PyUIC5
Description: PyUIC5
Program: E:\Venv\ImageCompression\Scripts\pyuic5.exe
Arguments: $FileName$ -o $FileNameWithoutExtension$.py
Working directory: $FileDir$
```

