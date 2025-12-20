<?php
/**
 * The header for our theme
 *
 * @package LogiShift
 */
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="profile" href="https://gmpg.org/xfn/11">

	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div id="page" class="site">
	<a class="skip-link screen-reader-text" href="#primary"><?php esc_html_e( 'Skip to content', 'logishift' ); ?></a>

	<header id="masthead" class="site-header">
		<div class="container header-container">
			<div class="site-branding">
				<?php
				the_custom_logo();
				if ( is_front_page() && is_home() ) :
					?>
					<h1 class="site-title">
						<a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">
							<img src="<?php echo get_template_directory_uri(); ?>/assets/images/logo.svg" alt="<?php bloginfo( 'name' ); ?>" style="height: 40px; width: auto;">
						</a>
					</h1>
					<?php
				else :
					?>
					<p class="site-title">
						<a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">
							<img src="<?php echo get_template_directory_uri(); ?>/assets/images/logo.svg" alt="<?php bloginfo( 'name' ); ?>" style="height: 40px; width: auto;">
						</a>
					</p>
					<?php
				endif;
				?>
				<?php
				$logishift_description = get_bloginfo( 'description', 'display' );
				if ( $logishift_description || is_customize_preview() ) :
					?>
					<p class="site-description"><?php echo $logishift_description; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></p>
				<?php endif; ?>
			</div><!-- .site-branding -->

			<nav id="site-navigation" class="main-navigation">
				<button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false">
					<span class="screen-reader-text"><?php esc_html_e( 'Menu', 'logishift' ); ?></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</button>
				<ul id="primary-menu" class="menu">
					<?php
					if ( has_nav_menu( 'menu-1' ) ) {
						wp_nav_menu(
							array(
								'theme_location' => 'menu-1',
								'menu_id'        => 'primary-menu',
								'container'      => false,
								'items_wrap'     => '%3$s',
							)
						);
					} else {
						?>
						<li><a href="<?php echo esc_url( home_url( '/category/global-trends/' ) ); ?>"><?php esc_html_e( 'Global Trends', 'logishift' ); ?></a></li>
						<li><a href="<?php echo esc_url( home_url( '/category/technology-dx/' ) ); ?>"><?php esc_html_e( 'Technology & DX', 'logishift' ); ?></a></li>
						<li><a href="<?php echo esc_url( home_url( '/category/cost-efficiency/' ) ); ?>"><?php esc_html_e( 'Cost & Efficiency', 'logishift' ); ?></a></li>
						<li><a href="<?php echo esc_url( home_url( '/category/scm/' ) ); ?>"><?php esc_html_e( 'SCM', 'logishift' ); ?></a></li>
						<li><a href="<?php echo esc_url( home_url( '/category/case-studies/' ) ); ?>"><?php esc_html_e( 'Case Studies', 'logishift' ); ?></a></li>
						<?php
					}
					?>
				</ul>
			</nav><!-- #site-navigation -->
		</div>
	</header><!-- #masthead -->
