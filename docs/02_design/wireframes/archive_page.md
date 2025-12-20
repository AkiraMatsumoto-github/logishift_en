# Wireframe: Archive Page

## Overview
- **File**: `archive.php`, `home.php`, `search.php`
- **Role**: Display a list of articles matching a specific theme or condition, guiding users to their desired content.
- **Design Policy**: Mobile-First, Flat Design (No Shadows/Gradients).

## Layout (Desktop / Mobile)

### Desktop (> 768px)
```text
+-----------------------------------------------------------------------+
| [Header]                                                              |
+-----------------------------------------------------------------------+
| [Page Header] (Flat Background)                                       |
|                                                                       |
|    CATEGORY: Cost Reduction                                           |
|    "Articles related to logistics cost reduction."                    |
|                                                                       |
+-----------------------------------------------------------------------+
| [Main Content] (Left/Center)        | [Sidebar] (Right)               |
|                                     |                                 |
| +-------------------------------+   | [Search Widget] (Flat)          |
| | [Thumbnail Image]             |   |                                 |
| |                               |   | [Popular Posts]                 |
| | [Category] 2025.11.23         |   |                                 |
| | Article Title (H3)            |   | [Categories Widget]             |
| | Excerpt text...               |   |                                 |
| +-------------------------------+   | [Tags Cloud] (Flat Badges)      |
| (Border: 1px solid Gray)            |                                 |
| (No Shadow)                         | [CTA Banner]                    |
|                                     |                                 |
| +-------------------------------+   |                                 |
| | ...                           |   |                                 |
| +-------------------------------+   |                                 |
|                                     |                                 |
| [Pagination] (Flat Buttons)         |                                 |
|  [<] [1] [2] [3] [>]                |                                 |
|                                     |                                 |
+-----------------------------------------------------------------------+
| [Footer]                                                              |
+-----------------------------------------------------------------------+
```

### Mobile (< 768px)
- **Features**: No sidebar, stacked article cards.
```text
+---------------------------------------+
| [Header] Logo      [Hamburger Menu =] |
+---------------------------------------+
| [Page Header]                         |
|  CATEGORY: Cost Reduction             |
+---------------------------------------+
| [Main Content] (Full Width)           |
|                                       |
| +-----------------------------------+ |
| | [Thumb] | [Category]              | |
| | (Square)| Article Title           | |
| |         | Excerpt...              | |
| +-----------------------------------+ |
| (Border-bottom separator)             |
|                                       |
| +-----------------------------------+ |
| | [Thumb] | ...                     | |
| +-----------------------------------+ |
|                                       |
| [Pagination]                        |
|  [Prev] 1 / 10 [Next]               |
+---------------------------------------+
| [Footer]                              |
+---------------------------------------+
```
