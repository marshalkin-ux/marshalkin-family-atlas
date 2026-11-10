# Editorial longread · 2026-11-10

Direction: contemporary documentary editorial design in Russian, retaining warm paper and archival images. Onest sans display/body, Prata literary quotations; locally embedded fonts. Full-viewport opening, 4 image-led transitions, narrow reading columns, large pull quotes and differentiated data surfaces. Existing chronology and all 903 cards remain intact. No new historical claims.

Implementation:
1. Add editorial-fonts.css with Cyrillic fonts/licenses.
2. Add editorial.css, editorial.js and editorial_build.py as final presentation layer after story_revision. Scenes inserted after existing chronology script; no duplicated ids or replacement of genealogy data.
3. Parallax uses passive scroll + requestAnimationFrame on visible scenes only, capped movement, disabled on mobile and reduced motion. Content visible without animation, keyboard links and source citations preserved.
4. Test font loading, scenes order, parallax/reduced motion, mobile no overflow, full tree and portrait. Inspect desktop/mobile screenshots.
5. Build, commit sources and index.html, push, verify deployment and live site.
