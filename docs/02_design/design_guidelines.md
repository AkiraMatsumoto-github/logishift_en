# LogiShift Design Guidelines

## 1. Design Concept
**"Reliable & Progressive"**
We aim for a design that conveys future-oriented potential through technology and DX, while being grounded in the solid foundation of the logistics industry.

## 2. Color Palette

### Primary Colors (Brand Identity)
- **Navy Blue (`#0A192F`)**:
    - **Usage**: Header, footer, primary text, prominent backgrounds.
    - **Impression**: Reliability, professionalism, depth.
- **Tech Blue (`#00B4D8`)**:
    - **Usage**: Accents, links, buttons, icons.
    - **Impression**: Technology, intelligence, future, cleanliness.

### Secondary Colors (Functional)
- **White (`#FFFFFF`)**: Backgrounds, card bases.
- **Light Gray (`#F8F9FA`)**: Overall site background, section separators.
- **Dark Gray (`#333333`)**: Body text.
- **Medium Gray (`#666666`)**: Supplemental text, dates, metadata.
- **Border Gray (`#E0E0E0`)**: Borders, card outlines.

### Color Usage Rules
- **No Gradients (Flat Design)**: Strictly adhere to flat design principles. Use solid colors.
- **Text Color**: Avoid pure black (`#000`). Use `#333` for better readability.
- **CTA**: Always use `Tech Blue` for action-oriented elements (Call To Action).

## 3. Typography

### Font Families
- **Global / En**: `Inter` (Google Fonts) for headings and UI elements.
- **Body**: System sans-serif (e.g., San Francisco, Segoe UI, Roboto) or `Noto Sans` to ensure fast loading and native feel.
    - *Note*: If a specific web font is required for body, use `Inter` with correct line-heights.

### Font Size Scale (rem based)
- **H1**: 2.5rem (40px) - Page Titles
- **H2**: 2.0rem (32px) - Section Headings
- **H3**: 1.75rem (28px) - Card Titles, Sub-headings
- **H4**: 1.5rem (24px) - Minor Headings
- **Body**: 1.0rem (16px) - Main Text
- **Small**: 0.875rem (14px) - Metadata, Notes

### Line Height
- **Headings**: 1.3 - 1.4 (Tight)
- **Body**: 1.8 (Readable)

## 4. Spacing & Shapes

### Spacing
Use an 8px-based scale to maintain consistent spacing.
- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px
- **3xl**: 64px
- **section**: 80px - 120px (Between sections)

### Shapes
- **Border Radius**:
    - **Buttons**: `32px` (Pill-shaped) - **Strict Rule**
    - **Labels**: `20px` (Pill-shaped)
    - **Cards**: `16px` (Rounded Rectangle)
    - **Inputs**: `4px` (Slightly Rounded) or `50px` (Search Pills)
- **Shadows**: `None`. Flatten all elements. Use borders and background color differences to express hierarchy. Do NOT use drop shadows for lift effects.
- **No Lift Effect**: Elements should not physically "lift" on hover. Use color shifts instead.

## 5. Layout

- **Mobile First**: Prioritize the smartphone experience.
- **Container Width**: Max `1200px` (Desktop). Side padding `16px` (Mobile).
- **Grid**:
    - **Desktop**: 12-column grid or Card Grid (`repeat(auto-fill, minmax(320px, 1fr))`).
    - **Mobile**: Single column stack layout.
- **Breakpoints**:
    - **Mobile**: ~767px
    - **Tablet**: 768px ~ 1023px
    - **Desktop**: 1024px ~
