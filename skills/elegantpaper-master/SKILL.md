---
name: elegantpaper-master
description: Use this skill when the user wants a LaTeX paper, working paper, course paper, academic report, research article draft, or converted Markdown/text content produced as a complete ElegantPaper-style .tex project using the bundled ElegantPaper LaTeX template.
---

# ElegantPaper Master

## Purpose

Generate complete, compilable LaTeX paper projects using the bundled ElegantPaper template. Use this skill when the user asks for ElegantPaper style, a LaTeX paper template, working papers, course papers, academic reports, research article drafts, or conversion of Markdown/plain text into an ElegantPaper `.tex` document.

The bundled template lives in `assets/ElegantPaper-master/`. Copy the needed template files into the user's output folder before or while creating the paper project:

- `elegantpaper.cls`
- `reference.bib`
- `image/` when figures or bundled images are used
- `elegantpaper-cn.tex` and `elegantpaper-en.tex` only as examples/reference, not as files to overwrite user output

## Default Documents

For Chinese papers, default to this document class unless the user specifies otherwise:

```tex
\documentclass[lang=cn,a4paper,newtx]{elegantpaper}
```

For English papers, default to:

```tex
\documentclass[11pt,en]{elegantpaper}
```

Use this complete skeleton for new Chinese papers:

```tex
%!TEX program = xelatex
% Full chain: xelatex -> biber -> xelatex -> xelatex
\documentclass[lang=cn,a4paper,newtx]{elegantpaper}

\title{Paper Title}
\author{Author One \\ Affiliation One \and Author Two \\ Affiliation Two}
\institute{Institute}
\version{1.0}
\date{\today}

\addbibresource[location=local]{reference.bib}

\begin{document}

\maketitle

\begin{abstract}
Abstract text.
\keywords{keyword one, keyword two, keyword three}
\end{abstract}

\section{Introduction}

Paper content.

\printbibliography[heading=bibintoc, title=\ebibname]

\end{document}
```

Default behavior:

- Produce a full `.tex` paper project, not only a body fragment, unless the user explicitly asks for a fragment.
- Keep `elegantpaper.cls` and `reference.bib` in the same directory as the output `.tex`, or otherwise make them discoverable by LaTeX.
- Copy `image/` when the document uses bundled images or generated figure files.
- Use `biblatex` through `reference.bib`; add user-provided bibliography entries to that file and cite them with `\cite{...}` or `\parencite{...}`.
- End full papers with `\printbibliography[heading=bibintoc, title=\ebibname]` unless the user requests no bibliography.

## Compilation

Use the engine and command chain that matches the document language:

- Chinese papers: `xelatex -> biber -> xelatex -> xelatex`.
- English papers: `pdflatex -> biber -> pdflatex -> pdflatex`; `xelatex` is acceptable when the user needs Unicode or system fonts.

If `biber` is unavailable, use the template's `bibend=bibtex` option and compile with the matching BibTeX chain.

## Paper Structure

When converting source material:

- Map the paper outline to `\section`, `\subsection`, and `\subsubsection`.
- Include `abstract` and `\keywords{...}` for complete papers.
- Use standard LaTeX math syntax and standard theorem-like environments only when the content needs them.
- Convert code blocks to `lstlisting` only when code is part of the paper.
- Use `figure` and `table` environments with labels for referenced visuals.
- Use `\figref{...}` and `\tabref{...}` when referring to labeled figures and tables.

Template options to preserve or choose based on user intent:

- Language: `lang=cn` or `cn` for Chinese, `lang=en` or `en` for English.
- Paper size and base options: pass article-class options such as `a4paper`, `10pt`, `11pt`, or `12pt`.
- Math fonts: default `math=cm`; use `newtx`/`math=newtx` only when requested or when following the bundled Chinese example.
- Bibliography backend: default `biber`; use `bibend=bibtex` only when requested or required by the environment.
- Bibliography/citation styles: use `bibstyle=...` and `citestyle=...` when the user requests a specific style, such as GB/T 7714.

## Validation

When practical, validate generated paper projects by compiling:

- Chinese: run `xelatex`, `biber`, `xelatex`, `xelatex`.
- English: run `pdflatex`, `biber`, `pdflatex`, `pdflatex`.

If TeX is unavailable, still verify that the generated `.tex` has a complete document structure, references the ElegantPaper class, includes `\addbibresource[location=local]{reference.bib}`, and keeps required template assets next to the output.
