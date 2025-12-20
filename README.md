# LogiShift Global - Logistics SEO Media

LogiShift Global is an SEO media platform dedicated to providing high-quality information to solve challenges in the logistics industry (Cost Reduction, DX Promotion, Global Supply Chain issues, etc.).
Powered by an advanced automated article generation system using the Gemini API, it rapidly delivers the latest industry trends and know-how.

## Project Structure

```
.
├── themes/logishift/          # WordPress Theme (Custom Development)
├── automation/                # Automated Article Generation/Collection System
│   ├── collector.py           # RSS/Sitemap Collector
│   ├── scorer.py              # Article Scoring
│   ├── pipeline.py            # Automation Pipeline (Collect -> Generate)
│   ├── generate_article.py    # Main Article Generation Script
│   ├── seo_optimizer.py       # SEO Optimizer (Meta Description/Title)
│   └── ...
├── docs/                      # Project Documentation
└── .github/workflows/         # GitHub Actions (CI/CD)
```

---

## 1. Server Connection & Infrastructure

The production environment is hosted on Xserver.

### SSH Connection Info

| Item | Value |
|---|---|
| **Host** | `sv16718.xserver.jp` |
| **Port** | `10022` (Not standard 22) |
| **User** | `xs937213` |
| **Site URL** | `https://en.logishift.net` |

### Connection Command

```bash
# Basic connection
ssh -p 10022 xs937213@sv16718.xserver.jp

# Or if ~/.ssh/config is configured
ssh xserver-logishift
```

---

## 2. Deployment

GitHub Actions automatically deploys changes pushed to the `main` branch.

### A. WordPress Theme (`themes/logishift/`)
- **Auto Deploy**: Triggered by changes in `themes/logishift/`.
- **Manual Deploy (Emergency)**:
  ```bash
  scp -P 10022 -r themes/logishift/ xs937213@sv16718.xserver.jp:~/logishift.net/public_html/wp-content/themes/
  ```
  *(Note: Path might need adjustment for the English site directory if separated)*

### B. Automation System (`automation/`)
- **Auto Deploy**: Triggered by changes in `automation/`. Updates Python packages as well.
- **Manual Deploy (Emergency)**:
  ```bash
  scp -P 10022 -r automation/ xs937213@sv16718.xserver.jp:~/logishift-automation/
  ```

---

## 3. Automation System (Article Generation)

### System Overview
1.  **Collector**: Collects articles from RSS/Sitemaps (Global Media, TechCrunch, WSJ, etc.).
2.  **Scorer**: Scores "Relevance to Logistics" and "Usefulness" using Gemini.
3.  **Generator**: Generates Markdown articles, SEO metadata, and images from high-scoring articles.
4.  **Poster**: Posts to WordPress.

### Environment Setup (Local)

#### Requirements
- Python 3.10+
- Docker (For WordPress local environment)

#### Setup Steps

1.  **Prepare Python Environment**
    ```bash
    cd automation
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Environment Variables**
    Create `automation/.env`:
    ```bash
    GEMINI_API_KEY=your_apiKey
    WORDPRESS_URL=http://localhost:8001
    WORDPRESS_USERNAME=admin
    WORDPRESS_APP_PASSWORD=your_appPassword
    GOOGLE_CLOUD_LOCATION=global
    ```

3.  **WordPress Basic Auth Plugin (For Local Dev)**
    Required for REST API authentication on local WordPress.
    ```bash
    # Download and install plugin
    curl -L https://github.com/WP-API/Basic-Auth/archive/master.zip -o /tmp/basic-auth.zip
    unzip -q /tmp/basic-auth.zip -d /tmp/
    docker cp /tmp/Basic-Auth-master logishift-en-wp:/var/www/html/wp-content/plugins/basic-auth
    ```
    *Activate the plugin in the admin dashboard.*

### Execution Command Details

#### Full Automation Pipeline (`pipeline.py`)
Executes everything from collection to generation. Used for scheduled runs (cron).

```bash
# Normal execution
python automation/pipeline.py

# Adjust collection range or limit
python automation/pipeline.py --days 2 --limit 3 --threshold 80

# Dry run (Check compatibility without writing to AWS/WP)
python automation/pipeline.py --dry-run
```

#### Individual Module Execution

**Phase 1: Article Generation (`generate_article.py`)**
```bash
# By Keyword
python automation/generate_article.py --keyword "Logistics DX"

# By Article Type (know/buy/do/news/global)
python automation/generate_article.py --keyword "AGV" --type buy

# Schedule Post
python automation/generate_article.py --keyword "2024 Problem" --schedule "2025-12-10 10:00"
```

#### Internal Link Suggester
Automatically suggests and embeds relevant internal links from existing WordPress articles when generating new ones.

- **Mechanism**:
  1. Fetch existing articles from WordPress (`InternalLinkSuggester`).
  2. Gemini scores the relevance between the new article theme and existing articles.
  3. "Excerpts" of high-relevance articles are injected into the writing prompt, allowing natural link placement.

- **Configuration (Number of articles read)**:
  Currently set to **latest 50 articles**.
  To change, modify `automation/generate_article.py`:
  ```python
  # automation/generate_article.py
  candidates = linker.fetch_candidates(limit=50)  # Change this number
  ```

**Phase 2: Collection (`collector.py`)**
```bash
# Collect from all sources
python automation/collector.py --source all > articles.json

# Specific source only (e.g., TechCrunch)
python automation/collector.py --source techcrunch --days 3
```

**Phase 2: Scoring (`scorer.py`)**
```bash
# Score from file input
python automation/scorer.py --input articles.json --threshold 80 --output scored.json
```

**Phase 3: Static Page Generation (`generate_static_pages.py`)**
```bash
python automation/generate_static_pages.py --all
```

---

## 4. Troubleshooting

### Server Operations

#### gcloud authentication missing
```bash 
gcloud auth application-default login
```

#### Permission error (Theme not reflecting)
```bash
ssh -p 10022 xs937213@sv16718.xserver.jp
chmod -R 755 ~/logishift.net/public_html/wp-content/themes/logishift
```

#### Automation script fails (Dependencies)
Miniconda environment might need rebuilding.
```bash
ssh -p 10022 xs937213@sv16718.xserver.jp
cd ~/logishift-automation/automation
conda install -c conda-forge lxml -y
pip install -r requirements.txt
```

#### GitHub Actions Deployment Failure
Check GitHub Secrets (`Settings > Secrets`):
- `SERVER_HOST`: sv16718.xserver.jp
- `SERVER_USER`: xs937213
- `SSH_PORT`: 10022
- `SSH_PRIVATE_KEY`: (Is it the correct private key?)

### Local Development
#### Start Environment
```bash
source automation/venv/bin/activate
export GOOGLE_CLOUD_LOCATION=global   
```

#### Articles not generating (Low Score)
The default `--threshold` in `pipeline.py` (85) might be too high. Try lowering it to around 60: `--threshold 60`.

## Related Documentation
- [Theme Deployment Guide](docs/00_meta/theme_deployment_guide.md)
- [Production Deployment Guide](docs/00_meta/production_deployment_guide.md)
