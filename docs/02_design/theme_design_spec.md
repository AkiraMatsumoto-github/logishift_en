# LogiShift Theme Design Specification

## 1. Design Concept
- **Keywords**: Reliable, Progressive, Business, Logistics, Clear, Direct
- **Design Policy**: Mobile-First, **Flat Design** (No Shadows, No Gradients), **Pill-shaped Elements**.
- **Color Palette**:
    - **Main**: Deep Navy (`#0A192F`) - Reliability, Stability
    - **Accent**: Tech Blue (`#00B4D8`) - Innovation, DX
    - **Base**: White / Light Gray (`#F8F9FA`) - Cleanliness
    - **Text**: Dark Gray (`#333333`) - Readability
- **Fonts**:
    - **Global/En**: Inter (Google Fonts) - Headings & UI
    - **Body**: System Sans-serif (or Noto Sans for Japan context)

## 2. Page Template Hierarchy

| Template File | Usage | Role & Function |
| :--- | :--- | :--- |
| `front-page.php` | Front Page | The face of the site. Features Hero Section, Latest Articles, Category Sections, and CTAs. |
| `index.php` | Blog Roll / Default | Standard list of articles (Fall back for `home.php` if not present). |
| `single.php` | Single Post | Individual article page. Contains Table of Contents, Content, Related Posts, Share Buttons, Author Info. |
| `page.php` | Static Page | Static content like "About Us", "Contact", "Privacy Policy". |
| `archive.php` | Category/Tag Archive | List of articles belonging to a specific category or tag. |
| `search.php` | Search Results | Displays search results. |
| `404.php` | 404 Page | Error page when content is not found. Guides users back to the sitemap or home. |

## 3. Component Design

### Common Components
- **Header (`header.php`)**:
    - Logo (Left)
    - Global Navigation (Right): "Cost Reduction", "Logistics DX", "Trends", "Glossary"
    - Hamburger Menu (Mobile)
- **Footer (`footer.php`)**:
    - Sitemap Links
    - About / Legal Links
    - Copyright
- **Sidebar (`sidebar.php`)**:
    - Widget area for posts (displayed on Desktop, bottom or hidden on Mobile).

### Page-Specific Components
- **Hero Section (Front Page)**:
    - **Copy**: "Shifting Business through Logistics"
    - **Background**: Abstract graphics representing logistics networks.
    - **Style**: Slider or Static Hero with distinct CTA.
- **Article Card (Archives/Lists)**:
    - Thumbnail (16:9)
    - Category Label (Pill-shaped)
    - Title (H3)
    - Excerpt & Date
    - **Style**: **Flat Design** (Border only, No Shadow), Stack Layout on Mobile.
- **CTA Box**:
    - Banners for newsletter signup or whitepaper downloads (End of article or Sidebar).

## 4. CMS Design (WordPress)

### Post Types
Currently using standard `Post` and `Page`.

- **Post**: Regular articles (News, Know-how, Case Studies).
- **Page**: Static pages (Company Info, Contact).

### Taxonomies
- **Category**: Hierarchical.
    - `Basics`
    - `Cost Reduction`
    - `Logistics DX`
    - `Industry Trends`
- **Tag**: Flat keywords.
    - `2024 Problem`, `WMS`, `RFID`, `Last Mile`, `Driver Shortage`

### Custom Fields
Not using plugins (ACF) initially. Standard custom fields or manual theme support if needed.

### Menu Locations
- `primary`: Header Main Navigation
- `footer`: Footer Links

### Widget Areas
- `sidebar-1`: Sidebar for Single Post pages (PC only usually).

## 5. Implementation Roadmap
(Retrospective / Maintenance)

1.  **Base Setup**: `functions.php`, `style.css` (Variables), `header.php`, `footer.php`
2.  **Front Page**: `front-page.php` (Hero, Lists)
3.  **Single Post**: `single.php` (Styles, TOC, Related)
4.  **Archives**: `archive.php` (Category grids)
5.  **Static Pages**: `page.php`
