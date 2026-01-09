"""Console script for grepcoll."""

import subprocess
import tempfile
import urllib.parse
from pathlib import Path
from typing import Annotated

import typer
from recoll import recoll
from rich.console import Console

app = typer.Typer()
console = Console()


class TerminalHighlighter:
    def startMatch(self, _):
        return "[bold red]"

    def endMatch(self):
        return "[/]"


terminalHighlighterInstance = TerminalHighlighter()


@app.command()
def main(
    pattern: Annotated[str, typer.Argument()],
    path: Annotated[
        Path,
        typer.Argument(exists=True, file_okay=False, readable=True, resolve_path=True),
    ] = Path("."),
):
    """GrepColl: grep, but with recoll underneath, useful to search with stemming and lemmatization."""
    with tempfile.TemporaryDirectory(prefix="grepcoll-") as index_dir_str:
        index_dir = Path(index_dir_str)
        # 1. Create config
        conf_file_path = index_dir / "recoll.conf"

        config = f"""
topdirs = {path}
indexstemminglanguages = russian english
noaspell = true
loglevel=1
pyloglevel=1"""
        with open(conf_file_path, "w") as f:
            f.write(config)

        # 2. Index
        # Really weird thing, but there's no API to start recollindex.
        cmd = ["recollindex", "-c", str(index_dir)]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 3. Find and print documents
        db = recoll.connect(confdir=index_dir_str)

        db.setAbstractParams(contextwords=4)
        query = db.query()

        query.execute(pattern, stemlang="russian english")

        for doc in query:
            url = doc.get("url")
            doc_path_str = urllib.parse.unquote(url).replace("file://", "")
            doc_path = Path(doc_path_str)

            snippet = query.makedocabstract(doc, methods=terminalHighlighterInstance)

            print(type(snippet))

            if not snippet:
                snippet = "(Найдено в имени файла или метаданных)"

            console.print(doc_path)
            console.print(snippet)
            console.print()


if __name__ == "__main__":
    app()
