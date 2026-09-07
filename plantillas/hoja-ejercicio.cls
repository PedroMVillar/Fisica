\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{hoja-ejercicio}[2026/09/07 v0.1 Una hoja apaisada por ejercicio]
% Las opciones que se le pasen a la clase (10pt, 12pt, ...) van a article.
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[11pt,a4paper,landscape]{article}
\RequirePackage{hoja-ejercicio}
