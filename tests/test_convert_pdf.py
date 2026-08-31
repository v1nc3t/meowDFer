from PIL import Image

from meowdfer.commands.convert import convert_pdf


class FakeConsole:
    def __init__(self):
        self.lines: list[str] = []

    def print(self, *args, **kwargs):
        self.lines.append(str(args[0]) if args else "")


def _chapter_folder(root, name: str) -> None:
    folder = root / name
    folder.mkdir()
    Image.new("RGB", (2, 2), color="white").save(folder / "001.jpg")


def test_convert_skips_unsortable_folder_when_skip_enabled(tmp_path):
    src = tmp_path / "src"
    dest = tmp_path / "dest"
    src.mkdir()
    dest.mkdir()
    _chapter_folder(src, "c001")
    (src / "not_a_chapter").mkdir()

    console = FakeConsole()
    ok = convert_pdf.convert(str(src), str(dest), "Gyo", "chapter", True, console)

    assert ok
    assert (dest / "Gyo Chapter 1.pdf").exists()
    assert any("Skipped: not_a_chapter" in line for line in console.lines)


def test_convert_aborts_on_unsortable_folder_without_skip(tmp_path):
    src = tmp_path / "src"
    dest = tmp_path / "dest"
    src.mkdir()
    dest.mkdir()
    _chapter_folder(src, "c001")
    (src / "not_a_chapter").mkdir()

    console = FakeConsole()
    ok = convert_pdf.convert(str(src), str(dest), "Gyo", "chapter", False, console)

    assert not ok
    assert not (dest / "Gyo Chapter 1.pdf").exists()
    assert any("Sorting Error" in line and "not_a_chapter" in line for line in console.lines)


def test_convert_processes_decimal_chapter(tmp_path):
    src = tmp_path / "src"
    dest = tmp_path / "dest"
    src.mkdir()
    dest.mkdir()
    _chapter_folder(src, "c010.5")

    console = FakeConsole()
    ok = convert_pdf.convert(str(src), str(dest), "Gyo", "chapter", False, console)

    assert ok
    assert (dest / "Gyo Chapter 10.5.pdf").exists()
