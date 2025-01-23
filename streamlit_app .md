### 提示词：

使用streamlit写一个程序，实现以下功能：

1.在第一行创建上传按钮和开关，开关上的文字为“上传私有文件”，默认关闭。打开开关时在开关右边显示输入框。

2.点击上传按钮时上传文件并保存到当前目录下的files文件夹，与之前上传的文件的文件名重复时替换文件。如果打开第1步创建的开关则在文件名开头加上输入框中的文字和“----”符号。

3.第1步创建的开关关闭时，显示所有文件名中未匹配到“----”的文件的文件名，在每一行左边创建一个下载按钮和预览按钮，每一行下面创建分隔符。点击下载按钮时下载相应文件，点击预览按钮时在页面底部显示文件（图片、视频文件以相应形式显示，其它以文本形式显示，对图片、视频以外且大于10mb的文件隐藏预览按钮）。第1步创建的开关打开时，显示所有文件名中匹配到“----”并且文件名中“----”前的内容与当前输入框中的文字相同的文件的文件名。下载文件时移除文件名中的“----”和前面的内容。

### 思维链：

好的，我现在需要帮用户解决一个使用Streamlit实现文件上传和管理的问题。首先，我要仔细阅读用户的需求，确保理解每个功能点。

用户的需求分为三个主要部分：

1. **第一行要有上传按钮和开关**：开关默认关闭，打开时右边显示输入框。开关上的文字是“上传私有文件”。这里需要注意的是，开关和上传按钮应该在同一行，可能需要使用Streamlit的列布局功能，比如columns来排列。

2. **上传文件时的处理**：

- 保存到当前目录下的files文件夹，如果文件名重复则替换。

- 如果开关打开，需要在文件名开头加上输入框中的文字和“----”。这里需要处理文件名拼接，并确保文件保存正确。同时，要处理文件名的重复替换逻辑，可能需要检查目标路径是否存在，存在的话就删除旧文件再保存新文件。

3. **显示文件列表并根据开关状态过滤**：

- 当开关关闭时，显示所有不包含“----”的文件，每行有下载和预览按钮，下方有分隔符。预览按钮需要根据文件类型和大小决定是否显示，比如图片和视频直接显示，其他文本文件显示内容，超过10MB的非图片视频文件隐藏预览按钮。

- 当开关打开时，显示文件名中包含“----”且前面部分与输入框内容相同的文件。下载时要去除前缀和“----”。

接下来，我需要考虑如何组织代码结构，以及使用哪些Streamlit组件。

首先，处理文件上传部分。上传按钮使用st.file_uploader，开关使用st.toggle。当开关打开时，显示输入框st.text_input。这里可能需要将开关和输入框放在同一行的不同列中，使用st.columns布局。

然后，处理文件保存逻辑。上传文件后，获取文件名，根据开关状态决定是否添加前缀。保存前检查files目录是否存在，不存在则创建。重复文件名时替换，可以用os.path.exists检查，存在的话先删除再保存。

对于文件列表的显示，需要遍历files目录中的文件，根据开关状态过滤。当开关关闭时，过滤出不含“----”的文件；当打开时，过滤出包含“----”且前缀匹配的文件。每个文件条目需要生成下载和预览按钮，下载时去除前缀，这可以通过字符串分割处理。

预览部分需要判断文件类型，可以使用mimetype或文件扩展名。图片（如jpg、png）、视频（如mp4、mov）用相应的st.image或st.video显示。文本文件用st.text显示内容。对于大文件（超过10MB的非媒体文件），隐藏预览按钮，这需要在生成按钮前检查文件大小和类型。

另外，下载按钮需要生成一个下载链接，Streamlit的st.download_button可以直接使用，但需要读取文件内容作为字节流。注意下载时的文件名处理，去除前缀和“----”。

关于布局，每个文件条目可能需要使用列来排列按钮，然后添加分隔符。使用st.columns将下载按钮、预览按钮和文件名放在同一行，下方用st.divider()添加分隔线。

潜在的问题点：

- 文件保存路径的处理，确保files目录存在。

- 文件名重复时的替换逻辑，可能需要先删除旧文件。

- 文件类型和大小的判断，特别是大文件的预览按钮隐藏。

- 动态显示不同的文件列表，根据开关状态和输入框内容过滤。

- 下载时文件名的修改，需要正确分割字符串并重组。

测试案例：

1. 开关关闭时上传文件，不添加前缀，确保保存在files目录，且列表显示正确。

2. 开关打开时输入前缀，上传文件，检查文件名是否正确添加前缀。

3. 上传同名文件，确认是否替换。

4. 测试不同文件类型的预览：图片、视频、文本，以及大文件是否隐藏预览按钮。

5. 切换开关状态，检查列表过滤是否正确。

6. 下载文件时，检查文件名是否去除了前缀。

可能需要使用os模块处理路径，glob模块遍历文件，shutil处理文件保存。对于大文件读取，需要注意内存使用，分块读取可能更安全，但Streamlit的下载按钮可能需要整个文件内容，所以需要权衡。

最后，代码结构大致分为：

- 创建files目录。

- 处理上传逻辑。

- 根据开关状态过滤文件列表。

- 显示每个文件条目，包括按钮和预览处理。

### 回答正文：

以下是实现所需功能的Streamlit代码：

```python
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
    st.title("文件管理应用")

    # 第一行布局
    col1, col2, col3 = st.columns([2, 2, 4])
    with col1:
        uploaded_file = st.file_uploader("选择文件", label_visibility="collapsed")
    with col2:
        private_switch = st.toggle("上传私有文件", value=False)
    with col3:
        if private_switch:
            prefix_input = st.text_input("私有文件前缀", placeholder="输入前缀")

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
```

功能说明：

1. **文件上传**：
   - 支持拖放和选择文件上传
   - 私有文件模式会添加前缀并使用特殊分隔符保存
   - 自动覆盖同名文件

2. **文件管理**：
   - 公共文件（无分隔符）和私有文件分开显示
   - 下载时自动去除前缀和分隔符
   - 实时刷新文件列表

3. **预览功能**：
   - 支持图片、视频预览
   - 支持文本文件预览（10MB以下）
   - 大文件自动隐藏预览按钮

4. **界面特性**：
   - 响应式布局
   - 清晰的分隔线
   - 友好的状态提示

使用方法：
1. 安装依赖：`pip install streamlit`
2. 保存代码为`app.py`
3. 运行：`streamlit run app.py`

注意：
- 文件实际保存在程序运行目录下的`files`文件夹
- 私有文件前缀输入支持任何合法字符
- 系统会自动处理文件名冲突
- 预览功能受浏览器和文件类型限制



