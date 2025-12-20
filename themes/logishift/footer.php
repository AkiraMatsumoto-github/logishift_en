<?php
/**
 * The template for displaying the footer
 *
 * @package LogiShift
 */
?>

	<footer id="colophon" class="site-footer">
		<div class="container">
			<div class="footer-content">
				<!-- Footer Columns -->
				<div class="footer-columns">
					<!-- About Column -->
					<div class="footer-column">
						<h3 class="footer-title">LogiShift Global</h3>
						<p class="footer-description">Leading media for logistics professionals offering global insights on Cost Reduction, DX, and Supply Chain Management.</p>
					</div>

					<!-- Categories Column -->
					<div class="footer-column">
						<h3 class="footer-title">Categories</h3>
						<ul class="footer-links">
							<li><a href="<?php echo esc_url( home_url( '/category/global-trends/' ) ); ?>">Global Trends</a></li>
							<li><a href="<?php echo esc_url( home_url( '/category/technology-dx/' ) ); ?>">Technology & DX</a></li>
							<li><a href="<?php echo esc_url( home_url( '/category/cost-efficiency/' ) ); ?>">Cost & Efficiency</a></li>
							<li><a href="<?php echo esc_url( home_url( '/category/scm/' ) ); ?>">Supply Chain Management</a></li>
						</ul>
					</div>

					<!-- More Categories Column -->
					<div class="footer-column">
						<h3 class="footer-title">Explore</h3>
						<ul class="footer-links">
							<li><a href="<?php echo esc_url( home_url( '/category/case-studies/' ) ); ?>">Case Studies</a></li>
							<li><a href="<?php echo esc_url( home_url( '/category/startups/' ) ); ?>">Logistics Startups</a></li>
						</ul>
					</div>

					<!-- Info Column -->
					<div class="footer-column">
						<h3 class="footer-title">Information</h3>
						<ul class="footer-links">
							<li><a href="<?php echo esc_url( home_url( '/about/' ) ); ?>">About Us</a></li>
							<li><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">Contact</a></li>
							<li><a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">Privacy Policy</a></li>
						</ul>
					</div>
				</div>

				<!-- Footer Bottom -->
				<div class="footer-bottom">
					<p class="copyright">&copy; <?php echo date( 'Y' ); ?> LogiShift. All rights reserved.</p>
				</div>
			</div>
		</div>
	</footer>

<?php wp_footer(); ?>

</body>
</html>
