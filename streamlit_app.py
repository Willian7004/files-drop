import os
import shutil
import streamlit as st
from pathlib import Path

# 创建保存文件的目录
UPLOAD_DIR = Path("files")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_uploaded_file(uploaded_file, prefix=None):
    """保存上传的文件"""
    if prefix:
        filename = f"{prefix}----{uploaded_file.name}"
    else:
        filename = uploaded_file.name
        
    target_path = UPLOAD_DIR / filename
    
    # 删除已存在的同名文件
    if target_path.exists():
        target_path.unlink()
    
    # 保存文件
    with open(target_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filename

def display_file(filepath, show_preview=True):
    """显示文件预览"""
    file_size = os.path.getsize(filepath)
    
    try:
        if filepath.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            st.image(str(filepath))
        elif filepath.suffix.lower() in ['.mp4', '.avi', '.mov']:
            st.video(str(filepath))
        elif file_size > 10 * 1024 * 1024:  # 超过10MB的非媒体文件
            st.warning("文件过大，无法预览")
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            st.text(content)
    except Exception as e:
        st.error(f"预览失败: {str(e)}")

def main():
    st.title("Files Drop")
    #项目说明
    with st.expander("项目说明"):
        st.write("本项目用于临时保存和预览文件，可以通过文件名前缀实现对私有文件的管理。")
        st.write("在Streamlit Cloud使用时，由于重启后不会保留文件，应当尽快取回文件，有条件时优先本地部署。")
    # 第一行布局
    col1, col2, col3 = st.columns([2, 2, 4])
    with col1:
        uploaded_file = st.file_uploader("选择文件", label_visibility="collapsed")
    with col2:
        private_switch = st.toggle("上传私有文件", value=False)
    with col3:
        if private_switch:
            prefix_input = st.text_input("私有文件前缀", placeholder="输入前缀")

    st.divider()

    # 处理文件上传
    if uploaded_file is not None:
        prefix = prefix_input if private_switch else None
        save_uploaded_file(uploaded_file, prefix)
        st.success("文件上传成功！")

    # 获取文件列表
    all_files = list(UPLOAD_DIR.glob("*"))
    
    # 过滤文件列表
    if private_switch and prefix_input:
        # 显示带指定前缀的私有文件
        filtered_files = [
            f for f in all_files
            if f.name.startswith(f"{prefix_input}----")
        ]
    else:
        # 显示公共文件（不包含----分隔符）
        filtered_files = [f for f in all_files if "----" not in f.name]

    # 显示文件列表
    for filepath in filtered_files:
        cols = st.columns([1, 1, 8])
        original_name = filepath.name.split("----")[-1] if "----" in filepath.name else filepath.name
        
        # 下载按钮
        with cols[0]:
            with open(filepath, "rb") as f:
                st.download_button(
                    "下载",
                    data=f,
                    file_name=original_name,
                    key=f"dl_{filepath.name}"
                )
        
        # 预览按钮
        with cols[1]:
            file_size = os.path.getsize(filepath)
            is_media = filepath.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov']
            if is_media or file_size <= 10 * 1024 * 1024:
                if st.button("预览", key=f"pv_{filepath.name}"):
                    st.session_state['preview_file'] = filepath
        
        # 显示文件名
        with cols[2]:
            st.write(original_name)
        
        # 分隔线
        st.divider()

    # 显示预览内容
    if 'preview_file' in st.session_state:
        st.subheader("文件预览")
        display_file(st.session_state['preview_file'])

if __name__ == "__main__":
    main()
