#!/usr/bin/env python3
"""Reaplica os ajustes da página jogável depois de cada exportação web."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOGAR = ROOT / "jogar"

LOAD_OLD = """\tfunction loadFetch(file, tracker, fileSize, raw) {
\t\ttracker[file] = {"""

LOAD_NEW = """\tfunction loadFetch(file, tracker, fileSize, raw) {
\t\tif (typeof file === 'string' && !/^[a-z]+:/i.test(file)) {
\t\t\ttry {
\t\t\t\tfile = new URL(file, document.baseURI).href;
\t\t\t} catch (e) {}
\t\t}
\t\ttracker[file] = {"""

WASM_OLD = """\t\t\t\tif (typeof (WebAssembly.instantiateStreaming) !== 'undefined') {
\t\t\t\t\tWebAssembly.instantiateStreaming(Promise.resolve(r), imports).then(done);
\t\t\t\t} else {
\t\t\t\t\tr.arrayBuffer().then(function (buffer) {
\t\t\t\t\t\tWebAssembly.instantiate(buffer, imports).then(done);
\t\t\t\t\t});
\t\t\t\t}"""

WASM_NEW = """\t\t\t\tconst wasmResponse = r;
\t\t\t\tfunction instantiateBuffer() {
\t\t\t\t\twasmResponse.arrayBuffer().then(function (buffer) {
\t\t\t\t\t\tWebAssembly.instantiate(buffer, imports).then(done);
\t\t\t\t\t});
\t\t\t\t}
\t\t\t\tif (typeof (WebAssembly.instantiateStreaming) !== 'undefined') {
\t\t\t\t\tWebAssembly.instantiateStreaming(Promise.resolve(wasmResponse), imports).then(done).catch(instantiateBuffer);
\t\t\t\t} else {
\t\t\t\t\tinstantiateBuffer();
\t\t\t\t}"""

STATUS_OLD = """#status {
	background-color: #3a242c;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	visibility: hidden;
}"""

STATUS_NEW = """#status {
	background-color: #3a242c;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	visibility: visible;
}"""

EXTRA_CSS = """<style>
#espera {
	color: #fff6ea;
	font-family: 'Noto Sans', 'Droid Sans', Arial, sans-serif;
	font-size: 1.05rem;
	line-height: 1.45;
	margin: 1rem 1.4rem 0;
	max-width: 24rem;
	text-align: center;
}
#status-progress {
	height: 1rem;
	accent-color: #fff6ea;
}
</style>
"""

ESPERA = (
    '<div id="status-notice"></div>\n'
    '\t\t\t<p id="espera"><b>Aniversário</b><br>'
    "A primeira vez demora um pouco.<br>Pode esperar. O jogo é grande.</p>"
)

MODE_OLD = """\t\tstatusProgress.style.display = mode === 'progress' ? 'block' : 'none';
\t\tstatusNotice.style.display = mode === 'notice' ? 'block' : 'none';"""

MODE_NEW = """\t\tstatusProgress.style.display = mode === 'progress' ? 'block' : 'none';
\t\tstatusNotice.style.display = mode === 'notice' ? 'block' : 'none';
\t\tconst espera = document.getElementById('espera');
\t\tif (espera) {
\t\t\tespera.style.display = mode === 'progress' ? 'block' : 'none';
\t\t}"""

GATE_OLD = "\tif (missing.length !== 0) {"

GATE_NEW = """\tif (/WhatsApp|Instagram|FBAN|FBAV|FB_IAB|Line\\//i.test(navigator.userAgent || '')) {
\t\tsetStatusNotice('Para jogar, abre no Chrome.\\n\\nNo WhatsApp: toca nos três pontinhos e escolhe Abrir no navegador.');
\t\tsetStatusMode('notice');
\t\tinitializing = false;
\t} else if (missing.length !== 0) {"""


def patch_engine(source: str) -> str:
    if "document.baseURI" not in source:
        if LOAD_OLD not in source:
            raise SystemExit("não achei o loadFetch para corrigir o endereço")
        source = source.replace(LOAD_OLD, LOAD_NEW, 1)
    if "function instantiateBuffer()" not in source:
        if WASM_OLD not in source:
            raise SystemExit("não achei o instantiateStreaming para corrigir o wasm")
        source = source.replace(WASM_OLD, WASM_NEW, 1)
    if "Promise.resolve(r)" in source:
        raise SystemExit("o wasm ainda usa Promise.resolve(r)")
    return source


def patch_html(html: str) -> str:
    html = html.replace("<html lang=\"en\">", "<html lang=\"pt\">", 1)
    if STATUS_OLD not in html and "visibility: visible;" not in html:
        raise SystemExit("não achei o painel de carregamento")
    html = html.replace(STATUS_OLD, STATUS_NEW, 1)
    if 'id="espera"' not in html:
        if "</head>" not in html or '<div id="status-notice"></div>' not in html:
            raise SystemExit("não achei onde escrever a espera")
        html = html.replace("</head>", EXTRA_CSS + "</head>", 1)
        html = html.replace('<div id="status-notice"></div>', ESPERA, 1)
    if "espera.style.display" not in html:
        if MODE_OLD not in html:
            raise SystemExit("não achei o modo da tela de espera")
        html = html.replace(MODE_OLD, MODE_NEW, 1)
    if "Para jogar, abre no Chrome" not in html:
        if GATE_OLD not in html:
            raise SystemExit("não achei o teste do navegador")
        html = html.replace(GATE_OLD, GATE_NEW, 1)
    html = html.replace(
        "const missingMsg = 'Error\\nThe following features required to run Godot projects on the Web are missing:\\n';",
        "const missingMsg = 'Este navegador não abre o jogo.\\nAbre no Chrome ou no Edge.\\n';",
    )
    html = html.replace(
        "setStatusNotice('An unknown error occurred.');",
        "setStatusNotice('Não consegui abrir o jogo. Tenta no Chrome.');",
    )
    return html


def main() -> None:
    engine_path = JOGAR / "Jogar.js"
    engine_path.write_text(patch_engine(engine_path.read_text(encoding="utf-8")), encoding="utf-8")
    html_path = JOGAR / "Jogar.html"
    html = patch_html(html_path.read_text(encoding="utf-8"))
    html_path.write_text(html, encoding="utf-8")
    shutil.copyfile(html_path, JOGAR / "index.html")
    pck = (JOGAR / "Jogar.pck").stat().st_size
    wasm = (JOGAR / "Jogar.wasm").stat().st_size
    if f'"Jogar.pck":{pck}' not in html or f'"Jogar.wasm":{wasm}' not in html:
        raise SystemExit(f"tamanho divergente pck={pck} wasm={wasm}")
    print("página pronta", pck, wasm)


if __name__ == "__main__":
    main()
