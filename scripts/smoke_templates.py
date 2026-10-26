#!/usr/bin/env python3
"""实际编译原创中文样例并导出逐页 PNG；视觉检查需要另行完成。"""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run(command, directory, log_name):
    result = subprocess.run(command, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    (directory / log_name).write_bytes(result.stdout)
    if result.returncode:
        raise RuntimeError(f'{command[0]} 失败，见 {directory / log_name}')
    return result.stdout.decode('utf-8', errors='replace')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'build' / 'smoke')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    reports = []
    for kind, cap in [('paper', 'Paper'), ('book', 'Book')]:
        directory = output / kind
        if directory.exists():
            raise FileExistsError(f'输出已存在，使用新的 --output: {directory}')
        directory.mkdir()
        assets = ROOT / 'skills' / f'elegant{kind}-master' / 'assets' / f'Elegant{cap}-master'
        shutil.copyfile(assets / f'elegant{kind}.cls', directory / f'elegant{kind}.cls')
        preamble = '\\PassOptionsToPackage{fontset=fandol}{ctex}\n'
        preamble += f'\\documentclass[lang=cn,newtx]{{elegant{kind}}}\n'
        preamble += '\\title{中文公式与引用检查}\\author{模板测试}\\date{}\n'
        if kind == 'book':
            shutil.copytree(assets / 'figure', directory / 'figure')
            preamble += '\\logo{logo-blue.png}\\cover{cover.jpg}\n'
        body = r'''
\addbibresource{reference.bib}
\begin{document}
\maketitle
'''
        if kind == 'book':
            body += '\\frontmatter\\tableofcontents\\mainmatter\\chapter{模型检查}\n'
        body += r'''
\section{中文排版}
本文件是原创测试样例。设 $x_0>0$，考虑离散迭代：
\begin{equation}\label{eq:test}
x_{n+1}=\frac{2x_n}{1+x_n},\qquad n=0,1,2,\ldots .
\end{equation}
式~\eqref{eq:test} 用于检查上下标、分式和交叉引用。
参考文献测试见~\cite{smoke}。
\begin{table}[htbp]\centering
\caption{原创测试表}\begin{tabular}{cc}\hline
变量 & 初值\\\hline $x_0$ & $1$\\\hline
\end{tabular}\end{table}
\printbibliography
\end{document}
'''
        (directory / 'smoke.tex').write_text(preamble + body, encoding='utf-8')
        (directory / 'reference.bib').write_text('@misc{smoke, author={Template Test}, title={Original smoke fixture}, year={2026}}\n', encoding='utf-8')
        for index, engine in enumerate(['xelatex', 'biber', 'xelatex', 'xelatex']):
            command = [engine, 'smoke'] if engine == 'biber' else [engine, '-interaction=nonstopmode', '-halt-on-error', 'smoke.tex']
            run(command, directory, f'pass-{index + 1}.txt')
        log = (directory / 'smoke.log').read_text(encoding='utf-8', errors='replace')
        for error in ['Missing character:', 'undefined references', 'Citation \'smoke\' on page', 'Overfull \\hbox', 'Overfull \\vbox']:
            if error in log:
                raise RuntimeError(f'{kind}: 编译日志需要检查: {error}')
        run(['pdftotext', '-layout', 'smoke.pdf', 'smoke.txt'], directory, 'extract.txt')
        text = (directory / 'smoke.txt').read_text(encoding='utf-8')
        assert '中文' in text and 'Original smoke fixture' in text, kind
        info = run(['pdfinfo', 'smoke.pdf'], directory, 'pdfinfo.txt')
        pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
        run(['pdftoppm', '-png', '-r', '100', 'smoke.pdf', 'page'], directory, 'render.txt')
        reports.append({'template': kind, 'pages': pages, 'build_pass': True, 'text_pass': True, 'visual_qa': 'pending'})
    (output / 'results.json').write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(reports, ensure_ascii=False))


if __name__ == '__main__':
    main()
