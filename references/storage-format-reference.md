# Confluence Storage Format Reference

## Summary

This document provides a reference for Confluence Storage Format (XHTML-based XML format used to store pages, templates, comments, and blog posts). The format uses custom XML namespaces:
- `ac:` - Confluence macros
- `ri:` - Resource identifiers (for pages, attachments, etc.)
- `at:` - Template variables

Key elements:
- **Headings** (`<h1>` to `<h6>`)
- **Text formatting** (`<strong>`, `<em>`, `<code>`, `<span>`, etc.)
- **Lists** (ordered `<ol>`, unordered `<ul>`, task lists `<ac:task-list>`)
- **Links** (`<ac:link>`, `<a>`, with `<ri:page>`, `<ri:attachment>` for internal resources)
- **Images** (`<ac:image>` with `<ri:attachment>` or `<ri:url>`)
- **Tables** (`<table>`, `<tr>`, `<td>`, `<th>` with `rowspan`/`colspan`)
- **Page layouts** (`<ac:layout>`, `<ac:layout-section>`, `<ac:layout-cell>`)
- **Emojis** (`<ac:emoticon>`)
- **Template variables** (`<at:declarations>`, `<at:var>`, `<at:string>`, `<at:textarea>`, `<at:list>`)
- **Instructional text** (`<ac:placeholder>`)


## Table of Contents

- [Headings](#headings)
- [Text Effects](#text-effects)
- [Text Breaks](#text-breaks)
- [Lists](#lists)
- [Links](#links)
  - [Link Body Markup Tags](#link-body-markup-tags)
- [Images](#images)
  - [Image Attributes](#image-attributes)
- [Tables](#tables)
- [Page Layouts](#page-layouts)
- [Emojis (Emoticons)](#emojis-emoticons)
- [Resource Identifiers](#resource-identifiers)
- [Template Variables](#template-variables)
- [Instructional Text](#instructional-text)
- [Summary](#summary)

## Headings

| Level | HTML Tag | Example |
|-------|----------|---------|
| 1 | `<h1>` | `<h1>Heading 1</h1>` |
| 2 | `<h2>` | `<h2>Heading 2</h2>` |
| 3 | `<h3>` | `<h3>Heading 3</h3>` |
| 4 | `<h4>` | `<h4>Heading 4</h4>` |
| 5 | `<h5>` | `<h5>Heading 5</h5>` |
| 6 | `<h6>` | `<h6>Heading 6</h6>` |

## Text Effects

| Format | XML Tag | Example |
|--------|---------|---------|
| Strong/Bold | `<strong>` | `<strong>strong text</strong>` |
| Emphasis | `<em>` | `<em>Italics Text</em>` |
| Strikethrough | `<span>` | `<span style="text-decoration: line-through;">strikethrough</span>` |
| Underline | `<u>` | `<u>underline</u>` |
| Superscript | `<sup>` | `<sup>superscript</sup>` |
| Subscript | `<sub>` | `<sub>subscript</sub>` |
| Monospace | `<code>` | `<code>monospaced</code>` |
| Preformatted | `<pre>` | `<pre>preformatted text</pre>` |
| Block quotes | `<blockquote>` | `<blockquote><p>block quote</p></blockquote>` |
| Text color | `<span>` | `<span style="color: rgb(255,0,0);">red text</span>` |
| Small | `<small>` | `<small>small text</small>` |
| Big | `<big>` | `<big>big text</big>` |
| Center-align | `<p>` | `<p style="text-align: center;">centered text</p>` |
| Right-align | `<p>` | `<p style="text-align: right;">right aligned text</p>` |

## Text Breaks

| Format | XML Tag | Example |
|--------|---------|---------|
| New paragraph | `<p>` | `<p>Paragraph 1</p><p>Paragraph 2</p>` |
| Line break | `<br>` | `Line 1 <br /> Line 2` |
| Horizontal rule | `<hr>` | `<hr />` |
| — symbol (em dash) | Entity | `&mdash;` |
| – symbol (en dash) | Entity | `&ndash;` |

Make sure Line break is always used as <br /> not <br>

## Lists

| Format | XML Structure | Example |
|--------|---------------|---------|
| Unordered list | `<ul><li>` | `<ul><li>round bullet list item</li></ul>` |
| Ordered list | `<ol><li>` | `<ol><li>numbered list item</li></ol>` |
| Task List | `<ac:task-list>` | `<ac:task-list><ac:task><ac:task-status>incomplete</ac:task-status><ac:task-body>task list item</ac:task-body></ac:task></ac:task-list>` |

## Links

| Type | XML Structure | Example |
|------|---------------|---------|
| Confluence page | `<ac:link><ri:page>` | `<ac:link><ri:page ri:content-title="Page Title" /><ac:plain-text-link-body><![CDATA[Link text]]></ac:plain-text-link-body></ac:link>` |
| Attachment | `<ac:link><ri:attachment>` | `<ac:link><ri:attachment ri:filename="file.gif" /><ac:plain-text-link-body><![CDATA[Link text]]></ac:plain-text-link-body></ac:link>` |
| External URL | `<a>` | `<a href="http://example.com">text</a>` |
| Anchor (same page) | `<ac:link ac:anchor>` | `<ac:link ac:anchor="anchor"><ac:plain-text-link-body><![CDATA[Link text]]></ac:plain-text-link-body></ac:link>` |
| Anchor (another page) | `<ac:link><ri:page>` | `<ac:link ac:anchor="anchor"><ri:page ri:content-title="pagetitle" /><ac:plain-text-link-body><![CDATA[Link text]]></ac:plain-text-link-body></ac:link>` |
| Image link body | `<ac:link-body>` | `<ac:link><ac:link-body><ac:image>...</ac:image></ac:link-body></ac:link>` |

### Link Body Markup Tags

Permitted tags within `<ac:link-body>`: `<b>`, `<strong>`, `<em>`, `<i>`, `<code>`, `<tt>`, `<sub>`, `<sup>`, `<br>`, `<span>`

## Images

| Type | XML Structure | Example |
|------|---------------|---------|
| Attached image | `<ac:image><ri:attachment>` | `<ac:image><ri:attachment ri:filename="atlassian_logo.gif" /></ac:image>` |
| External image | `<ac:image><ri:url>` | `<ac:image><ri:url ri:value="http://example.com/image.png" /></ac:image>` |

### Image Attributes

| Attribute | Description |
|-----------|-------------|
| `ac:align` | image alignment |
| `ac:border` | Set to "true" to set a border |
| `ac:class` | CSS class attribute |
| `ac:title` | image tooltip |
| `ac:style` | CSS style |
| `ac:thumbnail` | Set to "true" to designate as thumbnail |
| `ac:alt` | alt text |
| `ac:height` | image height |
| `ac:width` | image width |
| `ac:vspace` | white space on top and bottom |
| `ac:hspace` | white space on left and right |

## Tables

| Format | XML Structure | Example |
|--------|---------------|---------|
| Basic table | `<table><tbody><tr><th><td>` | see reference |
| Merged cells | `rowspan`, `colspan` | `<td rowspan="2" colspan="1">Cell</td>` |

## Page Layouts

| Element | Description | Attributes |
|---------|-------------|------------|
| `<ac:layout>` | Indicates page has layout (top-level element) | None |
| `<ac:layout-section>` | Represents a row in layout | `ac:type` (e.g., "single", "three_with_sidebars") |
| `<ac:layout-cell>` | Cell within layout section | None |

### Layout Example

```xml
<ac:layout>
  <ac:layout-section ac:type="single">
     <ac:layout-cell>
        {content}
     </ac:layout-cell>
  </ac:layout-section>
  <ac:layout-section ac:type="three_with_sidebars">
     <ac:layout-cell>{content}</ac:layout-cell>
     <ac:layout-cell>{content}</ac:layout-cell>
     <ac:layout-cell>{content}</ac:layout-cell>
  </ac:layout-section>
</ac:layout>
```

## Emojis (Emoticons)

| Format | XML Structure | Example |
|--------|---------------|---------|
| Emoji | `<ac:emoticon>` | `<ac:emoticon ac:name="smile" />` |

Supported emoticon names: smile, sad, cheeky, laugh, wink, thumbs-up, thumbs-down, information, tick, cross, warning

## Resource Identifiers

| Resource | Format | Notes |
|----------|--------|-------|
| Page | `<ri:page ri:space-key="..." ri:content-title="..." />` | `ri:space-key` optional; `ri:content-title` required |
| Blog Post | `<ri:blog-post ri:space-key="..." ri:content-title="..." ri:posting-day="YYYY/MM/DD" />` | `ri:posting-day` required format YYYY/MM/DD |
| Attachment | `<ri:attachment ri:filename="...">...</ri:attachment>` | Body contains container reference; can be relative |
| URL | `<ri:url ri:value="http://..." />` | `ri:value` required |
| Shortcut | `<ri:shortcut ri:key="..." ri:parameter="..." />` | Example: `[ABC-123@jira]` |
| User | `<ri:user ri:userkey="..." />` | `ri:userkey` required |
| Space | `<ri:space ri:space-key="..." />` | `ri:space-key` required |
| Content Entity | `<ri:content-entity ri:content-id="..." />` | `ri:content-id` required |

## Template Variables

| Variable Type | Declaration | Usage |
|---------------|-------------|-------|
| Single-line text | `<at:string at:name="..." />` | `<at:var at:name="..." />` |
| Multi-line text | `<at:textarea at:name="..." at:rows="..." at:columns="..." />` | `<at:var at:name="..." />` |
| List | `<at:list at:name="..."><at:option at:value="..." /></at:list>` | `<at:var at:name="..." />` |

### Template Example

```xml
<at:declarations>
  <at:string at:name="MyText" />
  <at:textarea at:columns="100" at:name="MyMulti" at:rows="5" />
  <at:list at:name="MyList">
    <at:option at:value="Apples" />
    <at:option at:value="Pears" />
    <at:option at:value="Peaches" />
  </at:list>
</at:declarations>
```

## Instructional Text

| Format | XML Structure | Example |
|--------|---------------|---------|
| Placeholder text | `<ac:placeholder>` | `<ac:placeholder>This text clears on edit</ac:placeholder>` |
| Mention placeholder | `<ac:placeholder ac:type="mention">` | `<ac:placeholder ac:type="mention">@mention example</ac:placeholder>` |

### Instructional Text Example

```xml
<ul>
  <li><ac:placeholder>This is instructional text that clears when typing</ac:placeholder></li>
</ul>
<ac:task-list>
  <ac:task>
    <ac:task-status>incomplete</ac:task-status>
    <ac:task-body><ac:placeholder ac:type="mention">@mention example</ac:placeholder></ac:task-body>
  </ac:task>
</ac:task-list>
```

## UML macros

```xml
<ac:structured-macro ac:name="plantuml" ac:schema-version="1"
    ac:macro-id="a775400f-ad2e-4e81-ac4d-fc333ac20450">
    <ac:parameter ac:name="atlassian-macro-output-type">INLINE</ac:parameter><ac:plain-text-body>
        <![CDATA[ UML diagramm code goes here ]]>
    </ac:plain-text-body>
</ac:structured-macro>
```
