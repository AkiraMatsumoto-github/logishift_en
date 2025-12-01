<?php
/**
 * The template for displaying the front page
 * SEO-optimized design based on content_strategy.md
 *
 * @package LogiShift
 */

get_header();
?>

<main id="primary" class="site-main">

	<!-- Hero Section -->
	<section class="hero-section">
		<div class="container">
			<div class="hero-content">
				<h1 class="hero-title"><?php esc_html_e( '物流DXで未来を創る LogiShift', 'logishift' ); ?></h1>
				<p class="hero-description"><?php esc_html_e( '倉庫管理・コスト削減・2024年問題対策まで。物流担当者と経営層のための実践的な課題解決メディア。', 'logishift' ); ?></p>
				<a href="#latest-articles" class="button hero-cta"><?php esc_html_e( '最新記事を読む', 'logishift' ); ?></a>
			</div>
		</div>
	</section>

	<!-- Featured Articles -->
	<section id="latest-articles" class="featured-articles-section">
		<div class="container">
			<div class="section-header">
				<h2 class="section-title"><?php esc_html_e( '注目記事', 'logishift' ); ?></h2>
			</div>

			<div class="featured-grid">
				<?php
				$featured_args = array(
					'post_type'      => 'post',
					'posts_per_page' => 3,
					'orderby'        => 'date',
					'order'          => 'DESC',
				);
				$featured_query = new WP_Query( $featured_args );

				if ( $featured_query->have_posts() ) :
					while ( $featured_query->have_posts() ) :
						$featured_query->the_post();
						?>
						<article id="post-<?php the_ID(); ?>" <?php post_class( 'featured-card' ); ?>>
							<div class="featured-thumbnail">
								<?php if ( has_post_thumbnail() ) : ?>
									<a href="<?php the_permalink(); ?>"><?php the_post_thumbnail( 'large' ); ?></a>
								<?php else : ?>
									<a href="<?php the_permalink(); ?>"><div class="no-image"></div></a>
								<?php endif; ?>
							</div>
							<div class="featured-content">
								<div class="article-meta">
									<?php
									$categories = get_the_category();
									if ( ! empty( $categories ) ) :
										?>
										<span class="cat-label"><?php echo esc_html( $categories[0]->name ); ?></span>
									<?php endif; ?>
									<span class="posted-on"><?php echo get_the_date(); ?></span>
								</div>
								<h3 class="featured-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
								<div class="featured-excerpt"><?php echo wp_trim_words( get_the_excerpt(), 30 ); ?></div>
							</div>
						</article>
						<?php
					endwhile;
					wp_reset_postdata();
				endif;
				?>
			</div>
		</div>
	</section>

	<?php
	// Category sections based on content_strategy.md
	$category_sections = array(
		array(
			'slug'        => 'logistics-dx',
			'name'        => '物流DX・トレンド',
			'description' => '物流業界の最新動向、2024年問題、DX推進の実践的ノウハウ',
		),
		array(
			'slug'        => 'warehouse-management',
			'name'        => '倉庫管理・WMS',
			'description' => 'WMS導入、在庫管理、ピッキング効率化の成功事例',
		),
		array(
			'slug'        => 'transportation',
			'name'        => '輸配送・TMS',
			'description' => '配車計画、ラストワンマイル、動態管理の最適化手法',
		),
		array(
			'slug'        => 'material-handling',
			'name'        => 'マテハン・ロボット',
			'description' => '自動倉庫、AGV/AMR、RFID導入の最新トレンド',
		),
		array(
			'slug'        => 'supply-chain',
			'name'        => 'サプライチェーン',
			'description' => 'SCM戦略、調達最適化、国際物流のベストプラクティス',
		),
		array(
			'slug'        => 'case-studies',
			'name'        => '事例・インタビュー',
			'description' => '企業の成功事例、現場インタビュー、導入効果の実績',
		),
	);

	foreach ( $category_sections as $cat_section ) :
		$cat_obj = get_category_by_slug( $cat_section['slug'] );
		if ( ! $cat_obj ) {
			continue;
		}
		?>
		<section class="category-section category-<?php echo esc_attr( $cat_section['slug'] ); ?>">
			<div class="container">
				<div class="section-header">
					<div class="section-header-content">
						<h2 class="section-title"><?php echo esc_html( $cat_section['name'] ); ?></h2>
						<p class="section-description"><?php echo esc_html( $cat_section['description'] ); ?></p>
					</div>
					<a href="<?php echo esc_url( get_category_link( $cat_obj ) ); ?>" class="section-link"><?php esc_html_e( '一覧へ', 'logishift' ); ?> →</a>
				</div>

				<div class="article-grid">
					<?php
					$cat_args = array(
						'category_name'  => $cat_section['slug'],
						'posts_per_page' => 3,
						'orderby'        => 'date',
						'order'          => 'DESC',
					);
					$cat_query = new WP_Query( $cat_args );

					if ( $cat_query->have_posts() ) :
						while ( $cat_query->have_posts() ) :
							$cat_query->the_post();
							?>
							<article id="post-<?php the_ID(); ?>" <?php post_class( 'article-card' ); ?>>
								<div class="article-thumbnail">
									<?php if ( has_post_thumbnail() ) : ?>
										<a href="<?php the_permalink(); ?>"><?php the_post_thumbnail( 'medium' ); ?></a>
									<?php else : ?>
										<a href="<?php the_permalink(); ?>"><div class="no-image"></div></a>
									<?php endif; ?>
								</div>
								<div class="article-content">
									<div class="article-meta">
										<span class="posted-on"><?php echo get_the_date(); ?></span>
									</div>
									<h3 class="article-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
								</div>
							</article>
							<?php
						endwhile;
						wp_reset_postdata();
					else :
						?>
						<p class="no-posts"><?php esc_html_e( '記事がまだありません。', 'logishift' ); ?></p>
					<?php endif; ?>
				</div>
			</div>
		</section>
		<?php
	endforeach;
	?>

	<!-- Global Trends Section with Regional Filtering -->
	<section class="global-trends-section">
		<div class="container">
			<div class="section-header">
				<div class="section-header-content">
					<h2 class="section-title">🌍 <?php esc_html_e( '海外トレンド', 'logishift' ); ?></h2>
					<p class="section-description"><?php esc_html_e( '米国・欧州・アジアの最新物流DX事例と日本への示唆', 'logishift' ); ?></p>
				</div>
			</div>

			<!-- Regional Filter Tabs -->
			<div class="region-filter-tabs">
				<button class="region-tab active" data-region="all"><?php esc_html_e( 'すべて', 'logishift' ); ?></button>
				<button class="region-tab" data-region="usa">🇺🇸 <?php esc_html_e( 'アメリカ', 'logishift' ); ?></button>
				<button class="region-tab" data-region="europe">🇪🇺 <?php esc_html_e( 'ヨーロッパ', 'logishift' ); ?></button>
				<button class="region-tab" data-region="china">🇨🇳 <?php esc_html_e( '中国', 'logishift' ); ?></button>
				<button class="region-tab" data-region="southeast-asia">🌏 <?php esc_html_e( '東南アジア', 'logishift' ); ?></button>
			</div>

			<div class="global-articles-container">
				<?php
				// Get all global trend articles with regional tags
				$global_args = array(
					'category_name'  => 'news-global',
					'posts_per_page' => 12,
					'orderby'        => 'date',
					'order'          => 'DESC',
				);
				$global_query = new WP_Query( $global_args );

				if ( $global_query->have_posts() ) :
					?>
					<div class="article-grid global-grid">
						<?php
						while ( $global_query->have_posts() ) :
							$global_query->the_post();
							$post_tags = get_the_tags();
							$region_tags = array();
							
							if ( $post_tags ) {
								foreach ( $post_tags as $tag ) {
									if ( in_array( $tag->slug, array( 'usa', 'europe', 'china', 'southeast-asia', 'japan', 'global' ) ) ) {
										$region_tags[] = $tag->slug;
									}
								}
							}
							
							$region_data = ! empty( $region_tags ) ? implode( ' ', $region_tags ) : 'all';
							?>
							<article id="post-<?php the_ID(); ?>" <?php post_class( 'article-card global-article' ); ?> data-regions="<?php echo esc_attr( $region_data ); ?>">
								<div class="article-thumbnail">
									<?php if ( has_post_thumbnail() ) : ?>
										<a href="<?php the_permalink(); ?>"><?php the_post_thumbnail( 'medium' ); ?></a>
									<?php else : ?>
										<a href="<?php the_permalink(); ?>"><div class="no-image"></div></a>
									<?php endif; ?>
								</div>
								<div class="article-content">
									<div class="article-meta">
										<?php if ( ! empty( $region_tags ) ) : ?>
											<span class="region-label"><?php echo esc_html( $region_tags[0] ); ?></span>
										<?php endif; ?>
										<span class="posted-on"><?php echo get_the_date(); ?></span>
									</div>
									<h3 class="article-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
								</div>
							</article>
							<?php
						endwhile;
						wp_reset_postdata();
						?>
					</div>
				<?php else : ?>
					<p class="no-posts"><?php esc_html_e( '記事がまだありません。', 'logishift' ); ?></p>
				<?php endif; ?>
			</div>
		</div>
	</section>

	<!-- Theme-based Tag Sections -->
	<section class="theme-tags-section">
		<div class="container">
			<div class="section-header">
				<h2 class="section-title"><?php esc_html_e( '課題別で探す', 'logishift' ); ?></h2>
			</div>

			<?php
			$theme_tags = array(
				array(
					'slug' => 'cost-reduction',
					'name' => 'コスト削減',
					'icon' => '💰',
				),
				array(
					'slug' => 'labor-shortage',
					'name' => '人手不足対策',
					'icon' => '👥',
				),
				array(
					'slug' => 'quality-improvement',
					'name' => '品質向上・誤出荷防止',
					'icon' => '✓',
				),
			);

			foreach ( $theme_tags as $theme_tag ) :
				?>
				<div class="theme-tag-block">
					<h3 class="theme-tag-title">
						<span class="theme-icon"><?php echo $theme_tag['icon']; ?></span>
						<?php echo esc_html( $theme_tag['name'] ); ?>
					</h3>
					<div class="theme-articles-scroll">
						<?php
						$tag_args = array(
							'tag'            => $theme_tag['slug'],
							'posts_per_page' => 4,
							'orderby'        => 'date',
							'order'          => 'DESC',
						);
						$tag_query = new WP_Query( $tag_args );

						if ( $tag_query->have_posts() ) :
							while ( $tag_query->have_posts() ) :
								$tag_query->the_post();
								?>
								<article class="theme-article-card">
									<div class="theme-article-thumbnail">
										<?php if ( has_post_thumbnail() ) : ?>
											<a href="<?php the_permalink(); ?>"><?php the_post_thumbnail( 'thumbnail' ); ?></a>
										<?php endif; ?>
									</div>
									<div class="theme-article-content">
										<h4 class="theme-article-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h4>
										<span class="theme-article-date"><?php echo get_the_date(); ?></span>
									</div>
								</article>
								<?php
							endwhile;
							wp_reset_postdata();
						endif;
						?>
					</div>
					<a href="<?php echo esc_url( get_tag_link( get_term_by( 'slug', $theme_tag['slug'], 'post_tag' ) ) ); ?>" class="theme-tag-link"><?php esc_html_e( 'もっと見る', 'logishift' ); ?> →</a>
				</div>
				<?php
			endforeach;
			?>
		</div>
	</section>

	<!-- CTA Section -->
	<section class="cta-section">
		<div class="container">
			<div class="cta-content">
				<h2><?php esc_html_e( 'LogiShiftについて', 'logishift' ); ?></h2>
				<p><?php esc_html_e( 'LogiShiftは、物流担当者と経営層のための課題解決メディアです。現場のノウハウから最新のDX事例まで、ビジネスを加速させる情報をお届けします。', 'logishift' ); ?></p>
				<div class="cta-buttons">
					<a href="<?php echo esc_url( home_url( '/about/' ) ); ?>" class="button outline"><?php esc_html_e( '運営者情報', 'logishift' ); ?></a>
					<a href="<?php echo esc_url( get_permalink( get_option( 'page_for_posts' ) ) ); ?>" class="button"><?php esc_html_e( '記事一覧', 'logishift' ); ?></a>
				</div>
			</div>
		</div>
	</section>

</main>

<script>
// Regional filter functionality
document.addEventListener('DOMContentLoaded', function() {
	const regionTabs = document.querySelectorAll('.region-tab');
	const globalArticles = document.querySelectorAll('.global-article');

	regionTabs.forEach(tab => {
		tab.addEventListener('click', function() {
			const selectedRegion = this.getAttribute('data-region');
			
			// Update active tab
			regionTabs.forEach(t => t.classList.remove('active'));
			this.classList.add('active');
			
			// Filter articles
			globalArticles.forEach(article => {
				const articleRegions = article.getAttribute('data-regions');
				
				if (selectedRegion === 'all' || articleRegions.includes(selectedRegion)) {
					article.style.display = 'block';
				} else {
					article.style.display = 'none';
				}
			});
		});
	});
});
</script>

<?php
get_footer();
