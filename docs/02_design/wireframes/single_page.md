# Wireframe: Single Article Page

## Overview
- **File**: `single.php`
- **Role**: Present article content legibly and encourage user engagement (circulation, CTA).
- **Design Policy**: Mobile-First, Flat Design (No Shadows/Gradients).

## Layout (Desktop / Mobile)

### Desktop (> 768px)
```text
+-----------------------------------------------------------------------+
| [Header]                                                              |
+-----------------------------------------------------------------------+
| [Breadcrumb] Home > Category > Article Title                          |
+-----------------------------------------------------------------------+
| [Main Content] (Left/Center)        | [Sidebar] (Right)               |
|                                     |                                 |
|  [Article Header]                   | [Search Widget] (Flat Input)    |
|  [Category Label] (Flat Badge)      |                                 |
|  <h1>Article Title:                 | [Table of Contents] (Sticky)    |
|      5 Steps to Cut Logistics Costs | (Border-left style)             |
|  </h1>                              |                                 |
|  Date: ...  Update: ...             | [Popular Posts]                 |
|                                     |                                 |
|  [Eye Catch Image] (No Shadow)      | [CTA Banner]                    |
|                                     |                                 |
|  [Lead Text]                        |                                 |
|                                     |                                 |
|  [Table of Contents] (In-article)   |                                 |
|  (Background: #F8F9FA, Flat)        |                                 |
|                                     |                                 |
|  <h2>1. Heading</h2>                |                                 |
|  Body text...                       |                                 |
|                                     |                                 |
|  [CTA Box] (Border only)            |                                 |
|                                     |                                 |
|  [Share Buttons] (Flat, No gap)     |                                 |
|                                     |                                 |
|  [Related Posts] (Grid Layout)      |                                 |
+-----------------------------------------------------------------------+
| [Footer]                                                              |
+-----------------------------------------------------------------------+
```

### Mobile (< 768px)
- **Features**: No sidebar, main content 100% width.
```text
+---------------------------------------+
| [Header] Logo      [Hamburger Menu =] |
+---------------------------------------+
| [Breadcrumb] (Scrollable or Short)    |
+---------------------------------------+
| [Main Content] (Full Width)           |
|                                       |
|  [Category Label]                     |
|  <h1>Article Title (24px)</h1>        |
|  Date: ...                            |
|                                       |
|  [Eye Catch Image]                    |
|                                       |
|  [Lead Text]                          |
|                                       |
|  [Table of Contents] (Accordion?)     |
|                                       |
|  <h2>1. Heading</h2>                  |
|  Body text...                         |
|                                       |
|  [CTA Box] (Stack Layout)             |
|                                       |
|  [Share Buttons] (Fixed Bottom?)      |
|  or (Inline Bottom)                   |
|                                       |
|  [Author Box]                         |
|                                       |
|  [Related Posts] (Stack Layout)       |
|  +--------------------------------+   |
|  | [Thumb] Title...               |   |
|  +--------------------------------+   |
|  +--------------------------------+   |
|  | [Thumb] Title...               |   |
|  +--------------------------------+   |
|                                       |
+---------------------------------------+
| [Footer]                              |
+---------------------------------------+
```
