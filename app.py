"""
MarkItDown Local Frontend
=========================
Version: v0.42.1

A self-contained Flask web application that provides a browser-based UI
for Microsoft's MarkItDown library (https://github.com/microsoft/markitdown).

All conversion happens locally — no files or URLs are sent to an external server.

Supported input types (via MarkItDown):
    PDF, DOCX, PPTX, XLSX, XLS, HTML, CSV, JSON, XML,
    EPUB, ZIP, images (JPG/PNG), audio (WAV/MP3), YouTube URLs, and more.

===========================================================================
SETUP & INSTALLATION — macOS
===========================================================================

REQUIREMENTS:
    Python 3.10 or higher. Check your version by opening Terminal and running:
        python3 --version

    If you have 3.9 or lower, download the latest Python from:
        https://www.python.org/downloads/
    The installer may place it under a versioned name e.g. python3.13 or
    python3.14 — use that name in the commands below instead of python3.

ONE-TIME SETUP:
    Open Terminal (press Cmd + Space, type Terminal, press Enter).
    Run each command one at a time, pressing Enter after each:

    1. Navigate to the folder containing this file:
           cd /path/to/your/folder
       Example: cd ~/Desktop/markitdown-app

    2. Create a virtual environment (keeps dependencies isolated):
           python3 -m venv .venv
       If python3 isn't found, try python3.13 or python3.14 instead.

    3. Activate the virtual environment:
           source .venv/bin/activate
       Your prompt will change to show (.venv) when it is active.

    4. Install dependencies:
           pip install "markitdown[all]" flask

    5. Download app.py from GitHub (or clone the repository):
           git clone https://github.com/kasey6801/MarkItDown.git

RUNNING THE APP:
    Each time you want to use the app, run:
        cd /path/to/your/folder
        source .venv/bin/activate
        python app.py

    The app will open automatically in your browser at http://127.0.0.1:5001

STOPPING THE APP:
    Click the Quit button in the top-right corner of the UI,
    or press Control + C in Terminal.

TROUBLESHOOTING (macOS):
    - "command not found: pip"      → Use: python3 -m pip install ...
    - "Port 5001 already in use"    → Another process is using port 5001.
                                       Run: lsof -ti :5001 | xargs kill -9
                                       then restart the app.
    - Xcode prompt appears          → Click Install and wait for it to finish,
                                       then re-run the pip install command.
    - "enable_plugins" error        → You have a newer MarkItDown version;
                                       ensure MarkItDown() has no arguments
                                       (already fixed in this file).


===========================================================================
SETUP & INSTALLATION — Windows
===========================================================================

REQUIREMENTS:
    Python 3.10 or higher. Check your version by opening Command Prompt and
    running:
        python --version

    If you have 3.9 or lower, or Python is not found, download it from:
        https://www.python.org/downloads/
    IMPORTANT: During installation, check the box that says
    "Add Python to PATH" before clicking Install.

ONE-TIME SETUP:
    Open Command Prompt (press Win + R, type cmd, press Enter).
    Run each command one at a time, pressing Enter after each:

    1. Navigate to the folder containing this file:
           cd C:\\path\\to\\your\\folder
       Example: cd C:\\Users\\YourName\\Desktop\\markitdown-app

    2. Create a virtual environment:
           python -m venv .venv

    3. Activate the virtual environment:
           .venv\\Scripts\\activate
       Your prompt will change to show (.venv) when it is active.

    4. Install dependencies:
           pip install "markitdown[all]" flask

    5. Save this file as app.py inside your folder using Notepad or any
       text editor. In Notepad, choose Save As → set file type to
       "All Files" and name it app.py (not app.py.txt).

RUNNING THE APP:
    Each time you want to use the app, open Command Prompt and run:
        cd C:\\path\\to\\your\\folder
        .venv\\Scripts\\activate
        python app.py

    The app will open automatically in your browser at http://127.0.0.1:5001

STOPPING THE APP:
    Click the Quit button in the top-right corner of the UI,
    or press Ctrl + C in Command Prompt.

TROUBLESHOOTING (Windows):
    - "'python' is not recognized"  → Python is not on your PATH. Re-run the
                                       installer and check "Add Python to PATH".
    - "Port 5001 already in use"    → Run: netstat -ano | findstr :5001
                                       then: taskkill /PID <pid> /F
    - pip install fails             → Try running Command Prompt as
                                       Administrator (right-click → Run as
                                       administrator) and repeat the command.
    - File saves as app.py.txt      → In Notepad, set Save As type to
                                       "All Files" before saving.

===========================================================================
"""

from flask import Flask, request, jsonify, render_template_string
from markitdown import MarkItDown
import io, os, time, traceback, threading, webbrowser

# ---------------------------------------------------------------------------
# App Initialisation
# ---------------------------------------------------------------------------

app = Flask(__name__)

# Cap uploaded file size at 100 MB to prevent memory exhaustion on large files.
# Adjust this value if your use case regularly handles larger documents.
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

# Instantiate MarkItDown once at startup rather than per-request.
# This avoids the overhead of re-initialising the converter on every call.
# Instantiate with no arguments — newer versions of MarkItDown removed the
# enable_plugins parameter and handle plugin discovery automatically.
md_converter = MarkItDown()

# ---------------------------------------------------------------------------
# HTML / CSS / JS — Single-file frontend
# ---------------------------------------------------------------------------
# The entire UI is embedded as a Python string so the app ships as one file
# with no separate static assets or template directory required.
# marked.min.js is loaded from a CDN to render the Markdown preview tab.
# ---------------------------------------------------------------------------

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>MarkItDown</title>

  <!-- marked.js: lightweight Markdown → HTML renderer used for the Preview tab -->
  <script>
  /* marked.js v15.0.12 — inlined for offline use */
  /**
 * marked v15.0.12 - a markdown parser
 * Copyright (c) 2011-2025, Christopher Jeffrey. (MIT Licensed)
 * https://github.com/markedjs/marked
 */

/**
 * DO NOT EDIT THIS FILE
 * The code in this file is generated from files in ./src/
 */
(function(g,f){if(typeof exports=="object"&&typeof module<"u"){module.exports=f()}else if("function"==typeof define && define.amd){define("marked",f)}else {g["marked"]=f()}}(typeof globalThis < "u" ? globalThis : typeof self < "u" ? self : this,function(){var exports={};var __exports=exports;var module={exports};
"use strict";var H=Object.defineProperty;var be=Object.getOwnPropertyDescriptor;var Te=Object.getOwnPropertyNames;var we=Object.prototype.hasOwnProperty;var ye=(l,e)=>{for(var t in e)H(l,t,{get:e[t],enumerable:!0})},Re=(l,e,t,n)=>{if(e&&typeof e=="object"||typeof e=="function")for(let s of Te(e))!we.call(l,s)&&s!==t&&H(l,s,{get:()=>e[s],enumerable:!(n=be(e,s))||n.enumerable});return l};var Se=l=>Re(H({},"__esModule",{value:!0}),l);var kt={};ye(kt,{Hooks:()=>L,Lexer:()=>x,Marked:()=>E,Parser:()=>b,Renderer:()=>$,TextRenderer:()=>_,Tokenizer:()=>S,defaults:()=>w,getDefaults:()=>z,lexer:()=>ht,marked:()=>k,options:()=>it,parse:()=>pt,parseInline:()=>ct,parser:()=>ut,setOptions:()=>ot,use:()=>lt,walkTokens:()=>at});module.exports=Se(kt);function z(){return{async:!1,breaks:!1,extensions:null,gfm:!0,hooks:null,pedantic:!1,renderer:null,silent:!1,tokenizer:null,walkTokens:null}}var w=z();function N(l){w=l}var I={exec:()=>null};function h(l,e=""){let t=typeof l=="string"?l:l.source,n={replace:(s,i)=>{let r=typeof i=="string"?i:i.source;return r=r.replace(m.caret,"$1"),t=t.replace(s,r),n},getRegex:()=>new RegExp(t,e)};return n}var m={codeRemoveIndent:/^(?: {1,4}| {0,3}\t)/gm,outputLinkReplace:/\\([\[\]])/g,indentCodeCompensation:/^(\s+)(?:```)/,beginningSpace:/^\s+/,endingHash:/#$/,startingSpaceChar:/^ /,endingSpaceChar:/ $/,nonSpaceChar:/[^ ]/,newLineCharGlobal:/\n/g,tabCharGlobal:/\t/g,multipleSpaceGlobal:/\s+/g,blankLine:/^[ \t]*$/,doubleBlankLine:/\n[ \t]*\n[ \t]*$/,blockquoteStart:/^ {0,3}>/,blockquoteSetextReplace:/\n {0,3}((?:=+|-+) *)(?=\n|$)/g,blockquoteSetextReplace2:/^ {0,3}>[ \t]?/gm,listReplaceTabs:/^\t+/,listReplaceNesting:/^ {1,4}(?=( {4})*[^ ])/g,listIsTask:/^\[[ xX]\] /,listReplaceTask:/^\[[ xX]\] +/,anyLine:/\n.*\n/,hrefBrackets:/^<(.*)>$/,tableDelimiter:/[:|]/,tableAlignChars:/^\||\| *$/g,tableRowBlankLine:/\n[ \t]*$/,tableAlignRight:/^ *-+: *$/,tableAlignCenter:/^ *:-+: *$/,tableAlignLeft:/^ *:-+ *$/,startATag:/^<a /i,endATag:/^<\/a>/i,startPreScriptTag:/^<(pre|code|kbd|script)(\s|>)/i,endPreScriptTag:/^<\/(pre|code|kbd|script)(\s|>)/i,startAngleBracket:/^</,endAngleBracket:/>$/,pedanticHrefTitle:/^([^'"]*[^\s])\s+(['"])(.*)\2/,unicodeAlphaNumeric:/[\p{L}\p{N}]/u,escapeTest:/[&<>"']/,escapeReplace:/[&<>"']/g,escapeTestNoEncode:/[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/,escapeReplaceNoEncode:/[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/g,unescapeTest:/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/ig,caret:/(^|[^\[])\^/g,percentDecode:/%25/g,findPipe:/\|/g,splitPipe:/ \|/,slashPipe:/\\\|/g,carriageReturn:/\r\n|\r/g,spaceLine:/^ +$/gm,notSpaceStart:/^\S*/,endingNewline:/\n$/,listItemRegex:l=>new RegExp(`^( {0,3}${l})((?:[	 ][^\\n]*)?(?:\\n|$))`),nextBulletRegex:l=>new RegExp(`^ {0,${Math.min(3,l-1)}}(?:[*+-]|\\d{1,9}[.)])((?:[ 	][^\\n]*)?(?:\\n|$))`),hrRegex:l=>new RegExp(`^ {0,${Math.min(3,l-1)}}((?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$)`),fencesBeginRegex:l=>new RegExp(`^ {0,${Math.min(3,l-1)}}(?:\`\`\`|~~~)`),headingBeginRegex:l=>new RegExp(`^ {0,${Math.min(3,l-1)}}#`),htmlBeginRegex:l=>new RegExp(`^ {0,${Math.min(3,l-1)}}<(?:[a-z].*>|!--)`,"i")},$e=/^(?:[ \t]*(?:\n|$))+/,_e=/^((?: {4}| {0,3}\t)[^\n]+(?:\n(?:[ \t]*(?:\n|$))*)?)+/,Le=/^ {0,3}(`{3,}(?=[^`\n]*(?:\n|$))|~{3,})([^\n]*)(?:\n|$)(?:|([\s\S]*?)(?:\n|$))(?: {0,3}\1[~`]* *(?=\n|$)|$)/,O=/^ {0,3}((?:-[\t ]*){3,}|(?:_[ \t]*){3,}|(?:\*[ \t]*){3,})(?:\n+|$)/,ze=/^ {0,3}(#{1,6})(?=\s|$)(.*)(?:\n+|$)/,F=/(?:[*+-]|\d{1,9}[.)])/,ie=/^(?!bull |blockCode|fences|blockquote|heading|html|table)((?:.|\n(?!\s*?\n|bull |blockCode|fences|blockquote|heading|html|table))+?)\n {0,3}(=+|-+) *(?:\n+|$)/,oe=h(ie).replace(/bull/g,F).replace(/blockCode/g,/(?: {4}| {0,3}\t)/).replace(/fences/g,/ {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g,/ {0,3}>/).replace(/heading/g,/ {0,3}#{1,6}/).replace(/html/g,/ {0,3}<[^\n>]+>\n/).replace(/\|table/g,"").getRegex(),Me=h(ie).replace(/bull/g,F).replace(/blockCode/g,/(?: {4}| {0,3}\t)/).replace(/fences/g,/ {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g,/ {0,3}>/).replace(/heading/g,/ {0,3}#{1,6}/).replace(/html/g,/ {0,3}<[^\n>]+>\n/).replace(/table/g,/ {0,3}\|?(?:[:\- ]*\|)+[\:\- ]*\n/).getRegex(),Q=/^([^\n]+(?:\n(?!hr|heading|lheading|blockquote|fences|list|html|table| +\n)[^\n]+)*)/,Pe=/^[^\n]+/,U=/(?!\s*\])(?:\\.|[^\[\]\\])+/,Ae=h(/^ {0,3}\[(label)\]: *(?:\n[ \t]*)?([^<\s][^\s]*|<.*?>)(?:(?: +(?:\n[ \t]*)?| *\n[ \t]*)(title))? *(?:\n+|$)/).replace("label",U).replace("title",/(?:"(?:\\"?|[^"\\])*"|'[^'\n]*(?:\n[^'\n]+)*\n?'|\([^()]*\))/).getRegex(),Ee=h(/^( {0,3}bull)([ \t][^\n]+?)?(?:\n|$)/).replace(/bull/g,F).getRegex(),v="address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|meta|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul",K=/<!--(?:-?>|[\s\S]*?(?:-->|$))/,Ce=h("^ {0,3}(?:<(script|pre|style|textarea)[\\s>][\\s\\S]*?(?:</\\1>[^\\n]*\\n+|$)|comment[^\\n]*(\\n+|$)|<\\?[\\s\\S]*?(?:\\?>\\n*|$)|<![A-Z][\\s\\S]*?(?:>\\n*|$)|<!\\[CDATA\\[[\\s\\S]*?(?:\\]\\]>\\n*|$)|</?(tag)(?: +|\\n|/?>)[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$)|<(?!script|pre|style|textarea)([a-z][\\w-]*)(?:attribute)*? */?>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$)|</(?!script|pre|style|textarea)[a-z][\\w-]*\\s*>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$))","i").replace("comment",K).replace("tag",v).replace("attribute",/ +[a-zA-Z:_][\w.:-]*(?: *= *"[^"\n]*"| *= *'[^'\n]*'| *= *[^\s"'=<>`]+)?/).getRegex(),le=h(Q).replace("hr",O).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("|lheading","").replace("|table","").replace("blockquote"," {0,3}>").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",v).getRegex(),Ie=h(/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/).replace("paragraph",le).getRegex(),X={blockquote:Ie,code:_e,def:Ae,fences:Le,heading:ze,hr:O,html:Ce,lheading:oe,list:Ee,newline:$e,paragraph:le,table:I,text:Pe},re=h("^ *([^\\n ].*)\\n {0,3}((?:\\| *)?:?-+:? *(?:\\| *:?-+:? *)*(?:\\| *)?)(?:\\n((?:(?! *\\n|hr|heading|blockquote|code|fences|list|html).*(?:\\n|$))*)\\n*|$)").replace("hr",O).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("blockquote"," {0,3}>").replace("code","(?: {4}| {0,3}	)[^\\n]").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",v).getRegex(),Oe={...X,lheading:Me,table:re,paragraph:h(Q).replace("hr",O).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("|lheading","").replace("table",re).replace("blockquote"," {0,3}>").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",v).getRegex()},Be={...X,html:h(`^ *(?:comment *(?:\\n|\\s*$)|<(tag)[\\s\\S]+?</\\1> *(?:\\n{2,}|\\s*$)|<tag(?:"[^"]*"|'[^']*'|\\s[^'"/>\\s]*)*?/?> *(?:\\n{2,}|\\s*$))`).replace("comment",K).replace(/tag/g,"(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b").getRegex(),def:/^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +(["(][^\n]+[")]))? *(?:\n+|$)/,heading:/^(#{1,6})(.*)(?:\n+|$)/,fences:I,lheading:/^(.+?)\n {0,3}(=+|-+) *(?:\n+|$)/,paragraph:h(Q).replace("hr",O).replace("heading",` *#{1,6} *[^
]`).replace("lheading",oe).replace("|table","").replace("blockquote"," {0,3}>").replace("|fences","").replace("|list","").replace("|html","").replace("|tag","").getRegex()},qe=/^\\([!"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])/,ve=/^(`+)([^`]|[^`][\s\S]*?[^`])\1(?!`)/,ae=/^( {2,}|\\)\n(?!\s*$)/,De=/^(`+|[^`])(?:(?= {2,}\n)|[\s\S]*?(?:(?=[\\<!\[`*_]|\b_|$)|[^ ](?= {2,}\n)))/,D=/[\p{P}\p{S}]/u,W=/[\s\p{P}\p{S}]/u,ce=/[^\s\p{P}\p{S}]/u,Ze=h(/^((?![*_])punctSpace)/,"u").replace(/punctSpace/g,W).getRegex(),pe=/(?!~)[\p{P}\p{S}]/u,Ge=/(?!~)[\s\p{P}\p{S}]/u,He=/(?:[^\s\p{P}\p{S}]|~)/u,Ne=/\[[^[\]]*?\]\((?:\\.|[^\\\(\)]|\((?:\\.|[^\\\(\)])*\))*\)|`[^`]*?`|<[^<>]*?>/g,ue=/^(?:\*+(?:((?!\*)punct)|[^\s*]))|^_+(?:((?!_)punct)|([^\s_]))/,je=h(ue,"u").replace(/punct/g,D).getRegex(),Fe=h(ue,"u").replace(/punct/g,pe).getRegex(),he="^[^_*]*?__[^_*]*?\\*[^_*]*?(?=__)|[^*]+(?=[^*])|(?!\\*)punct(\\*+)(?=[\\s]|$)|notPunctSpace(\\*+)(?!\\*)(?=punctSpace|$)|(?!\\*)punctSpace(\\*+)(?=notPunctSpace)|[\\s](\\*+)(?!\\*)(?=punct)|(?!\\*)punct(\\*+)(?!\\*)(?=punct)|notPunctSpace(\\*+)(?=notPunctSpace)",Qe=h(he,"gu").replace(/notPunctSpace/g,ce).replace(/punctSpace/g,W).replace(/punct/g,D).getRegex(),Ue=h(he,"gu").replace(/notPunctSpace/g,He).replace(/punctSpace/g,Ge).replace(/punct/g,pe).getRegex(),Ke=h("^[^_*]*?\\*\\*[^_*]*?_[^_*]*?(?=\\*\\*)|[^_]+(?=[^_])|(?!_)punct(_+)(?=[\\s]|$)|notPunctSpace(_+)(?!_)(?=punctSpace|$)|(?!_)punctSpace(_+)(?=notPunctSpace)|[\\s](_+)(?!_)(?=punct)|(?!_)punct(_+)(?!_)(?=punct)","gu").replace(/notPunctSpace/g,ce).replace(/punctSpace/g,W).replace(/punct/g,D).getRegex(),Xe=h(/\\(punct)/,"gu").replace(/punct/g,D).getRegex(),We=h(/^<(scheme:[^\s\x00-\x1f<>]*|email)>/).replace("scheme",/[a-zA-Z][a-zA-Z0-9+.-]{1,31}/).replace("email",/[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/).getRegex(),Je=h(K).replace("(?:-->|$)","-->").getRegex(),Ve=h("^comment|^</[a-zA-Z][\\w:-]*\\s*>|^<[a-zA-Z][\\w-]*(?:attribute)*?\\s*/?>|^<\\?[\\s\\S]*?\\?>|^<![a-zA-Z]+\\s[\\s\\S]*?>|^<!\\[CDATA\\[[\\s\\S]*?\\]\\]>").replace("comment",Je).replace("attribute",/\s+[a-zA-Z:_][\w.:-]*(?:\s*=\s*"[^"]*"|\s*=\s*'[^']*'|\s*=\s*[^\s"'=<>`]+)?/).getRegex(),q=/(?:\[(?:\\.|[^\[\]\\])*\]|\\.|`[^`]*`|[^\[\]\\`])*?/,Ye=h(/^!?\[(label)\]\(\s*(href)(?:(?:[ \t]*(?:\n[ \t]*)?)(title))?\s*\)/).replace("label",q).replace("href",/<(?:\\.|[^\n<>\\])+>|[^ \t\n\x00-\x1f]*/).replace("title",/"(?:\\"?|[^"\\])*"|'(?:\\'?|[^'\\])*'|\((?:\\\)?|[^)\\])*\)/).getRegex(),ke=h(/^!?\[(label)\]\[(ref)\]/).replace("label",q).replace("ref",U).getRegex(),ge=h(/^!?\[(ref)\](?:\[\])?/).replace("ref",U).getRegex(),et=h("reflink|nolink(?!\\()","g").replace("reflink",ke).replace("nolink",ge).getRegex(),J={_backpedal:I,anyPunctuation:Xe,autolink:We,blockSkip:Ne,br:ae,code:ve,del:I,emStrongLDelim:je,emStrongRDelimAst:Qe,emStrongRDelimUnd:Ke,escape:qe,link:Ye,nolink:ge,punctuation:Ze,reflink:ke,reflinkSearch:et,tag:Ve,text:De,url:I},tt={...J,link:h(/^!?\[(label)\]\((.*?)\)/).replace("label",q).getRegex(),reflink:h(/^!?\[(label)\]\s*\[([^\]]*)\]/).replace("label",q).getRegex()},j={...J,emStrongRDelimAst:Ue,emStrongLDelim:Fe,url:h(/^((?:ftp|https?):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/,"i").replace("email",/[A-Za-z0-9._+-]+(@)[a-zA-Z0-9-_]+(?:\.[a-zA-Z0-9-_]*[a-zA-Z0-9])+(?![-_])/).getRegex(),_backpedal:/(?:[^?!.,:;*_'"~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_'"~)]+(?!$))+/,del:/^(~~?)(?=[^\s~])((?:\\.|[^\\])*?(?:\\.|[^\s~\\]))\1(?=[^~]|$)/,text:/^([`~]+|[^`~])(?:(?= {2,}\n)|(?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)|[\s\S]*?(?:(?=[\\<!\[`*~_]|\b_|https?:\/\/|ftp:\/\/|www\.|$)|[^ ](?= {2,}\n)|[^a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-](?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)))/},nt={...j,br:h(ae).replace("{2,}","*").getRegex(),text:h(j.text).replace("\\b_","\\b_| {2,}\\n").replace(/\{2,\}/g,"*").getRegex()},B={normal:X,gfm:Oe,pedantic:Be},P={normal:J,gfm:j,breaks:nt,pedantic:tt};var st={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"},fe=l=>st[l];function R(l,e){if(e){if(m.escapeTest.test(l))return l.replace(m.escapeReplace,fe)}else if(m.escapeTestNoEncode.test(l))return l.replace(m.escapeReplaceNoEncode,fe);return l}function V(l){try{l=encodeURI(l).replace(m.percentDecode,"%")}catch{return null}return l}function Y(l,e){let t=l.replace(m.findPipe,(i,r,o)=>{let a=!1,c=r;for(;--c>=0&&o[c]==="\\";)a=!a;return a?"|":" |"}),n=t.split(m.splitPipe),s=0;if(n[0].trim()||n.shift(),n.length>0&&!n.at(-1)?.trim()&&n.pop(),e)if(n.length>e)n.splice(e);else for(;n.length<e;)n.push("");for(;s<n.length;s++)n[s]=n[s].trim().replace(m.slashPipe,"|");return n}function A(l,e,t){let n=l.length;if(n===0)return"";let s=0;for(;s<n;){let i=l.charAt(n-s-1);if(i===e&&!t)s++;else if(i!==e&&t)s++;else break}return l.slice(0,n-s)}function de(l,e){if(l.indexOf(e[1])===-1)return-1;let t=0;for(let n=0;n<l.length;n++)if(l[n]==="\\")n++;else if(l[n]===e[0])t++;else if(l[n]===e[1]&&(t--,t<0))return n;return t>0?-2:-1}function me(l,e,t,n,s){let i=e.href,r=e.title||null,o=l[1].replace(s.other.outputLinkReplace,"$1");n.state.inLink=!0;let a={type:l[0].charAt(0)==="!"?"image":"link",raw:t,href:i,title:r,text:o,tokens:n.inlineTokens(o)};return n.state.inLink=!1,a}function rt(l,e,t){let n=l.match(t.other.indentCodeCompensation);if(n===null)return e;let s=n[1];return e.split(`
`).map(i=>{let r=i.match(t.other.beginningSpace);if(r===null)return i;let[o]=r;return o.length>=s.length?i.slice(s.length):i}).join(`
`)}var S=class{options;rules;lexer;constructor(e){this.options=e||w}space(e){let t=this.rules.block.newline.exec(e);if(t&&t[0].length>0)return{type:"space",raw:t[0]}}code(e){let t=this.rules.block.code.exec(e);if(t){let n=t[0].replace(this.rules.other.codeRemoveIndent,"");return{type:"code",raw:t[0],codeBlockStyle:"indented",text:this.options.pedantic?n:A(n,`
`)}}}fences(e){let t=this.rules.block.fences.exec(e);if(t){let n=t[0],s=rt(n,t[3]||"",this.rules);return{type:"code",raw:n,lang:t[2]?t[2].trim().replace(this.rules.inline.anyPunctuation,"$1"):t[2],text:s}}}heading(e){let t=this.rules.block.heading.exec(e);if(t){let n=t[2].trim();if(this.rules.other.endingHash.test(n)){let s=A(n,"#");(this.options.pedantic||!s||this.rules.other.endingSpaceChar.test(s))&&(n=s.trim())}return{type:"heading",raw:t[0],depth:t[1].length,text:n,tokens:this.lexer.inline(n)}}}hr(e){let t=this.rules.block.hr.exec(e);if(t)return{type:"hr",raw:A(t[0],`
`)}}blockquote(e){let t=this.rules.block.blockquote.exec(e);if(t){let n=A(t[0],`
`).split(`
`),s="",i="",r=[];for(;n.length>0;){let o=!1,a=[],c;for(c=0;c<n.length;c++)if(this.rules.other.blockquoteStart.test(n[c]))a.push(n[c]),o=!0;else if(!o)a.push(n[c]);else break;n=n.slice(c);let p=a.join(`
`),u=p.replace(this.rules.other.blockquoteSetextReplace,`
    $1`).replace(this.rules.other.blockquoteSetextReplace2,"");s=s?`${s}
${p}`:p,i=i?`${i}
${u}`:u;let d=this.lexer.state.top;if(this.lexer.state.top=!0,this.lexer.blockTokens(u,r,!0),this.lexer.state.top=d,n.length===0)break;let g=r.at(-1);if(g?.type==="code")break;if(g?.type==="blockquote"){let T=g,f=T.raw+`
`+n.join(`
`),y=this.blockquote(f);r[r.length-1]=y,s=s.substring(0,s.length-T.raw.length)+y.raw,i=i.substring(0,i.length-T.text.length)+y.text;break}else if(g?.type==="list"){let T=g,f=T.raw+`
`+n.join(`
`),y=this.list(f);r[r.length-1]=y,s=s.substring(0,s.length-g.raw.length)+y.raw,i=i.substring(0,i.length-T.raw.length)+y.raw,n=f.substring(r.at(-1).raw.length).split(`
`);continue}}return{type:"blockquote",raw:s,tokens:r,text:i}}}list(e){let t=this.rules.block.list.exec(e);if(t){let n=t[1].trim(),s=n.length>1,i={type:"list",raw:"",ordered:s,start:s?+n.slice(0,-1):"",loose:!1,items:[]};n=s?`\\d{1,9}\\${n.slice(-1)}`:`\\${n}`,this.options.pedantic&&(n=s?n:"[*+-]");let r=this.rules.other.listItemRegex(n),o=!1;for(;e;){let c=!1,p="",u="";if(!(t=r.exec(e))||this.rules.block.hr.test(e))break;p=t[0],e=e.substring(p.length);let d=t[2].split(`
`,1)[0].replace(this.rules.other.listReplaceTabs,Z=>" ".repeat(3*Z.length)),g=e.split(`
`,1)[0],T=!d.trim(),f=0;if(this.options.pedantic?(f=2,u=d.trimStart()):T?f=t[1].length+1:(f=t[2].search(this.rules.other.nonSpaceChar),f=f>4?1:f,u=d.slice(f),f+=t[1].length),T&&this.rules.other.blankLine.test(g)&&(p+=g+`
`,e=e.substring(g.length+1),c=!0),!c){let Z=this.rules.other.nextBulletRegex(f),te=this.rules.other.hrRegex(f),ne=this.rules.other.fencesBeginRegex(f),se=this.rules.other.headingBeginRegex(f),xe=this.rules.other.htmlBeginRegex(f);for(;e;){let G=e.split(`
`,1)[0],C;if(g=G,this.options.pedantic?(g=g.replace(this.rules.other.listReplaceNesting,"  "),C=g):C=g.replace(this.rules.other.tabCharGlobal,"    "),ne.test(g)||se.test(g)||xe.test(g)||Z.test(g)||te.test(g))break;if(C.search(this.rules.other.nonSpaceChar)>=f||!g.trim())u+=`
`+C.slice(f);else{if(T||d.replace(this.rules.other.tabCharGlobal,"    ").search(this.rules.other.nonSpaceChar)>=4||ne.test(d)||se.test(d)||te.test(d))break;u+=`
`+g}!T&&!g.trim()&&(T=!0),p+=G+`
`,e=e.substring(G.length+1),d=C.slice(f)}}i.loose||(o?i.loose=!0:this.rules.other.doubleBlankLine.test(p)&&(o=!0));let y=null,ee;this.options.gfm&&(y=this.rules.other.listIsTask.exec(u),y&&(ee=y[0]!=="[ ] ",u=u.replace(this.rules.other.listReplaceTask,""))),i.items.push({type:"list_item",raw:p,task:!!y,checked:ee,loose:!1,text:u,tokens:[]}),i.raw+=p}let a=i.items.at(-1);if(a)a.raw=a.raw.trimEnd(),a.text=a.text.trimEnd();else return;i.raw=i.raw.trimEnd();for(let c=0;c<i.items.length;c++)if(this.lexer.state.top=!1,i.items[c].tokens=this.lexer.blockTokens(i.items[c].text,[]),!i.loose){let p=i.items[c].tokens.filter(d=>d.type==="space"),u=p.length>0&&p.some(d=>this.rules.other.anyLine.test(d.raw));i.loose=u}if(i.loose)for(let c=0;c<i.items.length;c++)i.items[c].loose=!0;return i}}html(e){let t=this.rules.block.html.exec(e);if(t)return{type:"html",block:!0,raw:t[0],pre:t[1]==="pre"||t[1]==="script"||t[1]==="style",text:t[0]}}def(e){let t=this.rules.block.def.exec(e);if(t){let n=t[1].toLowerCase().replace(this.rules.other.multipleSpaceGlobal," "),s=t[2]?t[2].replace(this.rules.other.hrefBrackets,"$1").replace(this.rules.inline.anyPunctuation,"$1"):"",i=t[3]?t[3].substring(1,t[3].length-1).replace(this.rules.inline.anyPunctuation,"$1"):t[3];return{type:"def",tag:n,raw:t[0],href:s,title:i}}}table(e){let t=this.rules.block.table.exec(e);if(!t||!this.rules.other.tableDelimiter.test(t[2]))return;let n=Y(t[1]),s=t[2].replace(this.rules.other.tableAlignChars,"").split("|"),i=t[3]?.trim()?t[3].replace(this.rules.other.tableRowBlankLine,"").split(`
`):[],r={type:"table",raw:t[0],header:[],align:[],rows:[]};if(n.length===s.length){for(let o of s)this.rules.other.tableAlignRight.test(o)?r.align.push("right"):this.rules.other.tableAlignCenter.test(o)?r.align.push("center"):this.rules.other.tableAlignLeft.test(o)?r.align.push("left"):r.align.push(null);for(let o=0;o<n.length;o++)r.header.push({text:n[o],tokens:this.lexer.inline(n[o]),header:!0,align:r.align[o]});for(let o of i)r.rows.push(Y(o,r.header.length).map((a,c)=>({text:a,tokens:this.lexer.inline(a),header:!1,align:r.align[c]})));return r}}lheading(e){let t=this.rules.block.lheading.exec(e);if(t)return{type:"heading",raw:t[0],depth:t[2].charAt(0)==="="?1:2,text:t[1],tokens:this.lexer.inline(t[1])}}paragraph(e){let t=this.rules.block.paragraph.exec(e);if(t){let n=t[1].charAt(t[1].length-1)===`
`?t[1].slice(0,-1):t[1];return{type:"paragraph",raw:t[0],text:n,tokens:this.lexer.inline(n)}}}text(e){let t=this.rules.block.text.exec(e);if(t)return{type:"text",raw:t[0],text:t[0],tokens:this.lexer.inline(t[0])}}escape(e){let t=this.rules.inline.escape.exec(e);if(t)return{type:"escape",raw:t[0],text:t[1]}}tag(e){let t=this.rules.inline.tag.exec(e);if(t)return!this.lexer.state.inLink&&this.rules.other.startATag.test(t[0])?this.lexer.state.inLink=!0:this.lexer.state.inLink&&this.rules.other.endATag.test(t[0])&&(this.lexer.state.inLink=!1),!this.lexer.state.inRawBlock&&this.rules.other.startPreScriptTag.test(t[0])?this.lexer.state.inRawBlock=!0:this.lexer.state.inRawBlock&&this.rules.other.endPreScriptTag.test(t[0])&&(this.lexer.state.inRawBlock=!1),{type:"html",raw:t[0],inLink:this.lexer.state.inLink,inRawBlock:this.lexer.state.inRawBlock,block:!1,text:t[0]}}link(e){let t=this.rules.inline.link.exec(e);if(t){let n=t[2].trim();if(!this.options.pedantic&&this.rules.other.startAngleBracket.test(n)){if(!this.rules.other.endAngleBracket.test(n))return;let r=A(n.slice(0,-1),"\\");if((n.length-r.length)%2===0)return}else{let r=de(t[2],"()");if(r===-2)return;if(r>-1){let a=(t[0].indexOf("!")===0?5:4)+t[1].length+r;t[2]=t[2].substring(0,r),t[0]=t[0].substring(0,a).trim(),t[3]=""}}let s=t[2],i="";if(this.options.pedantic){let r=this.rules.other.pedanticHrefTitle.exec(s);r&&(s=r[1],i=r[3])}else i=t[3]?t[3].slice(1,-1):"";return s=s.trim(),this.rules.other.startAngleBracket.test(s)&&(this.options.pedantic&&!this.rules.other.endAngleBracket.test(n)?s=s.slice(1):s=s.slice(1,-1)),me(t,{href:s&&s.replace(this.rules.inline.anyPunctuation,"$1"),title:i&&i.replace(this.rules.inline.anyPunctuation,"$1")},t[0],this.lexer,this.rules)}}reflink(e,t){let n;if((n=this.rules.inline.reflink.exec(e))||(n=this.rules.inline.nolink.exec(e))){let s=(n[2]||n[1]).replace(this.rules.other.multipleSpaceGlobal," "),i=t[s.toLowerCase()];if(!i){let r=n[0].charAt(0);return{type:"text",raw:r,text:r}}return me(n,i,n[0],this.lexer,this.rules)}}emStrong(e,t,n=""){let s=this.rules.inline.emStrongLDelim.exec(e);if(!s||s[3]&&n.match(this.rules.other.unicodeAlphaNumeric))return;if(!(s[1]||s[2]||"")||!n||this.rules.inline.punctuation.exec(n)){let r=[...s[0]].length-1,o,a,c=r,p=0,u=s[0][0]==="*"?this.rules.inline.emStrongRDelimAst:this.rules.inline.emStrongRDelimUnd;for(u.lastIndex=0,t=t.slice(-1*e.length+r);(s=u.exec(t))!=null;){if(o=s[1]||s[2]||s[3]||s[4]||s[5]||s[6],!o)continue;if(a=[...o].length,s[3]||s[4]){c+=a;continue}else if((s[5]||s[6])&&r%3&&!((r+a)%3)){p+=a;continue}if(c-=a,c>0)continue;a=Math.min(a,a+c+p);let d=[...s[0]][0].length,g=e.slice(0,r+s.index+d+a);if(Math.min(r,a)%2){let f=g.slice(1,-1);return{type:"em",raw:g,text:f,tokens:this.lexer.inlineTokens(f)}}let T=g.slice(2,-2);return{type:"strong",raw:g,text:T,tokens:this.lexer.inlineTokens(T)}}}}codespan(e){let t=this.rules.inline.code.exec(e);if(t){let n=t[2].replace(this.rules.other.newLineCharGlobal," "),s=this.rules.other.nonSpaceChar.test(n),i=this.rules.other.startingSpaceChar.test(n)&&this.rules.other.endingSpaceChar.test(n);return s&&i&&(n=n.substring(1,n.length-1)),{type:"codespan",raw:t[0],text:n}}}br(e){let t=this.rules.inline.br.exec(e);if(t)return{type:"br",raw:t[0]}}del(e){let t=this.rules.inline.del.exec(e);if(t)return{type:"del",raw:t[0],text:t[2],tokens:this.lexer.inlineTokens(t[2])}}autolink(e){let t=this.rules.inline.autolink.exec(e);if(t){let n,s;return t[2]==="@"?(n=t[1],s="mailto:"+n):(n=t[1],s=n),{type:"link",raw:t[0],text:n,href:s,tokens:[{type:"text",raw:n,text:n}]}}}url(e){let t;if(t=this.rules.inline.url.exec(e)){let n,s;if(t[2]==="@")n=t[0],s="mailto:"+n;else{let i;do i=t[0],t[0]=this.rules.inline._backpedal.exec(t[0])?.[0]??"";while(i!==t[0]);n=t[0],t[1]==="www."?s="http://"+t[0]:s=t[0]}return{type:"link",raw:t[0],text:n,href:s,tokens:[{type:"text",raw:n,text:n}]}}}inlineText(e){let t=this.rules.inline.text.exec(e);if(t){let n=this.lexer.state.inRawBlock;return{type:"text",raw:t[0],text:t[0],escaped:n}}}};var x=class l{tokens;options;state;tokenizer;inlineQueue;constructor(e){this.tokens=[],this.tokens.links=Object.create(null),this.options=e||w,this.options.tokenizer=this.options.tokenizer||new S,this.tokenizer=this.options.tokenizer,this.tokenizer.options=this.options,this.tokenizer.lexer=this,this.inlineQueue=[],this.state={inLink:!1,inRawBlock:!1,top:!0};let t={other:m,block:B.normal,inline:P.normal};this.options.pedantic?(t.block=B.pedantic,t.inline=P.pedantic):this.options.gfm&&(t.block=B.gfm,this.options.breaks?t.inline=P.breaks:t.inline=P.gfm),this.tokenizer.rules=t}static get rules(){return{block:B,inline:P}}static lex(e,t){return new l(t).lex(e)}static lexInline(e,t){return new l(t).inlineTokens(e)}lex(e){e=e.replace(m.carriageReturn,`
`),this.blockTokens(e,this.tokens);for(let t=0;t<this.inlineQueue.length;t++){let n=this.inlineQueue[t];this.inlineTokens(n.src,n.tokens)}return this.inlineQueue=[],this.tokens}blockTokens(e,t=[],n=!1){for(this.options.pedantic&&(e=e.replace(m.tabCharGlobal,"    ").replace(m.spaceLine,""));e;){let s;if(this.options.extensions?.block?.some(r=>(s=r.call({lexer:this},e,t))?(e=e.substring(s.raw.length),t.push(s),!0):!1))continue;if(s=this.tokenizer.space(e)){e=e.substring(s.raw.length);let r=t.at(-1);s.raw.length===1&&r!==void 0?r.raw+=`
`:t.push(s);continue}if(s=this.tokenizer.code(e)){e=e.substring(s.raw.length);let r=t.at(-1);r?.type==="paragraph"||r?.type==="text"?(r.raw+=`
`+s.raw,r.text+=`
`+s.text,this.inlineQueue.at(-1).src=r.text):t.push(s);continue}if(s=this.tokenizer.fences(e)){e=e.substring(s.raw.length),t.push(s);continue}if(s=this.tokenizer.heading(e)){e=e.substring(s.raw.length),t.push(s);continue}if(s=this.tokenizer.hr(e)){e=e.substring(s.raw.length),t.push(s);continue}if(s=this.tokenizer.blockquote(e)){e=e.substring(s.raw.length),t.push(s);continue}if(s=this.tokenizer.list(e)){e=e.substring(s.raw.length),t.push(s);continue}if(s=this.tokenizer.html(e)){e=e.substring(s.raw.length),t.push(s);continue}if(s=this.tokenizer.def(e)){e=e.substring(s.raw.length);let r=t.at(-1);r?.type==="paragraph"||r?.type==="text"?(r.raw+=`
`+s.raw,r.text+=`
`+s.raw,this.inlineQueue.at(-1).src=r.text):this.tokens.links[s.tag]||(this.tokens.links[s.tag]={href:s.href,title:s.title});continue}if(s=this.tokenizer.table(e)){e=e.substring(s.raw.length),t.push(s);continue}if(s=this.tokenizer.lheading(e)){e=e.substring(s.raw.length),t.push(s);continue}let i=e;if(this.options.extensions?.startBlock){let r=1/0,o=e.slice(1),a;this.options.extensions.startBlock.forEach(c=>{a=c.call({lexer:this},o),typeof a=="number"&&a>=0&&(r=Math.min(r,a))}),r<1/0&&r>=0&&(i=e.substring(0,r+1))}if(this.state.top&&(s=this.tokenizer.paragraph(i))){let r=t.at(-1);n&&r?.type==="paragraph"?(r.raw+=`
`+s.raw,r.text+=`
`+s.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=r.text):t.push(s),n=i.length!==e.length,e=e.substring(s.raw.length);continue}if(s=this.tokenizer.text(e)){e=e.substring(s.raw.length);let r=t.at(-1);r?.type==="text"?(r.raw+=`
`+s.raw,r.text+=`
`+s.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=r.text):t.push(s);continue}if(e){let r="Infinite loop on byte: "+e.charCodeAt(0);if(this.options.silent){console.error(r);break}else throw new Error(r)}}return this.state.top=!0,t}inline(e,t=[]){return this.inlineQueue.push({src:e,tokens:t}),t}inlineTokens(e,t=[]){let n=e,s=null;if(this.tokens.links){let o=Object.keys(this.tokens.links);if(o.length>0)for(;(s=this.tokenizer.rules.inline.reflinkSearch.exec(n))!=null;)o.includes(s[0].slice(s[0].lastIndexOf("[")+1,-1))&&(n=n.slice(0,s.index)+"["+"a".repeat(s[0].length-2)+"]"+n.slice(this.tokenizer.rules.inline.reflinkSearch.lastIndex))}for(;(s=this.tokenizer.rules.inline.anyPunctuation.exec(n))!=null;)n=n.slice(0,s.index)+"++"+n.slice(this.tokenizer.rules.inline.anyPunctuation.lastIndex);for(;(s=this.tokenizer.rules.inline.blockSkip.exec(n))!=null;)n=n.slice(0,s.index)+"["+"a".repeat(s[0].length-2)+"]"+n.slice(this.tokenizer.rules.inline.blockSkip.lastIndex);let i=!1,r="";for(;e;){i||(r=""),i=!1;let o;if(this.options.extensions?.inline?.some(c=>(o=c.call({lexer:this},e,t))?(e=e.substring(o.raw.length),t.push(o),!0):!1))continue;if(o=this.tokenizer.escape(e)){e=e.substring(o.raw.length),t.push(o);continue}if(o=this.tokenizer.tag(e)){e=e.substring(o.raw.length),t.push(o);continue}if(o=this.tokenizer.link(e)){e=e.substring(o.raw.length),t.push(o);continue}if(o=this.tokenizer.reflink(e,this.tokens.links)){e=e.substring(o.raw.length);let c=t.at(-1);o.type==="text"&&c?.type==="text"?(c.raw+=o.raw,c.text+=o.text):t.push(o);continue}if(o=this.tokenizer.emStrong(e,n,r)){e=e.substring(o.raw.length),t.push(o);continue}if(o=this.tokenizer.codespan(e)){e=e.substring(o.raw.length),t.push(o);continue}if(o=this.tokenizer.br(e)){e=e.substring(o.raw.length),t.push(o);continue}if(o=this.tokenizer.del(e)){e=e.substring(o.raw.length),t.push(o);continue}if(o=this.tokenizer.autolink(e)){e=e.substring(o.raw.length),t.push(o);continue}if(!this.state.inLink&&(o=this.tokenizer.url(e))){e=e.substring(o.raw.length),t.push(o);continue}let a=e;if(this.options.extensions?.startInline){let c=1/0,p=e.slice(1),u;this.options.extensions.startInline.forEach(d=>{u=d.call({lexer:this},p),typeof u=="number"&&u>=0&&(c=Math.min(c,u))}),c<1/0&&c>=0&&(a=e.substring(0,c+1))}if(o=this.tokenizer.inlineText(a)){e=e.substring(o.raw.length),o.raw.slice(-1)!=="_"&&(r=o.raw.slice(-1)),i=!0;let c=t.at(-1);c?.type==="text"?(c.raw+=o.raw,c.text+=o.text):t.push(o);continue}if(e){let c="Infinite loop on byte: "+e.charCodeAt(0);if(this.options.silent){console.error(c);break}else throw new Error(c)}}return t}};var $=class{options;parser;constructor(e){this.options=e||w}space(e){return""}code({text:e,lang:t,escaped:n}){let s=(t||"").match(m.notSpaceStart)?.[0],i=e.replace(m.endingNewline,"")+`
`;return s?'<pre><code class="language-'+R(s)+'">'+(n?i:R(i,!0))+`</code></pre>
`:"<pre><code>"+(n?i:R(i,!0))+`</code></pre>
`}blockquote({tokens:e}){return`<blockquote>
${this.parser.parse(e)}</blockquote>
`}html({text:e}){return e}heading({tokens:e,depth:t}){return`<h${t}>${this.parser.parseInline(e)}</h${t}>
`}hr(e){return`<hr>
`}list(e){let t=e.ordered,n=e.start,s="";for(let o=0;o<e.items.length;o++){let a=e.items[o];s+=this.listitem(a)}let i=t?"ol":"ul",r=t&&n!==1?' start="'+n+'"':"";return"<"+i+r+`>
`+s+"</"+i+`>
`}listitem(e){let t="";if(e.task){let n=this.checkbox({checked:!!e.checked});e.loose?e.tokens[0]?.type==="paragraph"?(e.tokens[0].text=n+" "+e.tokens[0].text,e.tokens[0].tokens&&e.tokens[0].tokens.length>0&&e.tokens[0].tokens[0].type==="text"&&(e.tokens[0].tokens[0].text=n+" "+R(e.tokens[0].tokens[0].text),e.tokens[0].tokens[0].escaped=!0)):e.tokens.unshift({type:"text",raw:n+" ",text:n+" ",escaped:!0}):t+=n+" "}return t+=this.parser.parse(e.tokens,!!e.loose),`<li>${t}</li>
`}checkbox({checked:e}){return"<input "+(e?'checked="" ':"")+'disabled="" type="checkbox">'}paragraph({tokens:e}){return`<p>${this.parser.parseInline(e)}</p>
`}table(e){let t="",n="";for(let i=0;i<e.header.length;i++)n+=this.tablecell(e.header[i]);t+=this.tablerow({text:n});let s="";for(let i=0;i<e.rows.length;i++){let r=e.rows[i];n="";for(let o=0;o<r.length;o++)n+=this.tablecell(r[o]);s+=this.tablerow({text:n})}return s&&(s=`<tbody>${s}</tbody>`),`<table>
<thead>
`+t+`</thead>
`+s+`</table>
`}tablerow({text:e}){return`<tr>
${e}</tr>
`}tablecell(e){let t=this.parser.parseInline(e.tokens),n=e.header?"th":"td";return(e.align?`<${n} align="${e.align}">`:`<${n}>`)+t+`</${n}>
`}strong({tokens:e}){return`<strong>${this.parser.parseInline(e)}</strong>`}em({tokens:e}){return`<em>${this.parser.parseInline(e)}</em>`}codespan({text:e}){return`<code>${R(e,!0)}</code>`}br(e){return"<br>"}del({tokens:e}){return`<del>${this.parser.parseInline(e)}</del>`}link({href:e,title:t,tokens:n}){let s=this.parser.parseInline(n),i=V(e);if(i===null)return s;e=i;let r='<a href="'+e+'"';return t&&(r+=' title="'+R(t)+'"'),r+=">"+s+"</a>",r}image({href:e,title:t,text:n,tokens:s}){s&&(n=this.parser.parseInline(s,this.parser.textRenderer));let i=V(e);if(i===null)return R(n);e=i;let r=`<img src="${e}" alt="${n}"`;return t&&(r+=` title="${R(t)}"`),r+=">",r}text(e){return"tokens"in e&&e.tokens?this.parser.parseInline(e.tokens):"escaped"in e&&e.escaped?e.text:R(e.text)}};var _=class{strong({text:e}){return e}em({text:e}){return e}codespan({text:e}){return e}del({text:e}){return e}html({text:e}){return e}text({text:e}){return e}link({text:e}){return""+e}image({text:e}){return""+e}br(){return""}};var b=class l{options;renderer;textRenderer;constructor(e){this.options=e||w,this.options.renderer=this.options.renderer||new $,this.renderer=this.options.renderer,this.renderer.options=this.options,this.renderer.parser=this,this.textRenderer=new _}static parse(e,t){return new l(t).parse(e)}static parseInline(e,t){return new l(t).parseInline(e)}parse(e,t=!0){let n="";for(let s=0;s<e.length;s++){let i=e[s];if(this.options.extensions?.renderers?.[i.type]){let o=i,a=this.options.extensions.renderers[o.type].call({parser:this},o);if(a!==!1||!["space","hr","heading","code","table","blockquote","list","html","paragraph","text"].includes(o.type)){n+=a||"";continue}}let r=i;switch(r.type){case"space":{n+=this.renderer.space(r);continue}case"hr":{n+=this.renderer.hr(r);continue}case"heading":{n+=this.renderer.heading(r);continue}case"code":{n+=this.renderer.code(r);continue}case"table":{n+=this.renderer.table(r);continue}case"blockquote":{n+=this.renderer.blockquote(r);continue}case"list":{n+=this.renderer.list(r);continue}case"html":{n+=this.renderer.html(r);continue}case"paragraph":{n+=this.renderer.paragraph(r);continue}case"text":{let o=r,a=this.renderer.text(o);for(;s+1<e.length&&e[s+1].type==="text";)o=e[++s],a+=`
`+this.renderer.text(o);t?n+=this.renderer.paragraph({type:"paragraph",raw:a,text:a,tokens:[{type:"text",raw:a,text:a,escaped:!0}]}):n+=a;continue}default:{let o='Token with "'+r.type+'" type was not found.';if(this.options.silent)return console.error(o),"";throw new Error(o)}}}return n}parseInline(e,t=this.renderer){let n="";for(let s=0;s<e.length;s++){let i=e[s];if(this.options.extensions?.renderers?.[i.type]){let o=this.options.extensions.renderers[i.type].call({parser:this},i);if(o!==!1||!["escape","html","link","image","strong","em","codespan","br","del","text"].includes(i.type)){n+=o||"";continue}}let r=i;switch(r.type){case"escape":{n+=t.text(r);break}case"html":{n+=t.html(r);break}case"link":{n+=t.link(r);break}case"image":{n+=t.image(r);break}case"strong":{n+=t.strong(r);break}case"em":{n+=t.em(r);break}case"codespan":{n+=t.codespan(r);break}case"br":{n+=t.br(r);break}case"del":{n+=t.del(r);break}case"text":{n+=t.text(r);break}default:{let o='Token with "'+r.type+'" type was not found.';if(this.options.silent)return console.error(o),"";throw new Error(o)}}}return n}};var L=class{options;block;constructor(e){this.options=e||w}static passThroughHooks=new Set(["preprocess","postprocess","processAllTokens"]);preprocess(e){return e}postprocess(e){return e}processAllTokens(e){return e}provideLexer(){return this.block?x.lex:x.lexInline}provideParser(){return this.block?b.parse:b.parseInline}};var E=class{defaults=z();options=this.setOptions;parse=this.parseMarkdown(!0);parseInline=this.parseMarkdown(!1);Parser=b;Renderer=$;TextRenderer=_;Lexer=x;Tokenizer=S;Hooks=L;constructor(...e){this.use(...e)}walkTokens(e,t){let n=[];for(let s of e)switch(n=n.concat(t.call(this,s)),s.type){case"table":{let i=s;for(let r of i.header)n=n.concat(this.walkTokens(r.tokens,t));for(let r of i.rows)for(let o of r)n=n.concat(this.walkTokens(o.tokens,t));break}case"list":{let i=s;n=n.concat(this.walkTokens(i.items,t));break}default:{let i=s;this.defaults.extensions?.childTokens?.[i.type]?this.defaults.extensions.childTokens[i.type].forEach(r=>{let o=i[r].flat(1/0);n=n.concat(this.walkTokens(o,t))}):i.tokens&&(n=n.concat(this.walkTokens(i.tokens,t)))}}return n}use(...e){let t=this.defaults.extensions||{renderers:{},childTokens:{}};return e.forEach(n=>{let s={...n};if(s.async=this.defaults.async||s.async||!1,n.extensions&&(n.extensions.forEach(i=>{if(!i.name)throw new Error("extension name required");if("renderer"in i){let r=t.renderers[i.name];r?t.renderers[i.name]=function(...o){let a=i.renderer.apply(this,o);return a===!1&&(a=r.apply(this,o)),a}:t.renderers[i.name]=i.renderer}if("tokenizer"in i){if(!i.level||i.level!=="block"&&i.level!=="inline")throw new Error("extension level must be 'block' or 'inline'");let r=t[i.level];r?r.unshift(i.tokenizer):t[i.level]=[i.tokenizer],i.start&&(i.level==="block"?t.startBlock?t.startBlock.push(i.start):t.startBlock=[i.start]:i.level==="inline"&&(t.startInline?t.startInline.push(i.start):t.startInline=[i.start]))}"childTokens"in i&&i.childTokens&&(t.childTokens[i.name]=i.childTokens)}),s.extensions=t),n.renderer){let i=this.defaults.renderer||new $(this.defaults);for(let r in n.renderer){if(!(r in i))throw new Error(`renderer '${r}' does not exist`);if(["options","parser"].includes(r))continue;let o=r,a=n.renderer[o],c=i[o];i[o]=(...p)=>{let u=a.apply(i,p);return u===!1&&(u=c.apply(i,p)),u||""}}s.renderer=i}if(n.tokenizer){let i=this.defaults.tokenizer||new S(this.defaults);for(let r in n.tokenizer){if(!(r in i))throw new Error(`tokenizer '${r}' does not exist`);if(["options","rules","lexer"].includes(r))continue;let o=r,a=n.tokenizer[o],c=i[o];i[o]=(...p)=>{let u=a.apply(i,p);return u===!1&&(u=c.apply(i,p)),u}}s.tokenizer=i}if(n.hooks){let i=this.defaults.hooks||new L;for(let r in n.hooks){if(!(r in i))throw new Error(`hook '${r}' does not exist`);if(["options","block"].includes(r))continue;let o=r,a=n.hooks[o],c=i[o];L.passThroughHooks.has(r)?i[o]=p=>{if(this.defaults.async)return Promise.resolve(a.call(i,p)).then(d=>c.call(i,d));let u=a.call(i,p);return c.call(i,u)}:i[o]=(...p)=>{let u=a.apply(i,p);return u===!1&&(u=c.apply(i,p)),u}}s.hooks=i}if(n.walkTokens){let i=this.defaults.walkTokens,r=n.walkTokens;s.walkTokens=function(o){let a=[];return a.push(r.call(this,o)),i&&(a=a.concat(i.call(this,o))),a}}this.defaults={...this.defaults,...s}}),this}setOptions(e){return this.defaults={...this.defaults,...e},this}lexer(e,t){return x.lex(e,t??this.defaults)}parser(e,t){return b.parse(e,t??this.defaults)}parseMarkdown(e){return(n,s)=>{let i={...s},r={...this.defaults,...i},o=this.onError(!!r.silent,!!r.async);if(this.defaults.async===!0&&i.async===!1)return o(new Error("marked(): The async option was set to true by an extension. Remove async: false from the parse options object to return a Promise."));if(typeof n>"u"||n===null)return o(new Error("marked(): input parameter is undefined or null"));if(typeof n!="string")return o(new Error("marked(): input parameter is of type "+Object.prototype.toString.call(n)+", string expected"));r.hooks&&(r.hooks.options=r,r.hooks.block=e);let a=r.hooks?r.hooks.provideLexer():e?x.lex:x.lexInline,c=r.hooks?r.hooks.provideParser():e?b.parse:b.parseInline;if(r.async)return Promise.resolve(r.hooks?r.hooks.preprocess(n):n).then(p=>a(p,r)).then(p=>r.hooks?r.hooks.processAllTokens(p):p).then(p=>r.walkTokens?Promise.all(this.walkTokens(p,r.walkTokens)).then(()=>p):p).then(p=>c(p,r)).then(p=>r.hooks?r.hooks.postprocess(p):p).catch(o);try{r.hooks&&(n=r.hooks.preprocess(n));let p=a(n,r);r.hooks&&(p=r.hooks.processAllTokens(p)),r.walkTokens&&this.walkTokens(p,r.walkTokens);let u=c(p,r);return r.hooks&&(u=r.hooks.postprocess(u)),u}catch(p){return o(p)}}}onError(e,t){return n=>{if(n.message+=`
Please report this to https://github.com/markedjs/marked.`,e){let s="<p>An error occurred:</p><pre>"+R(n.message+"",!0)+"</pre>";return t?Promise.resolve(s):s}if(t)return Promise.reject(n);throw n}}};var M=new E;function k(l,e){return M.parse(l,e)}k.options=k.setOptions=function(l){return M.setOptions(l),k.defaults=M.defaults,N(k.defaults),k};k.getDefaults=z;k.defaults=w;k.use=function(...l){return M.use(...l),k.defaults=M.defaults,N(k.defaults),k};k.walkTokens=function(l,e){return M.walkTokens(l,e)};k.parseInline=M.parseInline;k.Parser=b;k.parser=b.parse;k.Renderer=$;k.TextRenderer=_;k.Lexer=x;k.lexer=x.lex;k.Tokenizer=S;k.Hooks=L;k.parse=k;var it=k.options,ot=k.setOptions,lt=k.use,at=k.walkTokens,ct=k.parseInline,pt=k,ut=b.parse,ht=x.lex;

if(__exports != exports)module.exports = exports;return module.exports}));

  </script>

  <style>
    /* ── Reset & base ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /*
     * CSS custom properties (design tokens) are defined here on :root so that
     * colours and radii can be updated in one place if the theme changes.
     * This avoids "magic numbers" scattered throughout the stylesheet.
     */
    :root {
      --bg:       #0f1117;   /* page background — darkest layer           */
      --surface:  #1a1d27;   /* card / panel background — one step up     */
      --border:   #2e3145;   /* subtle borders between UI regions         */
      --accent:   #6c63ff;   /* primary brand / interactive colour        */
      --accent2:  #a78bfa;   /* lighter accent used for chips & links     */
      --text:     #e2e8f0;   /* primary readable text                     */
      --muted:    #64748b;   /* secondary / helper text                   */
      --success:  #22d3a5;   /* positive feedback (copy confirmed, stats) */
      --danger:   #f87171;   /* error state text and borders              */
      --radius:   12px;      /* consistent corner rounding across cards   */
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 20px 60px;
    }

    header {
      text-align: center;
      margin-bottom: 36px;
      position: relative;
    }
    #quit-btn {
      position: absolute;
      top: 0;
      right: 0;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--muted);
      border-radius: 6px;
      padding: 6px 14px;
      font-size: 0.85rem;
      cursor: pointer;
    }
    #quit-btn:hover { border-color: #e05555; color: #e05555; }
    header h1 {
      font-size: 2rem;
      font-weight: 700;
      /* Gradient text: browser clips the gradient to the text shape */
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    header p {
      color: var(--muted);
      margin-top: 6px;
      font-size: 0.95rem;
    }
    #version {
      font-size: 0.75rem;
      margin-top: 4px;
      opacity: 0.45;
    }

    /* ── Shared card wrapper ── */
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 28px;
      width: 100%;
      max-width: 820px;
    }

    /* ── Drop Zone ──
     * The native <input type="file"> is absolutely positioned over the entire
     * zone and set to opacity:0 so the styled div acts as the visual target
     * while still triggering the native file-picker on click.
     */
    #drop-zone {
      border: 2px dashed var(--border);
      border-radius: var(--radius);
      padding: 48px 24px;
      text-align: center;
      cursor: pointer;
      transition: border-color .2s, background .2s;
      position: relative;
    }
    #drop-zone.drag-over {
      /* Visual feedback while a file is dragged over the zone */
      border-color: var(--accent);
      background: rgba(108,99,255,.07);
    }
    #drop-zone input[type=file] {
      position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; height: 100%;
    }
    #drop-zone .icon { font-size: 2.8rem; margin-bottom: 12px; display: block; }
    #drop-zone h2   { font-size: 1.1rem; font-weight: 600; margin-bottom: 6px; }
    #drop-zone p    { font-size: 0.85rem; color: var(--muted); }

    /* ── Format chips ──
     * Purely informational — they show the user which file types are supported
     * without cluttering the UI with a long text list.
     */
    .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 22px; }
    #size-limit-note { font-size: 0.75rem; color: var(--muted); margin-top: 10px; opacity: 0.6; }
    .chip {
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: .04em;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(108,99,255,.15);
      color: var(--accent2);
      border: 1px solid rgba(108,99,255,.3);
    }

    /* ── Selected-file bar ──
     * Displayed only after the user picks a file; gives confirmation of the
     * chosen filename and size before the user clicks Convert.
     */
    #file-bar {
      display: none; /* hidden until a file is selected via selectFile() */
      align-items: center;
      gap: 12px;
      margin-top: 18px;
      background: rgba(255,255,255,.04);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 0.9rem;
    }
    #file-bar .fname { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    #file-bar .fsize { color: var(--muted); font-size: 0.8rem; white-space: nowrap; }

    /* ── Primary Convert button ──
     * Disabled by default; enabled only once a file is staged.
     * This prevents accidental empty-submission API calls.
     */
    #convert-btn {
      width: 100%;
      margin-top: 20px;
      padding: 13px;
      background: linear-gradient(135deg, var(--accent), #8b5cf6);
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: opacity .2s, transform .1s;
      display: flex; align-items: center; justify-content: center; gap: 8px;
    }
    #convert-btn:disabled { opacity: .5; cursor: not-allowed; }
    #convert-btn:not(:disabled):hover  { opacity: .88; }
    #convert-btn:not(:disabled):active { transform: scale(.98); }

    /* ── Inline spinner ──
     * CSS-only animation injected into the button during async conversion
     * so the user knows work is in progress without a full-page loading state.
     */
    .spinner {
      width: 18px; height: 18px;
      border: 2px solid rgba(255,255,255,.3);
      border-top-color: #fff;
      border-radius: 50%;
      animation: spin .7s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* ── Error box ──
     * Shown only when the /convert or /convert-url endpoint returns an error.
     * white-space:pre-wrap preserves the Python traceback formatting.
     */
    #error-box {
      display: none; /* toggled by showError() / hideError() */
      margin-top: 16px;
      padding: 12px 16px;
      background: rgba(248,113,113,.1);
      border: 1px solid rgba(248,113,113,.4);
      border-radius: 8px;
      color: var(--danger);
      font-size: 0.88rem;
      white-space: pre-wrap;
      word-break: break-word;
    }

    /* ── Output section ──
     * Hidden on page load; revealed by showOutput() after a successful conversion.
     * Keeping it in the DOM (display:none rather than removed) avoids re-rendering
     * cost if the user switches tabs multiple times.
     */
    #output-section {
      display: none;
      margin-top: 32px;
      width: 100%;
      max-width: 820px;
    }

    .output-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 10px;
    }
    .output-header h3 { font-size: 1rem; font-weight: 600; }

    /* ── Raw / Preview tabs ──
     * Simple two-state toggle. The active class drives the filled style;
     * switchTab() handles mutual exclusivity in JS.
     */
    .tabs { display: flex; gap: 4px; }
    .tab-btn {
      padding: 6px 16px;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--muted);
      font-size: 0.85rem;
      cursor: pointer;
      transition: background .15s, color .15s;
    }
    .tab-btn.active {
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }

    /* ── Action buttons (Copy / Download) ── */
    .actions { display: flex; gap: 8px; }
    .action-btn {
      padding: 6px 14px;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
      font-size: 0.82rem;
      cursor: pointer;
      transition: background .15s, border-color .15s;
      display: flex; align-items: center; gap: 5px;
    }
    .action-btn:hover  { background: rgba(255,255,255,.06); border-color: var(--accent); }
    .action-btn.copied { color: var(--success); border-color: var(--success); }

    /* ── Raw Markdown pane ──
     * Uses a monospace font stack to ensure consistent column widths; this
     * matters when the output contains ASCII tables from MarkItDown.
     */
    #raw-pane {
      background: #0d0f18;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
      overflow: auto;
      max-height: 600px;
      font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace;
      font-size: 0.82rem;
      line-height: 1.65;
      color: #c9d1d9;
      white-space: pre-wrap;
      word-break: break-word;
    }

    /* ── Preview pane ──
     * Receives innerHTML from marked.parse(); hidden by default — shown only
     * when the Preview tab is active. Scoped styles below prevent MarkItDown
     * output from disrupting the rest of the page layout.
     */
    #preview-pane {
      display: none;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 28px 32px;
      overflow: auto;
      max-height: 600px;
      line-height: 1.75;
      font-size: 0.95rem;
    }

    /* Scoped Markdown rendering styles — these only apply inside #preview-pane */
    #preview-pane h1,#preview-pane h2,#preview-pane h3,
    #preview-pane h4,#preview-pane h5,#preview-pane h6 {
      margin: 1.2em 0 .5em; font-weight: 700; line-height: 1.3;
    }
    #preview-pane h1 { font-size: 1.7em; border-bottom: 1px solid var(--border); padding-bottom: .3em; }
    #preview-pane h2 { font-size: 1.35em; border-bottom: 1px solid var(--border); padding-bottom: .2em; }
    #preview-pane p  { margin: .7em 0; }
    #preview-pane a  { color: var(--accent2); }
    #preview-pane code {
      background: rgba(255,255,255,.07); padding: 2px 6px;
      border-radius: 4px; font-family: monospace; font-size: .88em;
    }
    #preview-pane pre {
      background: #0d0f18; border: 1px solid var(--border);
      border-radius: 8px; padding: 14px 18px; overflow: auto;
    }
    #preview-pane pre code { background: none; padding: 0; }
    #preview-pane table {
      border-collapse: collapse; width: 100%; margin: 1em 0; font-size: .9em;
    }
    #preview-pane th, #preview-pane td { border: 1px solid var(--border); padding: 7px 12px; }
    #preview-pane th { background: rgba(255,255,255,.05); font-weight: 600; }
    #preview-pane ul, #preview-pane ol { padding-left: 1.5em; margin: .6em 0; }
    #preview-pane li { margin: .3em 0; }
    #preview-pane blockquote {
      border-left: 3px solid var(--accent); margin: .8em 0;
      padding: .4em 1em; color: var(--muted);
    }
    #preview-pane hr  { border: none; border-top: 1px solid var(--border); margin: 1.5em 0; }
    #preview-pane img { max-width: 100%; border-radius: 6px; }

    /* ── Reset link ──
     * Rendered as a plain text link rather than a button to visually
     * de-emphasise it — it's a secondary action that clears the entire session.
     */
    #reset-btn {
      display: block;
      margin: 20px auto 0;
      background: none;
      border: none;
      color: var(--muted);
      font-size: 0.85rem;
      cursor: pointer;
      text-decoration: underline;
      text-underline-offset: 3px;
    }
    #reset-btn:hover { color: var(--text); }

    /* ── Stats bar ──
     * Quick at-a-glance metrics (chars / words / lines / token estimate) after conversion.
     * Token range uses chars/4 (low, GPT-4/Claude density) to chars/3 (high, code/multilingual density).
     * Helps users gauge document size before deciding how to use the output.
     */
    #stats-bar { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 14px; }
    .stat { font-size: 0.8rem; color: var(--muted); }
    .stat span { color: var(--success); font-weight: 600; }
  </style>
</head>
<body>

<header>
  <button id="quit-btn" onclick="quitApp()">Quit</button>
  <h1>⚡ MarkItDown</h1>
  <p>Convert documents, PDFs, Office files &amp; more to Markdown — locally.</p>
  <p id="version">v0.42.1</p>
</header>

<!-- ═══════════════════════════════════════════════════
     FILE UPLOAD CARD
     Contains: drop zone, format chips, selected-file bar,
               convert button, and error display.
     ═══════════════════════════════════════════════════ -->
<div class="card" id="upload-card">

  <!-- Drop zone: the invisible <input> captures both click-to-browse and
       native drag-and-drop events; the styled div is purely presentational. -->
  <div id="drop-zone">
    <input type="file" id="file-input" />
    <span class="icon">📄</span>
    <h2>Drop a file here</h2>
    <p>or click to browse</p>
  </div>

  <!-- Supported format chips — informational only, not interactive -->
  <div class="chips">
    <span class="chip">.pdf</span><span class="chip">.docx</span><span class="chip">.pptx</span>
    <span class="chip">.xlsx</span><span class="chip">.xls</span><span class="chip">.html</span>
    <span class="chip">.csv</span><span class="chip">.json</span><span class="chip">.xml</span>
    <span class="chip">.epub</span><span class="chip">.zip</span><span class="chip">.jpg/png</span>
    <span class="chip">.wav/mp3</span><span class="chip">YouTube URL</span>
  </div>
  <p id="size-limit-note">Max file size: 100 MB</p>

  <!-- Shown once a file is chosen, confirming the filename and size -->
  <div id="file-bar">
    <span>📎</span>
    <span class="fname" id="fname-label"></span>
    <span class="fsize" id="fsize-label"></span>
  </div>

  <!-- Disabled until selectFile() stages a file; prevents empty submissions -->
  <button id="convert-btn" disabled>Convert to Markdown</button>

  <!-- Error messages from the backend are injected here as plain text -->
  <div id="error-box"></div>
</div>

<!-- ═══════════════════════════════════════════════════
     URL CONVERSION CARD
     Separate from the file upload card so both input
     methods are independently usable at the same time.
     Supports YouTube links, web pages, and any URL that
     MarkItDown's convert() method accepts.
     ═══════════════════════════════════════════════════ -->
<div class="card" style="margin-top:16px; max-width:820px; width:100%;">
  <div style="display:flex; gap:10px; align-items:center;">
    <input id="url-input" type="url" placeholder="Or paste a URL (YouTube, web page…)"
      style="flex:1; background:#0d0f18; border:1px solid var(--border); color:var(--text);
             border-radius:8px; padding:10px 14px; font-size:0.9rem; outline:none;" />
    <button id="url-btn"
      style="padding:10px 20px; background:linear-gradient(135deg,var(--accent),#8b5cf6);
             color:#fff; border:none; border-radius:8px; font-size:0.9rem; font-weight:600;
             cursor:pointer; white-space:nowrap;">
      Convert URL
    </button>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════
     OUTPUT SECTION
     Hidden on page load; revealed after a successful
     conversion. Contains: stats bar, Raw/Preview tabs,
     Copy/Download actions, and a Reset link.
     ═══════════════════════════════════════════════════ -->
<div id="output-section">
  <div class="output-header">
    <div>
      <h3>Result</h3>
      <!-- Stats are populated dynamically by showOutput() -->
      <div id="stats-bar" style="margin-top:6px;"></div>
    </div>
    <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
      <!-- Tab buttons call switchTab() to toggle pane visibility -->
      <div class="tabs">
        <button class="tab-btn active" id="tab-raw"     onclick="switchTab('raw')">Raw</button>
        <button class="tab-btn"        id="tab-preview" onclick="switchTab('preview')">Preview</button>
      </div>
      <div class="actions">
        <button class="action-btn" id="copy-btn"     onclick="copyMarkdown()">📋 Copy</button>
        <button class="action-btn" id="download-btn" onclick="downloadMarkdown()">⬇ Download</button>
      </div>
    </div>
  </div>

  <!-- Raw pane: plain text, shown by default after conversion -->
  <div id="raw-pane"></div>

  <!-- Preview pane: rendered HTML from marked.parse(); hidden until tab is switched -->
  <div id="preview-pane"></div>

  <!-- Secondary action — clears everything so the user can start a new conversion -->
  <button id="reset-btn" onclick="resetAll()">↩ Convert another file</button>
</div>

<!-- ═══════════════════════════════════════════════════
     JAVASCRIPT
     All interactivity is self-contained here.
     Key responsibilities:
       - Drag-and-drop and click-to-browse file staging
       - Async POST to /convert (file) and /convert-url (URL)
       - Spinner and disabled-state management during requests
       - Output rendering, tab switching, copy, download, reset
     ═══════════════════════════════════════════════════ -->
<script>
  // Module-level state: the converted Markdown string and the base filename
  // used when generating the .md download. Both are reset by resetAll().
  let currentMarkdown = "";
  let currentFilename = "output";

  // Cache DOM references at startup to avoid repeated querySelector calls
  // on every user interaction.
  const dropZone      = document.getElementById("drop-zone");
  const fileInput     = document.getElementById("file-input");
  const fileBar       = document.getElementById("file-bar");
  const fnameLabel    = document.getElementById("fname-label");
  const fsizeLabel    = document.getElementById("fsize-label");
  const convertBtn    = document.getElementById("convert-btn");
  const errorBox      = document.getElementById("error-box");
  const outputSection = document.getElementById("output-section");
  const rawPane       = document.getElementById("raw-pane");
  const previewPane   = document.getElementById("preview-pane");
  const statsBar      = document.getElementById("stats-bar");

  // ── Drag-and-drop event handlers ──────────────────────────────────────────
  // preventDefault on dragover is required; without it the browser handles the
  // drop itself (e.g. opening the file), which we do not want.
  dropZone.addEventListener("dragover", e => {
    e.preventDefault();
    dropZone.classList.add("drag-over"); // visual highlight while hovering
  });
  dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
  dropZone.addEventListener("drop", e => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    const f = e.dataTransfer.files[0]; // only handle the first dropped file
    if (f) selectFile(f);
  });

  // ── Native file-input change handler ──────────────────────────────────────
  // Fires when the user picks a file through the click-to-browse dialog.
  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) selectFile(fileInput.files[0]);
  });

  /**
   * Stages a File object for conversion.
   * Updates the filename/size bar, enables the Convert button, and attaches
   * the File to the button element so the click handler can read it later.
   * We store the file on the button (convertBtn._file) rather than in a
   * separate variable to keep the staging state co-located with the action.
   *
   * @param {File} f - The File object chosen by the user.
   */
  function selectFile(f) {
    fnameLabel.textContent = f.name;
    fsizeLabel.textContent = formatBytes(f.size);
    fileBar.style.display  = "flex";
    convertBtn.disabled    = false;
    hideError();
    // Strip the file extension to use as the default download filename
    currentFilename = f.name.replace(/\.[^.]+$/, "");
    convertBtn._file = f;
  }

  /**
   * Converts a raw byte count into a human-readable string (B / KB / MB).
   * Used exclusively in the selected-file bar to give size context.
   *
   * @param  {number} b - File size in bytes.
   * @returns {string}   Human-readable size string.
   */
  function formatBytes(b) {
    if (b < 1024)      return b + " B";
    if (b < 1024 ** 2) return (b / 1024).toFixed(1) + " KB";
    return (b / 1024 ** 2).toFixed(1) + " MB";
  }

  // ── File convert button click ──────────────────────────────────────────────
  // Wraps the file in FormData and delegates to the shared doConvert() helper.
  convertBtn.addEventListener("click", async () => {
    const f = convertBtn._file;
    if (!f) return; // guard: should never happen since button is disabled without a file
    await doConvert(async () => {
      const fd = new FormData();
      fd.append("file", f);
      return await fetch("/convert", { method: "POST", body: fd });
    });
  });

  // ── URL convert button click ───────────────────────────────────────────────
  // Sends the URL as JSON to /convert-url and delegates to doConvert().
  document.getElementById("url-btn").addEventListener("click", async () => {
    const url = document.getElementById("url-input").value.trim();
    if (!url) return;
    currentFilename = "converted"; // no meaningful filename for URLs
    await doConvert(async () => {
      return await fetch("/convert-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });
    });
  });

  /**
   * Shared conversion orchestrator used by both file and URL workflows.
   * Handles spinner/button state, calls the provided fetch function,
   * and routes the result to showOutput() or showError().
   *
   * Accepting a fetchFn callback (rather than duplicating try/catch in each
   * handler) keeps error handling and UI state transitions in one place.
   *
   * @param {Function} fetchFn - Async function that returns a fetch Response.
   */
  async function doConvert(fetchFn) {
    // Disable both conversion triggers while a request is in flight to
    // prevent duplicate submissions.
    convertBtn.disabled = true;
    document.getElementById("url-btn").disabled = true;
    convertBtn.innerHTML = '<div class="spinner"></div> Converting…';
    hideError();

    try {
      const res  = await fetchFn();
      const data = await res.json();
      // Surface backend errors (non-2xx status or explicit error field)
      if (!res.ok || data.error) throw new Error(data.error || "Conversion failed.");
      showOutput(data.markdown);
    } catch (err) {
      showError(err.message);
    } finally {
      // Always restore button state, even if the request failed
      convertBtn.innerHTML = "Convert to Markdown";
      convertBtn.disabled  = false;
      document.getElementById("url-btn").disabled = false;
    }
  }

  /**
   * Populates the output section with the converted Markdown.
   * - Sets rawPane as plain text (safe: no HTML injection)
   * - Renders previewPane via marked.parse() for the Preview tab
   * - Computes and displays basic document statistics
   * - Scrolls the output into view so the user doesn't have to scroll manually
   *
   * @param {string} md - The Markdown string returned by the backend.
   */
  function showOutput(md) {
    currentMarkdown = md;

    // textContent prevents any accidental HTML injection in the raw view
    rawPane.textContent = md;

    // marked.parse() converts Markdown to an HTML string; assigned via
    // innerHTML since we trust MarkItDown's output (local conversion only)
    previewPane.innerHTML = marked.parse(md);

    outputSection.style.display = "block";
    outputSection.scrollIntoView({ behavior: "smooth", block: "start" });

    // Compute document statistics for the stats bar
    const words = md.trim().split(/\s+/).filter(Boolean).length;
    const lines = md.split("\n").length;
    const chars = md.length;
    const tokLow  = Math.round(chars / 4).toLocaleString();
    const tokHigh = Math.round(chars / 3).toLocaleString();
    statsBar.innerHTML =
      `<div class="stat"><span>${chars.toLocaleString()}</span> chars</div>` +
      `<div class="stat"><span>${words.toLocaleString()}</span> words</div>` +
      `<div class="stat"><span>${lines.toLocaleString()}</span> lines</div>` +
      `<div class="stat"><span>~${tokLow}–${tokHigh}</span> tokens</div>`;
  }

  /**
   * Switches between the Raw and Preview output tabs.
   * Toggles the .active class on tab buttons and shows/hides panes.
   * Uses display:block/none rather than visibility to prevent the hidden
   * pane from occupying space in the layout.
   *
   * @param {'raw'|'preview'} t - The tab to activate.
   */
  function switchTab(t) {
    document.getElementById("tab-raw").classList.toggle("active", t === "raw");
    document.getElementById("tab-preview").classList.toggle("active", t === "preview");
    rawPane.style.display     = t === "raw"     ? "block" : "none";
    previewPane.style.display = t === "preview" ? "block" : "none";
  }

  /**
   * Copies the current Markdown to the clipboard using the async Clipboard API.
   * Provides temporary visual feedback ("✅ Copied!") that auto-resets after 2 s,
   * so the user knows the action succeeded without a persistent UI change.
   */
  async function copyMarkdown() {
    await navigator.clipboard.writeText(currentMarkdown);
    const btn = document.getElementById("copy-btn");
    btn.textContent = "✅ Copied!";
    btn.classList.add("copied");
    setTimeout(() => { btn.textContent = "📋 Copy"; btn.classList.remove("copied"); }, 2000);
  }

  /**
   * Triggers a browser file download of the current Markdown as a .md file.
   * Uses a temporary Object URL to avoid storing the content in localStorage
   * or making a round-trip to the server. The URL is revoked immediately after
   * the click to free memory.
   */
  function downloadMarkdown() {
    const blob = new Blob([currentMarkdown], { type: "text/markdown" });
    const a    = document.createElement("a");
    a.href     = URL.createObjectURL(blob);
    a.download = currentFilename + ".md";
    a.click();
    URL.revokeObjectURL(a.href); // release the blob URL from memory
  }

  /**
   * Resets the entire UI to its initial state.
   * Called when the user clicks "↩ Convert another file".
   * Clears all staged data, hides the output section, and scrolls back to top.
   */
  function resetAll() {
    currentMarkdown = "";
    outputSection.style.display = "none";
    fileBar.style.display       = "none";
    fileInput.value             = ""; // clearing value allows re-selecting the same file
    convertBtn.disabled         = true;
    convertBtn._file            = null;
    document.getElementById("url-input").value = "";
    hideError();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // ── Error display helpers ─────────────────────────────────────────────────
  // Centralised so that every code path uses the same show/hide mechanism
  // rather than touching errorBox.style.display directly.

  /** Displays an error message in the error box. */
  function showError(msg) {
    errorBox.textContent   = "⚠ " + msg;
    errorBox.style.display = "block";
  }

  /** Hides and clears the error box. */
  function hideError() {
    errorBox.style.display = "none";
  }

  /** Sends a shutdown request to the server then closes the tab. */
  function quitApp() {
    // Stop the heartbeat so the watchdog doesn't fire before the quit response
    clearInterval(heartbeatTimer);
    fetch("/quit", { method: "POST" }).finally(() => {
      // Redirect to the stopped page — works even when window.close() is blocked
      window.location.href = "/stopped";
    });
  }

  // ── Heartbeat ─────────────────────────────────────────────────────────────
  // Pings the server every 5 s so the watchdog knows the tab is still open.
  // When the tab is closed the pings stop; the watchdog shuts the server down
  // after a 12 s timeout (2× the interval + grace period).
  const heartbeatTimer = setInterval(() => {
    fetch("/heartbeat", { method: "POST" }).catch(() => {});
  }, 5000);
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the single-page frontend UI."""
    return render_template_string(HTML)


@app.route("/convert", methods=["POST"])
def convert_file():
    """
    Accept a multipart file upload and convert it to Markdown via MarkItDown.

    The file is read into an in-memory BytesIO stream rather than saved to
    disk. This avoids temporary file cleanup, reduces I/O, and ensures the
    app works in read-only environments (e.g. containers).

    We attach the original filename to the stream object because MarkItDown's
    convert_stream() inspects the .name attribute to determine the file type
    when no explicit extension is provided.

    Returns JSON:
        { "markdown": "<converted text>" }   on success  (HTTP 200)
        { "error":    "<traceback>" }         on failure  (HTTP 500)
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "No file selected."}), 400

    try:
        file_bytes = f.read()
        stream = io.BytesIO(file_bytes)

        # MarkItDown uses the stream's .name attribute for MIME type detection
        # when the file extension is not passed separately.
        stream.name = f.filename

        # Pass the file extension explicitly as a secondary hint; useful when
        # the filename contains dots (e.g. "report.final.docx").
        result = md_converter.convert_stream(
            stream,
            file_extension=os.path.splitext(f.filename)[1]
        )
        return jsonify({"markdown": result.text_content})

    except Exception:
        # Return the full Python traceback so the frontend can display it and
        # the user can diagnose unsupported file types or dependency issues.
        return jsonify({"error": traceback.format_exc()}), 500


@app.route("/convert-url", methods=["POST"])
def convert_url():
    """
    Accept a JSON body containing a URL and convert the target resource to
    Markdown via MarkItDown's convert() method.

    MarkItDown handles URL fetching internally, including special cases such
    as YouTube transcripts and standard web pages. No local file is created.

    Expected request body:
        { "url": "https://..." }

    Returns JSON:
        { "markdown": "<converted text>" }   on success  (HTTP 200)
        { "error":    "<traceback>" }         on failure  (HTTP 500)
    """
    data = request.get_json(silent=True) or {}
    url  = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "No URL provided."}), 400

    try:
        result = md_converter.convert(url)
        return jsonify({"markdown": result.text_content})
    except Exception:
        return jsonify({"error": traceback.format_exc()}), 500


@app.route("/quit", methods=["POST"])
def quit_app():
    """Shut down the Flask server gracefully. Called by the Quit button in the UI."""
    def _shutdown():
        import time
        time.sleep(0.3)   # brief delay so the HTTP response reaches the browser
        os._exit(0)
    threading.Thread(target=_shutdown, daemon=True).start()
    return jsonify({"status": "bye"})


@app.route("/stopped")
def stopped():
    """Shown after the server has received a quit request and the browser redirects here."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>MarkItDown stopped</title>
  <style>
    body { background:#0f0f13; color:#a0a0b0; font-family: system-ui, sans-serif;
           display:flex; align-items:center; justify-content:center; height:100vh; margin:0; }
    p { font-size:1rem; opacity:.7; }
  </style>
</head>
<body><p>MarkItDown has stopped. You can close this tab.</p></body>
</html>"""


# Timestamp of the most recent heartbeat from the browser tab.
_last_heartbeat = None


@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    """Receives a periodic ping from the browser tab. Resets the watchdog timer."""
    global _last_heartbeat
    _last_heartbeat = time.monotonic()
    return jsonify({"status": "ok"})


def _watchdog():
    """Background thread: shuts the server down if no heartbeat arrives within 12 s.

    The browser sends a heartbeat every 5 s. 12 s gives two missed pings plus a
    grace period, covering page reloads and brief network hiccups without
    triggering a false shutdown.
    """
    import time as _time
    # Wait for the first heartbeat before starting to enforce the timeout,
    # so a slow browser open doesn't trigger a premature shutdown.
    while _last_heartbeat is None:
        _time.sleep(1)
    while True:
        _time.sleep(3)
        if _time.monotonic() - _last_heartbeat > 12:
            os._exit(0)
            break


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = 5001

    # Open the browser automatically after a short delay, giving Flask time
    # to start before the browser tries to connect. The delay is run in a
    # background thread so it doesn't block the server from starting.
    def open_browser():
        import time
        time.sleep(1.2)
        webbrowser.open(f"http://127.0.0.1:{port}")

    threading.Thread(target=open_browser, daemon=True).start()
    threading.Thread(target=_watchdog, daemon=True).start()

    # debug=False is required when packaging as a Mac app — debug mode uses
    # a reloader that spawns a second process, which breaks PyInstaller bundles.
    # host='0.0.0.0' ensures Flask accepts connections on both IPv4 and IPv6
    # loopback addresses (127.0.0.1 and ::1), preventing "Failed to fetch" errors
    # on macOS Sequoia where localhost may resolve to ::1.
    try:
        app.run(debug=False, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        pass