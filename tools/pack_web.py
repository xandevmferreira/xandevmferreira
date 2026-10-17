#!/usr/bin/env python3
"""Junta a exportação web num único Jogar.html que abre com dois cliques."""

from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOGAR = ROOT / "jogar"
OUT = ROOT / "Jogar.html"

FILES = (
    ("Jogar.wasm", "application/wasm"),
    ("Jogar.pck", "application/octet-stream"),
    ("Jogar.audio.worklet.js", "text/javascript"),
    ("Jogar.audio.position.worklet.js", "text/javascript"),
)


def patch_engine(source: str) -> str:
    locate = """\t\t\t'locateFile': function (path) {
\t\t\t\tif (!path.startsWith('godot.')) {
\t\t\t\t\treturn path;
\t\t\t\t} else if (path.endsWith('.audio.worklet.js')) {
\t\t\t\t\treturn `${loadPath}.audio.worklet.js`;
\t\t\t\t} else if (path.endsWith('.audio.position.worklet.js')) {
\t\t\t\t\treturn `${loadPath}.audio.position.worklet.js`;
"""
    locate_new = """\t\t\t'locateFile': function (path) {
\t\t\t\tfunction jogar(name) {
\t\t\t\t\tconst files = globalThis.JOGAR_FILES;
\t\t\t\t\treturn files && files[name] ? files[name] : name;
\t\t\t\t}
\t\t\t\tif (!path.startsWith('godot.')) {
\t\t\t\t\treturn jogar(path);
\t\t\t\t} else if (path.endsWith('.audio.worklet.js')) {
\t\t\t\t\treturn jogar(`${loadPath}.audio.worklet.js`);
\t\t\t\t} else if (path.endsWith('.audio.position.worklet.js')) {
\t\t\t\t\treturn jogar(`${loadPath}.audio.position.worklet.js`);
"""
    wasm = """\t\t\t\tif (typeof (WebAssembly.instantiateStreaming) !== 'undefined') {
\t\t\t\t\tWebAssembly.instantiateStreaming(Promise.resolve(r), imports).then(done);
\t\t\t\t} else {
\t\t\t\t\tr.arrayBuffer().then(function (buffer) {
\t\t\t\t\t\tWebAssembly.instantiate(buffer, imports).then(done);
\t\t\t\t\t});
\t\t\t\t}
"""
    wasm_new = """\t\t\t\tconst wasmResponse = r;
\t\t\t\tfunction instantiateBuffer() {
\t\t\t\t\twasmResponse.arrayBuffer().then(function (buffer) {
\t\t\t\t\t\tWebAssembly.instantiate(buffer, imports).then(done);
\t\t\t\t\t});
\t\t\t\t}
\t\t\t\tif (typeof (WebAssembly.instantiateStreaming) !== 'undefined') {
\t\t\t\t\tWebAssembly.instantiateStreaming(Promise.resolve(wasmResponse), imports).then(done).catch(instantiateBuffer);
\t\t\t\t} else {
\t\t\t\t\tinstantiateBuffer();
\t\t\t\t}
"""
    if locate not in source or wasm not in source:
        raise SystemExit("não achei o trecho do motor para embutir os arquivos")
    return source.replace(locate, locate_new, 1).replace(wasm, wasm_new, 1)


def main() -> None:
    html = (JOGAR / "Jogar.html").read_text(encoding="utf-8")
    html = html.replace('src="Jogar.png"', 'src=""')
    html = html.replace('<script src="Jogar.js"></script>', "<!-- engine -->")
    start = "\t\tsetStatusMode('progress');\n\t\tengine.startGame({"
    start_new = "\t\tsetStatusMode('progress');\n\t\tjogarPrep().then(function () {\n\t\tengine.startGame({"
    end = """\t\t}).then(() => {
\t\t\tsetStatusMode('hidden');
\t\t}, displayFailureNotice);
\t}"""
    end_new = """\t\t}).then(() => {
\t\t\tsetStatusMode('hidden');
\t\t}, displayFailureNotice);
\t\t}).catch(displayFailureNotice);
\t}"""
    if start not in html or end not in html:
        raise SystemExit("não achei o arranque da página")
    html = html.replace(start, start_new, 1).replace(end, end_new, 1)
    marker = "<!-- engine -->"
    head, tail = html.split(marker, 1)
    engine = patch_engine((JOGAR / "Jogar.js").read_text(encoding="utf-8"))

    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(head)
        handle.write("<script>\n")
        handle.write("function jogarPrep() {\n")
        handle.write("\tconst jobs = jogarPrep.files;\n")
        handle.write("\tglobalThis.JOGAR_FILES = {};\n")
        handle.write("\tfor (let index = 0; index < jobs.length; index++) {\n")
        handle.write("\t\tconst name = jobs[index][0];\n")
        handle.write("\t\tconst type = jobs[index][1];\n")
        handle.write("\t\tconst bin = atob(jobs[index][2]);\n")
        handle.write("\t\tconst bytes = new Uint8Array(bin.length);\n")
        handle.write("\t\tfor (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);\n")
        handle.write("\t\tglobalThis.JOGAR_FILES[name] = URL.createObjectURL(new Blob([bytes], { type: type }));\n")
        handle.write("\t}\n")
        handle.write("\tconst orig = window.fetch.bind(window);\n")
        handle.write("\twindow.fetch = function (input, init) {\n")
        handle.write("\t\tconst url = typeof input === 'string' ? input : (input && input.url) || '';\n")
        handle.write("\t\tfor (const name in globalThis.JOGAR_FILES) {\n")
        handle.write("\t\t\tif (url === name || url.endsWith('/' + name)) return orig(globalThis.JOGAR_FILES[name], init);\n")
        handle.write("\t\t}\n")
        handle.write("\t\treturn orig(input, init);\n")
        handle.write("\t};\n")
        handle.write("\treturn Promise.resolve();\n")
        handle.write("}\n")
        handle.write("jogarPrep.files = [];\n")
        for name, mime in FILES:
            raw = (JOGAR / name).read_bytes()
            encoded = base64.b64encode(raw).decode("ascii")
            handle.write(f'jogarPrep.files.push(["{name}","{mime}","')
            handle.write(encoded)
            handle.write('"]);\n')
            print(name, len(raw))
        handle.write("</script>\n<script>\n")
        handle.write(engine)
        handle.write("\n</script>\n")
        handle.write(tail)
    print("escreveu", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
