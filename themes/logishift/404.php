<?php
/**
 * The template for displaying 404 pages (not found)
 *
 * @package LogiShift
 */

get_header();
?>

<main id="primary" class="site-main">
	<div class="container">
		
		<div class="error-404 not-found" style="text-align: center; padding: var(--spacing-3xl) 0;">
			<header class="page-header">
				<h1 class="page-title" style="font-size: 6rem; color: var(--color-tech-blue); margin-bottom: var(--spacing-md);">404</h1>
				<h2 class="page-subtitle" style="font-size: 1.5rem; margin-bottom: var(--spacing-xl);"><?php esc_html_e( 'Page Not Found.', 'logishift' ); ?></h2>
			</header>

			<div class="page-content" style="max-width: 600px; margin: 0 auto;">
				<p style="margin-bottom: var(--spacing-xl);"><?php esc_html_e( 'The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.', 'logishift' ); ?></p>

				<div style="margin-bottom: var(--spacing-2xl);">
					<?php get_search_form(); ?>
				</div>

				<a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="button primary"><?php esc_html_e( 'Back to Home', 'logishift' ); ?></a>
			</div>
		</div>

	</div>
</main>

<?php
get_footer();
