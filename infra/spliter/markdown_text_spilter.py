from langchain_text_splitters import MarkdownHeaderTextSplitter

if __name__ == "__main__":
    # 使用递归字符文本分割器
    text_splitter = MarkdownHeaderTextSplitter()
    text_splitter.split_text(pdf_page.page_content[0:1000])

