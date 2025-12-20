# Component Design

This document outlines the design system and component specifications for LogiShift (Global).
It reflects the current "Flat Design" principles: no shadows, no gradients, and pill-shaped interactive elements.

## 1. Buttons

### Primary Button (CTA)
- **Usage**: Main actions like "Read More", "Contact Us".
- **Style**:
    - **Background**: `Tech Blue (#00B4D8)` (Solid)
    - **Text**: `White (#FFFFFF)`
    - **Border Radius**: `32px` (Pill-shaped)
    - **Border**: None
    - **Shadow**: None
    - **Hover**: Background darkens slightly (`#0096B4`). No lift effect.

- **Size**:
    - **Padding**: `14px 36px`

### Secondary Button (Outline)
- **Usage**: Secondary actions like "See More", "Cancel".
- **Style**:
    - **Background**: Transparent
    - **Border**: `2px solid Tech Blue`
    - **Border Radius**: `32px` (Pill-shaped)
    - **Text**: `Tech Blue`
    - **Hover**: Background becomes `Tech Blue`, Text becomes `White`.

### Text Link
- **Usage**: Inline links, subtle navigation.
- **Style**:
    - **Text**: `Tech Blue`
    - **Underline**: Appears on hover.
    - **Icon**: Optional arrow that moves slightly on hover (e.g., `text-link-arrow`).

## 2. Cards

### Article Card
- **Structure**:
    - Thumbnail Image (Aspect Ratio 16:9)
    - Category Label (Overlaid or above title)
    - Title (H3 level)
    - Meta Info (Date)
- **Style**:
    - **Background**: `White`
    - **Border**: `1px solid Border Gray`
    - **Shadow**: None
    - **Border Radius**: `16px`
    - **Transition**: Border color changes to `Tech Blue` on hover. No lift effect.
    - **Image Interaction**: Slight zoom (scale 1.05) on hover.

## 3. Labels & Badges

### Category Label
- **Usage**: Indicates the article category.
- **Style**:
    - **Background**: `Navy Blue (#0A192F)` (Default)
    - **Text**: `White`
    - **Font Size**: `0.7rem`
    - **Border Radius**: `20px` (Pill-shaped)
    - **Padding**: `4px 10px`
    - **Text Transform**: Uppercase

## 4. Form Elements

### Inputs / Textareas
- **Style**:
    - **Background**: `White` or `Light Gray` (depending on context)
    - **Border**: `1px solid Border Gray`
    - **Shadow**: None
    - **Border Radius**: `4px` (Slightly rounded for inputs, distinct from buttons) or `50px` for Search fields.
    - **Padding**: `12px`
    - **Focus**: `Tech Blue` border (`2px` solid). No glow.

## 5. Navigation

### Header Navigation
- **Desktop**: Horizontal text links.
    - **Style**: Pill-shaped hover effect (`border-radius: 20px`).
    - **Hover**: Background `Tech Blue`, Text `White`.
- **Mobile**: Hamburger menu. Expands to a drawer/vertical list.

### Breadcrumbs
- **Usage**: Indicates current page location.
- **Style**:
    - **Text**: `Medium Gray`
    - **Separator**: `>` (Chevron Right)
    - **Current Page**: `Dark Gray` (Regular weight)

## 6. Typography & Icons

### Typography
- **Headings**: `Inter` (sans-serif), Bold (`700/800`).
- **Body**: `Noto Sans JP` (or system sans-serif for Global), `line-height: 1.8`.

### Icons
- **Library**: `Phosphor Icons` or `Heroicons` (SVG).
- **Style**: Line/Outline style. Consistent stroke width.

## Color Palette Reference
- **Tech Blue**: `#00B4D8`
- **Tech Blue Dark**: `#0096B4`
- **Navy Blue**: `#0A192F`
- **White**: `#FFFFFF`
- **Light Gray**: `#F8F9FA`
- **Border Gray**: `#E0E0E0`
- **Text**: `#333333`
