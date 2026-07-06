import sys
from pathlib import Path

from langchain_community.document_loaders import UnstructuredMarkdownLoader


def _prepare_runtime_for_standalone_execution() -> None:
    """避免当前文件名 markdown.py 遮蔽第三方 markdown 包。"""
    current_dir = Path(__file__).resolve().parent
    if sys.path and Path(sys.path[0]).resolve() == current_dir:
        sys.path.pop(0)


def load_markdown_pages():
    _prepare_runtime_for_standalone_execution()
    project_root = Path(__file__).resolve().parents[2]
    markdown_file = project_root / "resource/1. 简介 Introduction.md"
    loader = UnstructuredMarkdownLoader(str(markdown_file))
    return loader.load()


if __name__ == "__main__":
    md_pages = load_markdown_pages()
    print(f"载入后的变量类型为：{type(md_pages)}，", f"该 Markdown 一共包含 {len(md_pages)} 页")
    md_page = md_pages[0]
    print(
        f"每一个元素的类型：{type(md_page)}.",
        f"该文档的描述性数据：{md_page.metadata}",
        f"查看该文档的内容:\n{md_page.page_content[:200]}",
        sep="\n------\n",
    )
