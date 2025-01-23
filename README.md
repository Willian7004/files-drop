Files Drop

本项目使用Streamlit创建，用于临时保存和预览文件，可以通过文件名前缀实现对私有文件的管理。

本项目已部署到Streamlit Cloud，域名为https://william7004-files-drop.streamlit.app 。在Streamlit Cloud使用时，由于重启后不会保留文件，应当尽快取回文件，有条件时优先本地部署。

本地部署流程

建议使用Python=3.10环境

1.安装依赖
```bash
pip install -r requirements.txt
```
2.运行应用
```bash
streamlit run streamlit_app.py
```

