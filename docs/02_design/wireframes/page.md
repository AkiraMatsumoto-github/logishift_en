# Wireframe: Static Page

## Overview
- **File**: `page.php`
- **Role**: Display static content such as About Us, Contact, and Privacy Policy.
- **Target Pages**:
    - About Us (`/about/`)
    - Contact (`/contact/`)
    - Privacy Policy (`/privacy-policy/`)
    - Sitemap (`/sitemap/`)
- **Design Policy**: Mobile-First, Flat Design (No Shadows/Gradients).

## Layout (Desktop / Mobile)

### Desktop (> 768px)
```text
+-----------------------------------------------------------------------+
| [Header]                                                              |
+-----------------------------------------------------------------------+
| [Breadcrumb] Home > About Us                                          |
+-----------------------------------------------------------------------+
| [Main Content] (Center / Max-width: 800px)                            |
|                                                                       |
|  <h1>About Us</h1> (Flat Style)                                       |
|                                                                       |
|  [Lead Text]                                                          |
|  Introduction to LogiShift Global operation structure.                |
|                                                                       |
|  <h2>Operation Information</h2>                                       |
|  +-------------------------------------------------------+            |
|  | Site Name      | LogiShift Global                     |            |
|  +-------------------------------------------------------+            |
|  | Operator       | LogiShift Editorial Team             |            |
|  +-------------------------------------------------------+            |
|  (Border: 1px solid Gray, No Shadow)                                  |
|                                                                       |
|  (For Contact Form)                                                   |
|  [ Name Input (Flat) ]                                                |
|  [ Email Input (Flat) ]                                               |
|  [ Message Textarea (Flat) ]                                          |
|  [ Submit Button (Flat, Solid Color) ]                                |
|                                                                       |
+-----------------------------------------------------------------------+
| [Footer]                                                              |
+-----------------------------------------------------------------------+
```

### Mobile (< 768px)
- **Features**: 100% Width (Padding 16px), stacked tables, vertically stacked forms.
```text
+---------------------------------------+
| [Header] Hamburger Menu               |
+---------------------------------------+
| [Breadcrumb]                          |
+---------------------------------------+
| [Main Content]                        |
|                                       |
|  <h1>About Us (24px)</h1>             |
|                                       |
|  <h2>Operation Information</h2>       |
|  (Table may stack or scroll)          |
|  [ Site Name ]                        |
|  [ LogiShift Global ]                 |
|  [ Operator ]                         |
|  [ LogiShift Editorial Team ]         |
|                                       |
|  (Form)                               |
|  [ Name Input ]                       |
|  [ Email Input ]                      |
|  [ Message Textarea ]                 |
|  [ Submit Button (Full Width) ]       |
|                                       |
+---------------------------------------+
| [Footer]                              |
+---------------------------------------+
```
