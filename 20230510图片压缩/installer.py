import PyInstaller.__main__

# add wechat.jpg to the exe file
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--icon=static/logo.ico',
    '--add-data=static/wechat.jpg;.',
    '--name=图片压缩工具'
])
