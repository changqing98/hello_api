from langchain_text_splitters import MarkdownHeaderTextSplitter

from infra.document_loader import markdown

if __name__ == "__main__":
    # 使用递归字符文本分割器
    text_splitter = MarkdownHeaderTextSplitter()
    markdown_pages = markdown.load_markdown_pages()
    text_splitter.split_text(markdown_pages.page_content[0:10000])

