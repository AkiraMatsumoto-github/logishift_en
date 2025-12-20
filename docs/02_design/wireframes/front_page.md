# Wireframe: Front Page

## Overview
- **File**: `front-page.php`
- **Role**: Serve as the face of the site, conveying brand image and providing navigation to key content.
- **Design Policy**: Mobile-First, Flat Design (No Shadows/Gradients).

## Layout (Desktop / Mobile)

### Desktop (> 768px)
```text
+-----------------------------------------------------------------------+
| [Header] Logo: LogiShift Global                                       |
| Nav: [Global Trends] [Tech & DX] [Cost] [SCM] [Search]                |
+-----------------------------------------------------------------------+
| [Hero Section] (Flat Color Background)                                |
| "Shaping the Future of Logistics with DX"                             |
| [ Read Latest Articles (Flat Button) ]                                |
+-----------------------------------------------------------------------+
| [Featured Articles]                                                   |
| +-----------+ +-----------+ +-----------+                             |
| | [Thumb]   | | [Thumb]   | | [Thumb]   |                             |
| | Title...  | | Title...  | | Title...  |                             |
| +-----------+ +-----------+ +-----------+                             |
+-----------------------------------------------------------------------+
| [Category Sections]                                                   |
| (Loop: Global Trends, Technology & DX, Cost & Efficiency, SCM, Cases) |
|                                                                       |
|  Title: Technology & DX                                               |
|  +-----------+ +-----------+ +-----------+                            |
|  | [Thumb]   | | [Thumb]   | | [Thumb]   |                            |
|  +-----------+ +-----------+ +-----------+                            |
|  [ View More -> ]                                                     |
|                                                                       |
|  (Repeats for other categories...)                                    |
+-----------------------------------------------------------------------+
| [Global Trends]                                                       |
| [ALL] [Japan] [USA] [Europe] [Asia-Pacific] (Tabs)                    |
| +-----------+ +-----------+ +-----------+                             |
| | [Thumb]   | | [Thumb]   | | [Thumb]   |                             |
| | 🇯🇵 JP      | | 🇺🇸 USA    | | 🇪🇺 EU     |                             |
| +-----------+ +-----------+ +-----------+                             |
| ... (Grid 3 cols)                                                     |
| [ View More -> ]                                                      |
+-----------------------------------------------------------------------+
| [By Topic]                                                            |
|                                                                       |
|  [Icon] Sustainability    [Icon] Labor Shortage                       |
|  +-----------+             +-----------+                              |
|  | [Thumb]   |             | [Thumb]   |                              |
|  | Title...  |             | Title...  |                              |
|  +-----------+             +-----------+                              |
|  (Horizontal Scroll or Grid)                                          |
+-----------------------------------------------------------------------+
| [Footer]                                                              |
+-----------------------------------------------------------------------+
```

### Mobile (< 768px)
- **Features**: Single column. Article list is "Side-by-side (Thumb Left, Text Right)".
```text
+---------------------------------------+
| [Header] Logo      [Hamburger Menu =] |
+---------------------------------------+
| [Hero Section]                        |
+---------------------------------------+
| [Featured Articles]                   |
| (Stack Layout - Horizontal Card)      |
| +-----------------------------------+ |
| | [Thumb] | [Category]              | |
| | (Square)| Article Title...        | |
| +-----------------------------------+ |
| +-----------------------------------+ |
| | [Thumb] | ...                     | |
| +-----------------------------------+ |
+---------------------------------------+
| [Category List]                       |
|  Title: Technology & DX               |
|  [ View More -> ]                     |
|  +--------------------------------+   |
|  | [Thumb] | Title...             |   |
|  +--------------------------------+   |
|  (Limit 3 items)                      |
|                                       |
|  (Repeats...)                         |
+---------------------------------------+
| [Global Trends]                       |
| [ALL] [JP] [USA] [EU] [Asia] (Scroll) |
| +-----------------------------------+ |
| | [Thumb] | 🇯🇵 JP                   | |
| |         | Title...                | |
| +-----------------------------------+ |
| [ View More -> ] (Button)             |
+---------------------------------------+
| [By Topic]                            |
|  [Icon] Sustainability                |
|  (Horizontal Scroll Area)             |
|  [Card] [Card] [Card]                 |
+---------------------------------------+
| [Footer]                              |
+---------------------------------------+
```
