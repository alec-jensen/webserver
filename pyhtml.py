def _attr_str(attr: dict):
    return " ".join([f'{key}="{value}"' for key, value in attr.items()])

def html(*content, attr={}, meta=''):
    return f"<!DOCTYPE html><html {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</html>"

def base(attr={}, meta=''):
    return f"<base {_attr_str(attr)} {meta}>"

def head(*content, attr={}, meta=''):
    return f"<head {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</head>"

def link(attr={}, meta=''):
    return f"<link {_attr_str(attr)} {meta}>"

def meta(attr={}, meta=''):
    return f"<meta {_attr_str(attr)} {meta}>"

def style(*content, attr={}, meta=''):
    return f"<style {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</style>"

def title(*content, attr={}, meta=''):
    return f"<title {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</title>"

def body(*content, attr={}, meta=''):
    return f"<body {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</body>"

def address(*content, attr={}, meta=''):
    return f"<address {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</address>"

def article(*content, attr={}, meta=''):
    return f"<article {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</article>"

def aside(*content, attr={}, meta=''):
    return f"<aside {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</aside>"

def footer(*content, attr={}, meta=''):
    return f"<footer {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</footer>"

def header(*content, attr={}, meta=''):
    return f"<header {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</header>"

def h1(*content, attr={}, meta=''):
    return f"<h1 {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</h1>"

def h2(*content, attr={}, meta=''):
    return f"<h2 {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</h2>"

def h3(*content, attr={}, meta=''):
    return f"<h3 {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</h3>"

def h4(*content, attr={}, meta=''):
    return f"<h4 {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</h4>"

def h5(*content, attr={}, meta=''):
    return f"<h5 {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</h5>"

def h6(*content, attr={}, meta=''):
    return f"<h6 {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</h6>"

def hgroup(*content, attr={}, meta=''):
    return f"<hgroup {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</hgroup>"

def main(*content, attr={}, meta=''):
    return f"<main {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</main>"

def nav(*content, attr={}, meta=''):
    return f"<nav {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</nav>"

def section(*content, attr={}, meta=''):
    return f"<section {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</section>"

def search(*content, attr={}, meta=''):
    return f"<search {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</search>"

def blockquote(*content, attr={}, meta=''):
    return f"<blockquote {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</blockquote>"

def dd(*content, attr={}, meta=''):
    return f"<dd {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</dd>"

def div(*content, attr={}, meta=''):
    return f"<div {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</div>"

def dl(*content, attr={}, meta=''):
    return f"<dl {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</dl>"

def dt(*content, attr={}, meta=''):
    return f"<dt {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</dt>"

def figcaption(*content, attr={}, meta=''):
    return f"<figcaption {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</figcaption>"

def figure(*content, attr={}, meta=''):
    return f"<figure {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</figure>"

def hr(*content, attr={}, meta=''):
    return f"<hr {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</hr>"

def li(*content, attr={}, meta=''):
    return f"<li {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</li>"

def menu(*content, attr={}, meta=''):
    return f"<menu {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</menu>"

def ol(*content, attr={}, meta=''):
    return f"<ol {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</ol>"

def p(*content, attr={}, meta=''):
    return f"<p {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</p>"

def pre(*content, attr={}, meta=''):
    return f"<pre {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</pre>"

def ul(*content, attr={}, meta=''):
    return f"<ul {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</ul>"

def a(*content, attr={}, meta=''):
    return f"<a {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</a>"

def abbr(*content, attr={}, meta=''):
    return f"<abbr {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</abbr>"

def b(*content, attr={}, meta=''):
    return f"<b {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</b>"

def bdi(*content, attr={}, meta=''):
    return f"<bdi {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</bdi>"

def bdo(*content, attr={}, meta=''):
    return f"<bdo {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</bdo>"

def br(*content, attr={}, meta=''):
    return f"<br {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</br>"

def cite(*content, attr={}, meta=''):
    return f"<cite {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</cite>"

def code(*content, attr={}, meta=''):
    return f"<code {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</code>"

def data(*content, attr={}, meta=''):
    return f"<data {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</data>"

def dfn(*content, attr={}, meta=''):
    return f"<dfn {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</dfn>"

def em(*content, attr={}, meta=''):
    return f"<em {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</em>"

def i(*content, attr={}, meta=''):
    return f"<i {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</i>"

def kbd(*content, attr={}, meta=''):
    return f"<kbd {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</kbd>"

def mark(*content, attr={}, meta=''):
    return f"<mark {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</mark>"

def q(*content, attr={}, meta=''):
    return f"<q {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</q>"

def rp(*content, attr={}, meta=''):
    return f"<rp {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</rp>"

def rt(*content, attr={}, meta=''):
    return f"<rt {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</rt>"

def ruby(*content, attr={}, meta=''):
    return f"<ruby {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</ruby>"

def s(*content, attr={}, meta=''):
    return f"<s {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</s>"

def samp(*content, attr={}, meta=''):
    return f"<samp {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</samp>"

def small(*content, attr={}, meta=''):
    return f"<small {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</small>"

def span(*content, attr={}, meta=''):
    return f"<span {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</span>"

def strong(*content, attr={}, meta=''):
    return f"<strong {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</strong>"

def sub(*content, attr={}, meta=''):
    return f"<sub {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</sub>"

def sup(*content, attr={}, meta=''):
    return f"<sup {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</sup>"

def time(*content, attr={}, meta=''):
    return f"<time {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</time>"

def u(*content, attr={}, meta=''):
    return f"<u {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</u>"

def var(*content, attr={}, meta=''):
    return f"<var {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</var>"

def wbr(*content, attr={}, meta=''):
    return f"<wbr {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</wbr>"

def area(*content, attr={}, meta=''):
    return f"<area {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</area>"

def audio(*content, attr={}, meta=''):
    return f"<audio {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</audio>"

def img(*content, attr={}, meta=''):
    return f"<img {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</img>"

def map(*content, attr={}, meta=''):
    return f"<map {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</map>"

def track(*content, attr={}, meta=''):
    return f"<track {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</track>"

def video(*content, attr={}, meta=''):
    return f"<video {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</video>"

def embed(*content, attr={}, meta=''):
    return f"<embed {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</embed>"

def iframe(*content, attr={}, meta=''):
    return f"<iframe {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</iframe>"

def object(*content, attr={}, meta=''):
    return f"<object {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</object>"

def picture(*content, attr={}, meta=''):
    return f"<picture {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</picture>"

def portal(*content, attr={}, meta=''):
    return f"<portal {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</portal>"

def source(*content, attr={}, meta=''):
    return f"<source {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</source>"

def svg(*content, attr={}, meta=''):
    return f"<svg {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</svg>"

def math(*content, attr={}, meta=''):
    return f"<math {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</math>"

def canvas(*content, attr={}, meta=''):
    return f"<canvas {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</canvas>"

def noscript(*content, attr={}, meta=''):
    return f"<noscript {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</noscript>"

def script(*content, attr={}, meta=''):
    return f"<script {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</script>"

def del_(*content, attr={}, meta=''):
    return f"<del {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</del>"

def ins(*content, attr={}, meta=''):
    return f"<ins {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</ins>"

def caption(*content, attr={}, meta=''):
    return f"<caption {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</caption>"

def col(*content, attr={}, meta=''):
    return f"<col {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</col>"

def colgroup(*content, attr={}, meta=''):
    return f"<colgroup {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</colgroup>"

def table(*content, attr={}, meta=''):
    return f"<table {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</table>"

def tbody(*content, attr={}, meta=''):
    return f"<tbody {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</tbody>"

def td(*content, attr={}, meta=''):
    return f"<td {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</td>"

def tfoot(*content, attr={}, meta=''):
    return f"<tfoot {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</tfoot>"

def th(*content, attr={}, meta=''):
    return f"<th {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</th>"

def thead(*content, attr={}, meta=''):
    return f"<thead {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</thead>"

def tr(*content, attr={}, meta=''):
    return f"<tr {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</tr>"

def button(*content, attr={}, meta=''):
    return f"<button {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</button>"

def datalist(*content, attr={}, meta=''):
    return f"<datalist {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</datalist>"

def fieldset(*content, attr={}, meta=''):
    return f"<fieldset {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</fieldset>"

def form(*content, attr={}, meta=''):
    return f"<form {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</form>"

def input(*content, attr={}, meta=''):
    return f"<input {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</input>"

def label(*content, attr={}, meta=''):
    return f"<label {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</label>"

def legend(*content, attr={}, meta=''):
    return f"<legend {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</legend>"

def meter(*content, attr={}, meta=''):
    return f"<meter {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</meter>"

def optgroup(*content, attr={}, meta=''):
    return f"<optgroup {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</optgroup>"

def option(*content, attr={}, meta=''):
    return f"<option {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</option>"

def output(*content, attr={}, meta=''):
    return f"<output {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</output>"

def progress(*content, attr={}, meta=''):
    return f"<progress {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</progress>"

def select(*content, attr={}, meta=''):
    return f"<select {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</select>"

def textarea(*content, attr={}, meta=''):
    return f"<textarea {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</textarea>"

def details(*content, attr={}, meta=''):
    return f"<details {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</details>"

def dialog(*content, attr={}, meta=''):
    return f"<dialog {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</dialog>"

def summary(*content, attr={}, meta=''):
    return f"<summary {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</summary>"

def slot(*content, attr={}, meta=''):
    return f"<slot {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</slot>"

def template(*content, attr={}, meta=''):
    return f"<template {_attr_str(attr)} {meta}>{''.join([str(c) for c in content])}</template>"
