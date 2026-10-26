---
name: elegantbook-master
description: Use this skill when the user wants a LaTeX book, textbook, monograph, course book, long-form lecture notes, thesis-like book manuscript, or converted Markdown/text content produced as a complete ElegantBook-style .tex project using the bundled ElegantBook LaTeX template.
---

# ElegantBook Master

## Purpose

Generate complete, compilable LaTeX book projects using the bundled ElegantBook template. Use this skill when the user asks for ElegantBook style, a LaTeX book template, textbooks, monographs, course books, long-form lecture notes, or conversion of Markdown/plain text into an ElegantBook `.tex` document.

The bundled template lives in `assets/ElegantBook-master/`. Copy the needed template files into the user's output folder before or while creating the book project:

- `elegantbook.cls`
- `reference.bib`
- Create `preface.tex` from the user's preface when a separate preface file is needed; the bundle contains no personal preface.
- `figure/` for cover and logo images
- `image/` when examples or content images are used
- `elegantbook-cn.tex` and `elegantbook-en.tex` only as examples/reference, not as files to overwrite user output

## Default Documents

For Chinese books, default to this document class unless the user specifies otherwise:

```tex
\documentclass[lang=cn,newtx,10pt,scheme=chinese]{elegantbook}
```

For English books, default to:

```tex
\documentclass[11pt]{elegantbook}
```

Use this complete skeleton for new Chinese books:

```tex
%!TEX program = xelatex
% Full chain: xelatex -> biber -> xelatex -> xelatex
\documentclass[lang=cn,newtx,10pt,scheme=chinese]{elegantbook}

\title{Book Title}
\subtitle{Book Subtitle}
\author{Author}
\institute{Institute}
\date{\today}
\version{1.0}
\bioinfo{Info}{Details}

\setcounter{tocdepth}{3}

\logo{logo-blue.png}
\cover{cover.jpg}

\definecolor{customcolor}{RGB}{32,178,170}
\colorlet{coverlinecolor}{customcolor}

\addbibresource[location=local]{reference.bib}

\begin{document}

\maketitle

\frontmatter

\chapter*{Preface}
\addcontentsline{toc}{chapter}{Preface}
Preface text.

\tableofcontents

\mainmatter

\chapter{Chapter Title}

Book content.

\printbibliography[heading=bibintoc]

\end{document}
```

Default behavior:

- Produce a full `.tex` book project, not only a body fragment, unless the user explicitly asks for a fragment.
- Keep `elegantbook.cls` and `reference.bib` in the same directory as the output `.tex`, or otherwise make them discoverable by LaTeX.
- Copy `figure/` when using the bundled logo or cover commands.
- Copy `image/` when the document references bundled or generated figures.
- Use `biblatex` through `reference.bib`; add user-provided bibliography entries to that file and cite them with `\cite{...}` or `\parencite{...}`.
- Include `\frontmatter`, `\tableofcontents`, and `\mainmatter` for complete books.

## Compilation

Use the engine and command chain that matches the document language:

- Chinese books: `xelatex -> biber -> xelatex -> xelatex`.
- English books: `pdflatex -> biber -> pdflatex -> pdflatex`; `xelatex` is acceptable when the user needs Unicode or system fonts.

If `biber` is unavailable, use the template's BibTeX-compatible options only when requested or required by the user's environment.

## Book Structure

When converting source material:

- Map major divisions to `\part` only for large multi-part books.
- Map chapters to `\chapter`, sections to `\section`, and lower levels to `\subsection` or `\subsubsection`.
- Put preliminary material before `\mainmatter`; use `\frontmatter` for preface, acknowledgements, and table of contents.
- Put appendices after `\appendix` when the user provides supplementary chapters.
- Use `figure` and `table` environments with labels for referenced visuals.
- Use the template's built-in theorem-style environments for textbook content: `definition`, `theorem`, `lemma`, `corollary`, `proposition`, `example`, `exercise`, `problem`, `proof`, `note`, `remark`, `solution`, `conclusion`, `assumption`, and `property`.
- Use `lstlisting` for code blocks only when code is part of the book content.

Template options to preserve or choose based on user intent:

- Language: `lang=cn` or `cn` for Chinese, `lang=en` or `en` for English.
- Device: default normal/A4; use `pad` or `device=pad` only when requested.
- Color theme: default `blue`; also supports `green`, `cyan`, `gray`, `black`, and `nocolor`.
- Chapter title style: default `hang`; use `display` when the user requests display-style chapter titles.
- Theorem mode: default `fancy`; use `simple` when the user requests a simpler theorem style.
- Answers/results: use `result=answer` or `result=noanswer` when the user asks to show or hide solutions/proofs.

## Validation

When practical, validate generated book projects by compiling:

- Chinese: run `xelatex`, `biber`, `xelatex`, `xelatex`.
- English: run `pdflatex`, `biber`, `pdflatex`, `pdflatex`.

If TeX is unavailable, still verify that the generated `.tex` has a complete book structure, references the ElegantBook class, includes `\addbibresource[location=local]{reference.bib}`, and keeps required template assets next to the output.
