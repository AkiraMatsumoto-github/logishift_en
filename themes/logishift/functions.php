<?php
/**
 * LogiShift functions and definitions
 *
 * @package LogiShift
 */

// Enqueue styles
function logishift_scripts() {
    wp_enqueue_style( 'logishift-style', get_stylesheet_uri(), array(), '1.0.15' );

    // Swiper
    if ( is_front_page() ) {
        wp_enqueue_style( 'swiper-css', 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css', array(), '11.0.0' );
        wp_enqueue_script( 'swiper-js', 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js', array(), '11.0.0', true );
        wp_enqueue_script( 'logishift-front-page', get_template_directory_uri() . '/assets/js/front-page.js', array( 'swiper-js', 'jquery' ), '1.0.0', true );
    }

    wp_enqueue_script( 'logishift-navigation', get_template_directory_uri() . '/assets/js/navigation.js', array(), '1.0.7', true );
}
add_action( 'wp_enqueue_scripts', 'logishift_scripts' );

if ( ! function_exists( 'logishift_setup' ) ) :
	function logishift_setup() {
		// Add default posts and comments RSS feed links to head.
		add_theme_support( 'automatic-feed-links' );

		// Let WordPress manage the document title.
		add_theme_support( 'title-tag' );

		// Enable support for Post Thumbnails on posts and pages.
		add_theme_support( 'post-thumbnails' );

		// Add support for editor styles.
		add_theme_support( 'editor-styles' );

		// Enqueue editor styles.
		add_editor_style( 'style.css' );

		// Register navigation menus.
		register_nav_menus(
			array(
				'menu-1' => esc_html__( 'Primary', 'logishift' ),
				'footer' => esc_html__( 'Footer', 'logishift' ),
			)
		);

		// Add support for core custom logo.
		add_theme_support(
			'custom-logo',
			array(
				'height'      => 250,
				'width'       => 250,
				'flex-width'  => true,
				'flex-height' => true,
			)
		);
	}
endif;
add_action( 'after_setup_theme', 'logishift_setup' );

/**
 * Register widget area.
 *
 * @link https://developer.wordpress.org/themes/functionality/sidebars/#registering-a-sidebar
 */
function logishift_widgets_init() {
	register_sidebar(
		array(
			'name'          => esc_html__( 'Sidebar', 'logishift' ),
			'id'            => 'sidebar-1',
			'description'   => esc_html__( 'Add widgets here.', 'logishift' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);
}
add_action( 'widgets_init', 'logishift_widgets_init' );

/**
 * Create dummy menu for demonstration.
 */
function logishift_create_dummy_menu() {
    $menu_name = 'Primary Menu';
    $menu_exists = wp_get_nav_menu_object( $menu_name );

    if ( ! $menu_exists ) {
        $menu_id = wp_create_nav_menu( $menu_name );

        wp_update_nav_menu_item( $menu_id, 0, array(
            'menu-item-title' =>  __( 'Home', 'logishift' ),
            'menu-item-url' => home_url( '/' ),
            'menu-item-status' => 'publish'
        ) );

        wp_update_nav_menu_item( $menu_id, 0, array(
            'menu-item-title' =>  __( 'Global Trends', 'logishift' ),
            'menu-item-url' => home_url( '/category/global-trends/' ),
            'menu-item-status' => 'publish'
        ) );

        wp_update_nav_menu_item( $menu_id, 0, array(
            'menu-item-title' =>  __( 'Tech & DX', 'logishift' ),
            'menu-item-url' => home_url( '/category/technology-dx/' ),
            'menu-item-status' => 'publish'
        ) );

        wp_update_nav_menu_item( $menu_id, 0, array(
            'menu-item-title' =>  __( 'Cost', 'logishift' ),
            'menu-item-url' => home_url( '/category/cost-efficiency/' ),
            'menu-item-status' => 'publish'
        ) );

        wp_update_nav_menu_item( $menu_id, 0, array(
            'menu-item-title' =>  __( 'SCM', 'logishift' ),
            'menu-item-url' => home_url( '/category/scm/' ),
            'menu-item-status' => 'publish'
        ) );

        wp_update_nav_menu_item( $menu_id, 0, array(
            'menu-item-title' =>  __( 'Contact', 'logishift' ),
            'menu-item-url' => home_url( '/contact/' ),
            'menu-item-status' => 'publish'
        ) );

        $locations = get_theme_mod( 'nav_menu_locations' );
        $locations['menu-1'] = $menu_id;
        set_theme_mod( 'nav_menu_locations', $locations );
    }
}
add_action( 'init', 'logishift_create_dummy_menu' );

/**
 * Add search form to navigation menu.
 */
function logishift_add_search_to_menu( $items, $args ) {
    if ( $args->theme_location == 'menu-1' ) {
        $items .= '<li class="menu-item menu-item-search">';
        $items .= get_search_form( false );
        $items .= '</li>';
    }
    return $items;
}

add_filter( 'wp_nav_menu_items', 'logishift_add_search_to_menu', 10, 2 );

/**
 * Output SEO Meta Tags.
 */
function logishift_seo_meta() {
    global $post;

    // Default values
    $title = wp_get_document_title();
    $description = get_bloginfo( 'description' );
    $url = get_permalink();
    $site_name = get_bloginfo( 'name' );
    $type = 'website';
    $image = get_template_directory_uri() . '/assets/images/hero-bg.png'; // Default image

    // Single Post / Page
    if ( is_singular() ) {
        $type = 'article';
        if ( has_excerpt() ) {
            $description = get_the_excerpt();
        } else {
            $description = wp_trim_words( $post->post_content, 120, '...' );
        }
        
        if ( has_post_thumbnail() ) {
            $image = get_the_post_thumbnail_url( $post->ID, 'large' );
        }
    }
    
    // Archive / Category
    if ( is_archive() ) {
        $description = get_the_archive_description();
        if ( empty( $description ) ) {
            $description = 'Archive for ' . get_the_archive_title();
        }
        $url = get_category_link( get_queried_object_id() );
    }

    // Sanitize
    $description = strip_tags( $description );
    $description = str_replace( array( "\r", "\n" ), '', $description );

    ?>
    <!-- SEO Meta Tags -->
    <meta name="description" content="<?php echo esc_attr( $description ); ?>">
    
    <!-- OGP -->
    <meta property="og:title" content="<?php echo esc_attr( $title ); ?>">
    <meta property="og:description" content="<?php echo esc_attr( $description ); ?>">
    <meta property="og:url" content="<?php echo esc_url( $url ); ?>">
    <meta property="og:type" content="<?php echo esc_attr( $type ); ?>">
    <meta property="og:site_name" content="<?php echo esc_attr( $site_name ); ?>">
    <meta property="og:image" content="<?php echo esc_url( $image ); ?>">
    <meta property="og:locale" content="en_US">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="<?php echo esc_attr( $title ); ?>">
    <meta name="twitter:description" content="<?php echo esc_attr( $description ); ?>">
    <meta name="twitter:image" content="<?php echo esc_url( $image ); ?>">
    <?php
}
add_action( 'wp_head', 'logishift_seo_meta', 1 );

/**
 * Disable canonical redirects only for category URLs.
 * This prevents ?cat=ID from being redirected to /category/slug/
 * while keeping redirects working for other pages.
 */
function logishift_disable_category_redirect( $redirect_url ) {
    if ( is_category() && strpos( $_SERVER['REQUEST_URI'], '?cat=' ) !== false ) {
        return false;
    }
    return $redirect_url;
}
add_filter( 'redirect_canonical', 'logishift_disable_category_redirect' );

/**
 * Force enable pretty permalinks.
 * This ensures post URLs work correctly.
 */
function logishift_enable_permalinks() {
    $current_structure = get_option( 'permalink_structure' );
    if ( empty( $current_structure ) ) {
        global $wp_rewrite;
        $wp_rewrite->set_permalink_structure( '/%postname%/' );
        update_option( 'rewrite_rules', false );
        $wp_rewrite->flush_rules( true );
    }
}
add_action( 'init', 'logishift_enable_permalinks' );

/**
 * Automatically generate SEO-friendly English slugs from Japanese titles.
 * Uses post ID (e.g., post-123) to ensure clean URLs.
 * Hooked to save_post to ensure ID is available.
 */
function logishift_auto_generate_slug_on_save( $post_id, $post, $update ) {
    // Only process posts
    if ( $post->post_type !== 'post' ) {
        return;
    }

    // Avoid infinite loops
    if ( wp_is_post_revision( $post_id ) || wp_is_post_autosave( $post_id ) ) {
        return;
    }

    // Check if slug is empty, contains Japanese, or is URL-encoded
    $slug = $post->post_name;
    if ( empty( $slug ) || preg_match( '/[ぁ-んァ-ヶー一-龠％]/u', $slug ) || strpos( $slug, '%' ) !== false ) {
        
        // Unhook to prevent infinite loop
        remove_action( 'save_post', 'logishift_auto_generate_slug_on_save', 10, 3 );

        // Update the post slug
        wp_update_post( array(
            'ID'        => $post_id,
            'post_name' => 'post-' . $post_id,
        ) );

        // Re-hook
        add_action( 'save_post', 'logishift_auto_generate_slug_on_save', 10, 3 );
    }
}
add_action( 'save_post', 'logishift_auto_generate_slug_on_save', 10, 3 );

/**
 * Sanitize post slugs to prevent Japanese characters in URLs.
 * Generates clean English slugs from Japanese titles.
 */
function logishift_sanitize_post_slug( $slug, $post_ID, $post_status, $post_type ) {
    // Only process posts, not pages or other post types
    if ( $post_type !== 'post' ) {
        return $slug;
    }

    // If slug is empty or contains Japanese characters
    if ( empty( $slug ) || preg_match( '/[ぁ-んァ-ヶー一-龠]/u', $slug ) ) {
        // Get the post title
        $post = get_post( $post_ID );
        if ( $post ) {
            // Generate slug from post ID and first few words of title
            $title_words = explode( ' ', $post->post_title );
            $slug = 'post-' . $post_ID;
        }
    }

    return $slug;
}
add_filter( 'wp_unique_post_slug', 'logishift_sanitize_post_slug', 10, 4 );

/**
 * Register custom meta fields for REST API.
 * This exposes the AI structured summary to the API.
 */
function logishift_register_meta() {
    register_post_meta( 'post', 'ai_structured_summary', array(
        'show_in_rest' => true,
        'single'       => true,
        'type'         => 'string',
        'auth_callback' => '__return_true'
    ) );
}
add_action( 'init', 'logishift_register_meta' );

/**
 * Remove prefixes from archive titles.
 */
function logishift_archive_title( $title ) {
    if ( is_category() ) {
        $title = single_cat_title( '', false );
    } elseif ( is_tag() ) {
        $title = single_tag_title( '', false );
    } elseif ( is_author() ) {
        $title = '<span class="vcard">' . get_the_author() . '</span>';
    } elseif ( is_post_type_archive() ) {
        $title = post_type_archive_title( '', false );
    } elseif ( is_tax() ) {
        $title = single_term_title( '', false );
    }
    return $title;
}
add_filter( 'get_the_archive_title', 'logishift_archive_title' );

/**
 * View Controller for Popular Articles.
 */
require get_template_directory() . '/inc/view-controller.php';

/**
 * Initialize Popular Articles DB Table.
 * Runs on init to check if table needs creation/update.
 */
function logishift_initialize_popular_articles() {
    $current_version = get_option( 'logishift_view_table_version' );
    if ( version_compare( $current_version, '1.0.0', '<' ) ) {
        logishift_create_view_table();
    }
}
add_action( 'init', 'logishift_initialize_popular_articles' );

/**
 * Register REST API endpoint for Popular Posts
 */
add_action( 'rest_api_init', function () {
    register_rest_route( 'logishift/v1', '/popular-posts', array(
        'methods' => 'GET',
        'callback' => 'logishift_api_get_popular_posts',
        'permission_callback' => '__return_true', // Public access allowed
    ) );
} );

/**
 * REST API Callback for Popular Posts
 */
function logishift_api_get_popular_posts( $request ) {
    $days = $request->get_param( 'days' );
    $limit = $request->get_param( 'limit' );
    
    if ( ! $days ) $days = 7;
    if ( ! $limit ) $limit = 20;

    // Use view controller function (make sure it's loaded)
    if ( ! function_exists( 'logishift_get_popular_posts' ) ) {
        return new WP_Error( 'internal_server_error', 'View controller not loaded', array( 'status' => 500 ) );
    }

    $popular_posts = logishift_get_popular_posts( $days, $limit );
    
    $data = array();
    foreach ( $popular_posts as $post ) {
        // Format similar to standard WP REST API for compatibility
        $meta = get_post_meta($post->ID, 'ai_structured_summary', true);
        
        $data[] = array(
            'id' => $post->ID,
            'date' => $post->post_date,
            'link' => get_permalink( $post->ID ),
            'title' => array( 'rendered' => $post->post_title ),
            'excerpt' => array( 'rendered' => $post->post_excerpt ), // Raw excerpt
            'meta' => $meta ? array('ai_structured_summary' => $meta) : array(),
            'views' => $post->views // Extra field
        );
    }

    return $data;
}


/**
 * ==============================================================================
 * SEO Optimizations
 * ==============================================================================
 */

/**
 * 1. Feed Noindex
 * Add X-Robots-Tag: noindex, follow to all feed responses.
 */
function logishift_noindex_feeds() {
    if ( is_feed() ) {
        header( 'X-Robots-Tag: noindex, follow', true );
    }
}
add_action( 'template_redirect', 'logishift_noindex_feeds' );

/**
 * 2. Head Cleanup
 * Remove unnecessary meta tags generated by WordPress.
 */
function logishift_cleanup_head() {
    remove_action( 'wp_head', 'wp_generator' );
    remove_action( 'wp_head', 'wlwmanifest_link' );
    remove_action( 'wp_head', 'rsd_link' );
    remove_action( 'wp_head', 'wp_shortlink_wp_head' );
    // Remove adjacent posts links (prev/next) only if not strictly needed for navigational SEO
    // Keeping them is usually fine, but removing declutters. Let's keep them for now.
}
add_action( 'init', 'logishift_cleanup_head' );

/**
 * 3. Pagination Canonical Fix
 * Ensure paged archives point to their own URL, not the first page.
 */
function logishift_filter_canonical( $canonical ) {
    if ( is_paged() ) {
        $canonical = get_pagenum_link( get_query_var( 'paged' ) );
    }
    return $canonical;
}
add_filter( 'get_canonical_url', 'logishift_filter_canonical' );

/**
 * 4. JSON-LD Schema Markup
 */
function logishift_json_ld() {
    if ( is_admin() || is_feed() ) {
        return;
    }

    $schema = array();
    
    // BreadcrumbList (Global)
    $breadcrumbs = array(
        '@context' => 'https://schema.org',
        '@type'    => 'BreadcrumbList',
        'itemListElement' => array(
            array(
                '@type' => 'ListItem',
                'position' => 1,
                'name' => get_bloginfo( 'name' ),
                'item' => home_url()
            )
        )
    );

    if ( is_singular() ) {
        $categories = get_the_category();
        if ( ! empty( $categories ) ) {
            $breadcrumbs['itemListElement'][] = array(
                '@type' => 'ListItem',
                'position' => 2,
                'name' => $categories[0]->name,
                'item' => get_category_link( $categories[0]->term_id )
            );
            $breadcrumbs['itemListElement'][] = array(
                '@type' => 'ListItem',
                'position' => 3,
                'name' => get_the_title(),
                'item' => get_permalink()
            );
        } else {
             $breadcrumbs['itemListElement'][] = array(
                '@type' => 'ListItem',
                'position' => 2,
                'name' => get_the_title(),
                'item' => get_permalink()
            );
        }
    } elseif ( is_category() ) {
         $breadcrumbs['itemListElement'][] = array(
            '@type' => 'ListItem',
            'position' => 2,
            'name' => single_cat_title( '', false ),
            'item' => get_category_link( get_queried_object_id() )
        );
    }

    $schema[] = $breadcrumbs;

    // Article Schema (Singular Posts)
    if ( is_single() ) {
        global $post;
        
        // Use AI Summary if available, else extract
        $summary = get_post_meta( $post->ID, 'ai_structured_summary', true );
        if ( empty( $summary ) ) {
            $summary = has_excerpt() ? get_the_excerpt() : wp_trim_words( $post->post_content, 120, '...' );
        }

        // Image
        $image_url = has_post_thumbnail() ? get_the_post_thumbnail_url( $post->ID, 'full' ) : get_template_directory_uri() . '/assets/images/hero-bg.png';

        $article = array(
            '@context'      => 'https://schema.org',
            '@type'         => 'Article',
            'headline'      => get_the_title(),
            'description'   => wp_strip_all_tags( $summary ),
            'image'         => array( $image_url ),
            'datePublished' => get_the_date( 'c' ),
            'dateModified'  => get_the_modified_date( 'c' ),
            'author'        => array(
                '@type' => 'Organization',
                'name'  => get_bloginfo( 'name' ),
                'url'   => home_url()
            ),
            'publisher'     => array(
                '@type' => 'Organization',
                'name'  => get_bloginfo( 'name' ),
                'logo'  => array(
                    '@type' => 'ImageObject',
                    'url'   => get_template_directory_uri() . '/assets/images/logo.svg' // Assuming vector logo, might need png for strict schema sometimes
                )
            ),
            'mainEntityOfPage' => array(
                '@type' => 'WebPage',
                '@id'   => get_permalink()
            )
        );
        $schema[] = $article;
    }

    // Output
    foreach ( $schema as $entity ) {
        echo '<script type="application/ld+json">' . json_encode( $entity, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
    }
}
add_action( 'wp_head', 'logishift_json_ld' );


/**
 * 5. Custom XML Sitemap
 * Generates a lightweight XML sitemap at /sitemap.xml
 */
function logishift_sitemap_init() {
    add_rewrite_rule( 'sitemap\.xml$', 'index.php?logishift_sitemap=1', 'top' );
}
add_action( 'init', 'logishift_sitemap_init' );

function logishift_sitemap_query_vars( $vars ) {
    $vars[] = 'logishift_sitemap';
    return $vars;
}
add_filter( 'query_vars', 'logishift_sitemap_query_vars' );

function logishift_sitemap_render() {
    if ( get_query_var( 'logishift_sitemap' ) ) {
        header( 'Content-Type: application/xml; charset=utf-8' );
        echo '<?xml version="1.0" encoding="UTF-8"?>';
        ?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <!-- Home -->
            <url>
                <loc><?php echo esc_url( home_url( '/' ) ); ?></loc>
                <lastmod><?php echo date( 'c' ); ?></lastmod>
                <changefreq>daily</changefreq>
                <priority>1.0</priority>
            </url>

            <!-- Pages -->
            <?php
            $pages = get_posts( array(
                'numberposts' => 100,
                'post_type'   => 'page',
                'post_status' => 'publish',
            ) );
            foreach ( $pages as $p ) : ?>
            <url>
                <loc><?php echo esc_url( get_permalink( $p->ID ) ); ?></loc>
                <lastmod><?php echo get_the_modified_date( 'c', $p->ID ); ?></lastmod>
                <changefreq>daily</changefreq>
                <priority>0.8</priority>
            </url>
            <?php endforeach; ?>

            <!-- Categories -->
            <?php
            $categories = get_categories();
            foreach ( $categories as $cat ) : ?>
            <url>
                <loc><?php echo esc_url( get_category_link( $cat->term_id ) ); ?></loc>
                <changefreq>daily</changefreq>
                <priority>0.6</priority>
            </url>
            <?php endforeach; ?>

            <!-- Posts -->
            <?php
            $posts = get_posts( array(
                'numberposts' => 1000,
                'post_type'   => 'post',
                'post_status' => 'publish',
                'orderby'     => 'date',
                'order'       => 'DESC',
            ) );
            foreach ( $posts as $p ) : ?>
            <url>
                <loc><?php echo esc_url( get_permalink( $p->ID ) ); ?></loc>
                <lastmod><?php echo get_the_modified_date( 'c', $p->ID ); ?></lastmod>
                <changefreq>monthly</changefreq>
                <priority>0.5</priority>
            </url>
            <?php endforeach; ?>

        </urlset>
        <?php
        exit;
    }
}
add_action( 'template_redirect', 'logishift_sitemap_render' );

/**
 * Flush rewrite rules if sitemap rule is missing.
 * Runs only once per admin pageload if needed.
 */
function logishift_check_sitemap_rules() {
    $rules = get_option( 'rewrite_rules' );
    if ( ! isset( $rules['sitemap\.xml$'] ) ) {
        global $wp_rewrite;
        $wp_rewrite->flush_rules();
    }
}
add_action( 'admin_init', 'logishift_check_sitemap_rules' );

/**
 * 6. Disable Default WP Sitemap
 * Prevent conflict with our custom sitemap.xml
 */
add_filter( 'wp_sitemaps_enabled', '__return_false' );


