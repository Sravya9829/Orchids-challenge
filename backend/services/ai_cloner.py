import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Dict, Optional, List
import json
import re
import asyncio

load_dotenv()

class LayoutAwareCloner:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("âš ï¸ GEMINI_API_KEY not found in environment variables")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("âœ… Gemini AI service initialized for layout-aware cloning")
    
    async def clone_website(self, scraped_data: Dict, url: str) -> str:
        """Generate layout-aware website clone with proper structure and flow"""
        
        if not self.model:
            print("âš ï¸ AI model not available, using layout-aware fallback")
            return self._create_layout_aware_fallback(scraped_data, url)
        
        try:
            # Extract structured data
            layout_structure = scraped_data.get("layout_structure", {})
            content_sections = scraped_data.get("content_sections", {})
            design_system = scraped_data.get("design_system", {})
            structured_content = scraped_data.get("structured_content", {})
            navigation_analysis = scraped_data.get("navigation_analysis", {})
            
            print(f"ðŸ—ï¸ Layout type: {layout_structure.get('page_type', 'unknown')}")
            print(f"ðŸ“‘ Content sections: {len(content_sections.get('main_content', {}).get('sections', []))}")
            print(f"ðŸ§­ Navigation items: {len(navigation_analysis.get('primary_nav', []))}")
            
            # Build layout-aware prompt
            prompt = self._build_layout_aware_prompt(
                layout_structure, content_sections, design_system, 
                structured_content, navigation_analysis, url
            )
            
            print("ðŸ¤– Generating layout-aware clone with AI...")
            
            # Generate with structure-focused settings
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 16384,
                }
            )
            
            # Extract and validate HTML
            html_result = self._extract_clean_html(response.text)
            
            if self._is_well_structured_html(html_result, structured_content):
                print("âœ… Generated well-structured HTML clone")
                return html_result
            else:
                print("âš ï¸ AI result not well-structured, using layout-aware fallback")
                return self._create_layout_aware_fallback(scraped_data, url)
                
        except Exception as e:
            print(f"âŒ Layout-aware AI cloning failed: {e}")
            return self._create_layout_aware_fallback(scraped_data, url)
    
    def _build_layout_aware_prompt(self, layout_structure: Dict, content_sections: Dict, 
                                 design_system: Dict, structured_content: Dict, 
                                 navigation_analysis: Dict, url: str) -> str:
        """Build prompt focused on proper layout structure and content flow"""
        
        prompt = f"""Create a well-structured, professional website that recreates {url} with proper layout flow and visual hierarchy.

CRITICAL REQUIREMENTS:
- Return ONLY complete HTML code (no explanations, no markdown blocks)
- Start with <!DOCTYPE html> and end with </html>
- Use proper CSS Grid/Flexbox for layout structure
- Maintain logical content flow and visual hierarchy
- Create a cohesive, professional design

LAYOUT STRUCTURE:
Page Type: {layout_structure.get('page_type', 'content_focused')}
Layout Flow: {layout_structure.get('layout_flow', 'vertical')}
Container Width: {layout_structure.get('container_info', {}).get('maxWidth', '1200px')}

CONTENT STRUCTURE:
{self._format_content_structure(content_sections, structured_content)}

NAVIGATION SYSTEM:
{self._format_navigation_system(navigation_analysis)}

DESIGN SYSTEM:
{self._format_design_system(design_system)}

LAYOUT IMPLEMENTATION REQUIREMENTS:

1. STRUCTURAL HIERARCHY:
   - Header: Logo/brand + primary navigation
   - Main: Content sections in logical order
   - Footer: Secondary links and information
   - Use semantic HTML5 elements (header, nav, main, section, footer)

2. CONTENT FLOW:
   - Maintain vertical content flow with proper spacing
   - Group related content in sections
   - Use consistent typography hierarchy (h1 > h2 > h3 > p)
   - Proper spacing between sections (2-3rem)

3. LAYOUT SYSTEM:
   - Use CSS Grid for main page layout
   - Use Flexbox for navigation and component layout
   - Responsive design with proper breakpoints
   - Container with max-width for content

4. VISUAL HIERARCHY:
   - Large, prominent main heading
   - Clear section divisions
   - Consistent button styling
   - Proper color contrast and readability

5. MODERN DESIGN:
   - Clean, minimal aesthetic
   - Subtle shadows and borders
   - Smooth hover transitions
   - Professional color scheme

Generate a complete, well-structured HTML page that flows naturally and looks professional:"""

        return prompt
    
    def _format_content_structure(self, content_sections: Dict, structured_content: Dict) -> str:
        """Format content structure for AI prompt"""
        
        structure_info = []
        
        # Page title and main heading
        page_title = structured_content.get('page_title', 'Website')
        main_heading = structured_content.get('main_heading', page_title)
        
        structure_info.append(f"Page Title: {page_title}")
        structure_info.append(f"Main Heading: {main_heading}")
        
        # Meta description
        meta_desc = structured_content.get('meta_description', '')
        if meta_desc:
            structure_info.append(f"Description: {meta_desc}")
        
        # Content sections in order
        main_content = content_sections.get('main_content', {})
        sections = main_content.get('sections', [])
        
        if sections:
            structure_info.append("CONTENT SECTIONS (in order):")
            for i, section in enumerate(sections[:8]):  # Limit sections
                section_type = section.get('type', 'content')
                heading = section.get('heading', {})
                content = section.get('content', [])
                
                if heading:
                    structure_info.append(f"  {i+1}. {heading.get('level', 'h2').upper()}: {heading.get('text', 'Section Heading')}")
                
                if content:
                    for content_item in content[:2]:  # Limit content per section
                        if len(content_item) > 50:
                            structure_info.append(f"     Content: {content_item[:100]}...")
        
        # Text content
        text_content = structured_content.get('text_content', [])
        if text_content:
            structure_info.append("ADDITIONAL TEXT CONTENT:")
            for text in text_content[:3]:  # Limit additional text
                structure_info.append(f"  - {text[:80]}...")
        
        # Buttons
        buttons = structured_content.get('buttons', [])
        if buttons:
            structure_info.append("BUTTONS/ACTIONS:")
            for button in buttons[:5]:  # Limit buttons
                structure_info.append(f"  - {button.get('text', 'Button')}")
        
        return '\n'.join(structure_info)
    
    def _format_navigation_system(self, navigation_analysis: Dict) -> str:
        """Format navigation system for AI prompt"""
        
        nav_info = []
        
        # Primary navigation
        primary_nav = navigation_analysis.get('primary_nav', [])
        if primary_nav:
            nav_info.append("PRIMARY NAVIGATION:")
            for nav_item in primary_nav[:8]:  # Limit nav items
                text = nav_item.get('text', 'Link')
                is_current = nav_item.get('is_current', False)
                current_indicator = " (CURRENT)" if is_current else ""
                nav_info.append(f"  - {text}{current_indicator}")
        
        # Navigation style
        nav_style = navigation_analysis.get('nav_style', 'horizontal')
        nav_info.append(f"Navigation Style: {nav_style}")
        
        # Breadcrumbs
        breadcrumbs = navigation_analysis.get('breadcrumbs', [])
        if breadcrumbs:
            nav_info.append(f"Breadcrumbs: {' > '.join(breadcrumbs)}")
        
        # Footer navigation
        footer_nav = navigation_analysis.get('footer_nav', [])
        if footer_nav:
            nav_info.append("FOOTER NAVIGATION:")
            for footer_item in footer_nav[:6]:  # Limit footer nav
                nav_info.append(f"  - {footer_item.get('text', 'Footer Link')}")
        
        return '\n'.join(nav_info) if nav_info else "Standard navigation structure"
    
    def _format_design_system(self, design_system: Dict) -> str:
        """Format design system for AI prompt"""
        
        design_info = []
        
        # Colors
        colors = design_system.get('colors', {})
        primary_colors = colors.get('primary', {})
        
        if primary_colors:
            design_info.append("COLOR SCHEME:")
            bg_color = primary_colors.get('background', '#ffffff')
            text_color = primary_colors.get('text', '#333333')
            font_family = primary_colors.get('font_family', 'system-ui, sans-serif')
            
            design_info.append(f"  Background: {bg_color}")
            design_info.append(f"  Text: {text_color}")
            design_info.append(f"  Font Family: {font_family}")
        
        # Typography
        typography = design_system.get('typography', {})
        headings = typography.get('headings', {})
        
        if headings:
            design_info.append("TYPOGRAPHY:")
            for tag, styles in headings.items():
                font_size = styles.get('fontSize', '1rem')
                font_weight = styles.get('fontWeight', 'normal')
                color = styles.get('color', text_color)
                design_info.append(f"  {tag.upper()}: {font_size}, {font_weight}, {color}")
        
        # Components
        components = design_system.get('components', {})
        button_style = components.get('button', {})
        
        if button_style:
            design_info.append("BUTTON STYLE:")
            bg = button_style.get('backgroundColor', '#007bff')
            color = button_style.get('color', '#ffffff')
            border_radius = button_style.get('borderRadius', '4px')
            padding = button_style.get('padding', '12px 24px')
            design_info.append(f"  Background: {bg}, Color: {color}, Radius: {border_radius}, Padding: {padding}")
        
        # Spacing
        spacing = design_system.get('spacing', {})
        if spacing:
            margins = spacing.get('common_margins', [])
            paddings = spacing.get('common_paddings', [])
            
            if margins:
                design_info.append(f"Common Margins: {', '.join(margins[:3])}px")
            if paddings:
                design_info.append(f"Common Paddings: {', '.join(paddings[:3])}px")
        
        return '\n'.join(design_info) if design_info else "Modern, clean design system"
    
    def _extract_clean_html(self, response: str) -> str:
        """Extract clean HTML from AI response"""
        
        # Remove markdown formatting
        cleaned = response.strip()
        
        # Remove code block markers
        cleaned = re.sub(r'```html\n?', '', cleaned)
        cleaned = re.sub(r'```\n?', '', cleaned)
        
        # Look for HTML structure
        if '<!DOCTYPE html>' in cleaned:
            start = cleaned.find('<!DOCTYPE html>')
            end = cleaned.rfind('</html>')
            if end != -1:
                return cleaned[start:end + 7]
        
        elif '<html>' in cleaned:
            start = cleaned.find('<html>')
            end = cleaned.rfind('</html>')
            if end != -1:
                return cleaned[start:end + 7]
        
        return cleaned
    
    def _is_well_structured_html(self, html: str, structured_content: Dict) -> bool:
        """Check if HTML has proper structure and content"""
        
        if len(html) < 2000:  # Minimum length for substantial content
            return False
        
        quality_checks = [
            '<!DOCTYPE html>' in html,
            '<html>' in html and '</html>' in html,
            '<head>' in html and '</head>' in html,
            '<body>' in html and '</body>' in html,
            '<header>' in html or '<nav>' in html,  # Has navigation
            '<main>' in html or '<section>' in html,  # Has main content
            '<style>' in html,  # Has styling
            'display:' in html or 'flex' in html or 'grid' in html,  # Uses modern layout
            html.count('<') > 40,  # Multiple elements
        ]
        
        # Check if it contains actual content
        main_heading = structured_content.get('main_heading', '')
        if main_heading:
            content_match = main_heading.lower()[:30] in html.lower()
            quality_checks.append(content_match)
        
        buttons = structured_content.get('buttons', [])
        if buttons:
            button_texts = [b.get('text', '')[:20] for b in buttons[:2]]
            button_match = any(text.lower() in html.lower() for text in button_texts if text)
            quality_checks.append(button_match)
        
        return sum(quality_checks) >= 8
    
    def _create_layout_aware_fallback(self, scraped_data: Dict, url: str) -> str:
        """Create a well-structured fallback with proper layout"""
        
        # Extract all data
        layout_structure = scraped_data.get("layout_structure", {})
        content_sections = scraped_data.get("content_sections", {})
        design_system = scraped_data.get("design_system", {})
        structured_content = scraped_data.get("structured_content", {})
        navigation_analysis = scraped_data.get("navigation_analysis", {})
        
        # Basic info
        page_title = structured_content.get("page_title", "Website")
        main_heading = structured_content.get("main_heading", page_title)
        meta_description = structured_content.get("meta_description", "")
        
        # Navigation
        primary_nav = navigation_analysis.get("primary_nav", [])
        
        # Content sections
        main_content = content_sections.get("main_content", {})
        sections = main_content.get("sections", [])
        
        # Text content
        text_content = structured_content.get("text_content", [])
        buttons = structured_content.get("buttons", [])
        
        # Design system
        colors = design_system.get("colors", {})
        primary_colors = colors.get("primary", {})
        
        bg_color = primary_colors.get("background", "#ffffff")
        text_color = primary_colors.get("text", "#333333")
        font_family = primary_colors.get("font_family", "system-ui, -apple-system, sans-serif")
        
        # Component styles
        components = design_system.get("components", {})
        button_style = components.get("button", {})
        
        button_bg = button_style.get("backgroundColor", "#0066cc")
        button_text = button_style.get("color", "#ffffff")
        button_radius = button_style.get("borderRadius", "6px")
        button_padding = button_style.get("padding", "12px 24px")
        
        # Build navigation HTML
        nav_html = ""
        if primary_nav:
            nav_items = []
            for nav_item in primary_nav[:6]:  # Limit nav items
                text = nav_item.get('text', 'Link')
                href = nav_item.get('href', '#')
                is_current = nav_item.get('is_current', False)
                current_class = ' aria-current="page"' if is_current else ''
                nav_items.append(f'<a href="{href}" class="nav-link{" current" if is_current else ""}"{current_class}>{text}</a>')
            
            nav_html = f'''
        <nav class="main-nav">
            <div class="nav-container">
                {chr(10).join([f'        {item}' for item in nav_items])}
            </div>
        </nav>'''
        
        # Build content sections HTML
        content_html = ""
        
        # Add main sections
        for i, section in enumerate(sections[:6]):  # Limit sections
            heading = section.get('heading', {})
            content = section.get('content', [])
            
            section_html = f'''
        <section class="content-section">'''
            
            if heading:
                heading_level = heading.get('level', 'h2')
                heading_text = heading.get('text', f'Section {i+1}')
                section_html += f'''
            <{heading_level} class="section-heading">{heading_text}</{heading_level}>'''
            
            # Add content
            if content:
                for content_item in content[:2]:  # Limit content per section
                    section_html += f'''
            <p class="section-content">{content_item}</p>'''
            
            section_html += '''
        </section>'''
            content_html += section_html
        
        # Add additional text content
        for text in text_content[:3]:  # Limit additional content
            content_html += f'''
        <section class="content-section">
            <p class="section-content">{text}</p>
        </section>'''
        
        # Build buttons HTML
        buttons_html = ""
        if buttons:
            button_elements = []
            for button in buttons[:4]:  # Limit buttons
                text = button.get('text', 'Button')
                href = button.get('href', '')
                
                if href:
                    button_elements.append(f'<a href="{href}" class="btn btn-primary">{text}</a>')
                else:
                    button_elements.append(f'<button type="button" class="btn btn-primary">{text}</button>')
            
            buttons_html = f'''
        <section class="cta-section">
            <div class="button-group">
                {chr(10).join([f'            {btn}' for btn in button_elements])}
            </div>
        </section>'''
        
        # Build complete HTML with proper structure
        html_document = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    {f'<meta name="description" content="{meta_description}">' if meta_description else ''}
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: {font_family};
            line-height: 1.6;
            color: {text_color};
            background-color: {bg_color};
            font-size: 16px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }}
        
        /* Header */
        .site-header {{
            background: {bg_color};
            border-bottom: 1px solid #e2e8f0;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }}
        
        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }}
        
        .logo {{
            font-size: 1.75rem;
            font-weight: 800;
            color: {text_color};
            text-decoration: none;
        }}
        
        /* Navigation */
        .main-nav {{
            background: {bg_color};
        }}
        
        .nav-container {{
            display: flex;
            gap: 2rem;
            padding: 1rem 0;
            justify-content: center;
            flex-wrap: wrap;
            max-width: 1200px;
            margin: 0 auto;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }}
        
        .nav-link {{
            color: {text_color};
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .nav-link:hover,
        .nav-link.current {{
            color: {button_bg};
            background-color: rgba(0, 102, 204, 0.1);
        }}
        
        /* Hero Section */
        .hero-section {{
            text-align: center;
            padding: 4rem 0;
            background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 102, 204, 0.1) 100%);
        }}
        
        .hero-title {{
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1.5rem;
            color: {text_color};
            line-height: 1.2;
        }}
        
        .hero-description {{
            font-size: 1.25rem;
            color: {text_color};
            opacity: 0.8;
            max-width: 600px;
            margin: 0 auto 2rem;
        }}
        
        /* Main Content */
        .main-content {{
            padding: 3rem 0;
        }}
        
        .content-section {{
            margin: 2.5rem 0;
            padding: 2rem;
            background: {bg_color};
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            border: 1px solid #f0f0f0;
        }}
        
        .section-heading {{
            color: {text_color};
            margin-bottom: 1.5rem;
            font-weight: 700;
            line-height: 1.3;
        }}
        
        .section-heading:is(h1) {{ font-size: 2.5rem; }}
        .section-heading:is(h2) {{ font-size: 2rem; }}
        .section-heading:is(h3) {{ font-size: 1.5rem; }}
        .section-heading:is(h4) {{ font-size: 1.25rem; }}
        
        .section-content {{
            font-size: 1.1rem;
            line-height: 1.7;
            margin-bottom: 1rem;
            color: {text_color};
            opacity: 0.9;
        }}
        
        /* Buttons */
        .cta-section {{
            text-align: center;
            padding: 3rem 0;
        }}
        
        .button-group {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .btn {{
            display: inline-block;
            padding: {button_padding};
            background-color: {button_bg};
            color: {button_text};
            text-decoration: none;
            border-radius: {button_radius};
            font-weight: 600;
            font-size: 1rem;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }}
        
        .btn:hover {{
            background-color: {button_bg}dd;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
        }}
        
        .btn-primary {{
            background-color: {button_bg};
            color: {button_text};
        }}
        
        /* Footer */
        .site-footer {{
            background: {text_color};
            color: {bg_color};
            text-align: center;
            padding: 2rem 0;
            margin-top: 3rem;
        }}
        
        .footer-content {{
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        
        .footer-content a {{
            color: {bg_color};
            text-decoration: none;
        }}
        
        .footer-content a:hover {{
            text-decoration: underline;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .header-content {{
                flex-direction: column;
                gap: 1rem;
            }}
            
            .nav-container {{
                flex-direction: column;
                align-items: center;
                gap: 1rem;
            }}
            
            .hero-title {{
                font-size: 2.25rem;
            }}
            
            .content-section {{
                padding: 1.5rem;
                margin: 1.5rem 0;
            }}
            
            .button-group {{
                flex-direction: column;
                align-items: center;
                gap: 0.75rem;
            }}
        }}
        
        /* Animation */
        .content-section {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <div class="header-content">
                <a href="#" class="logo">{page_title}</a>
            </div>
        </div>
    </header>

    {nav_html}

    <section class="hero-section">
        <div class="container">
            <h1 class="hero-title">{main_heading}</h1>
            {f'<p class="hero-description">{meta_description}</p>' if meta_description else ''}
        </div>
    </section>

    <main class="main-content">
        <div class="container">
            {content_html}
            {buttons_html}
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <p>Recreated from <a href="{url}" target="_blank">{url}</a> | Layout-aware website cloning</p>
            </div>
        </div>
    </footer>
</body>
</html>'''
        
        return html_document

# Create global instance
website_cloner = LayoutAwareCloner()