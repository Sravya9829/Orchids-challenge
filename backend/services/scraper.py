import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import requests
from typing import Dict, Optional, List
import base64
import re
import json

class LayoutAwareScraper:
    def __init__(self):
        self.browser = None
        self.page = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        self.page = await self.context.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def scrape_website(self, url: str) -> Dict:
        """Layout-aware scraping that understands website structure and flow"""
        
        print(f"🏗️ Starting layout-aware scrape for: {url}")
        
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            # Navigate to page
            await self.page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(4)  # Allow all content to load
            
            print("📸 Capturing visual reference...")
            screenshot = await self._capture_screenshot()
            
            print("🏗️ Analyzing layout structure...")
            layout_structure = await self._analyze_layout_structure()
            
            print("📐 Mapping content sections...")
            content_sections = await self._map_content_sections()
            
            print("🎨 Extracting visual design...")
            design_system = await self._extract_design_system()
            
            print("📝 Getting structured content...")
            structured_content = await self._extract_structured_content()
            
            print("🔗 Analyzing navigation...")
            navigation_analysis = await self._analyze_navigation_structure()
            
            return {
                "success": True,
                "url": url,
                "method": "layout_aware",
                "screenshot": screenshot,
                "layout_structure": layout_structure,
                "content_sections": content_sections,
                "design_system": design_system,
                "structured_content": structured_content,
                "navigation_analysis": navigation_analysis,
                "html": await self.page.content(),
                "css": {},
                "layout": layout_structure
            }
            
        except Exception as e:
            print(f"❌ Layout-aware scraping failed: {e}")
            return await self._fallback_scrape(url)

    async def _analyze_layout_structure(self) -> Dict:
        """Analyze the overall layout structure and flow"""
        
        layout_data = await self.page.evaluate("""
            () => {
                const layout = {
                    page_type: 'unknown',
                    main_sections: [],
                    layout_flow: 'vertical',
                    container_info: {},
                    viewport: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    }
                };
                
                // Detect main layout containers
                const body = document.body;
                const main = document.querySelector('main, .main, #main, [role="main"]') || body;
                const header = document.querySelector('header, .header, #header, [role="banner"]');
                const nav = document.querySelector('nav, .nav, .navigation, [role="navigation"]');
                const footer = document.querySelector('footer, .footer, #footer, [role="contentinfo"]');
                const sidebar = document.querySelector('aside, .sidebar, [role="complementary"]');
                
                // Determine page type based on structure
                if (header && nav && main && footer) {
                    layout.page_type = 'full_layout';
                } else if (main) {
                    layout.page_type = 'content_focused';
                } else {
                    layout.page_type = 'simple';
                }
                
                // Analyze main container
                const mainRect = main.getBoundingClientRect();
                const mainStyles = window.getComputedStyle(main);
                
                layout.container_info = {
                    width: mainRect.width,
                    maxWidth: mainStyles.maxWidth,
                    margin: mainStyles.margin,
                    padding: mainStyles.padding,
                    display: mainStyles.display,
                    flexDirection: mainStyles.flexDirection,
                    gridTemplateColumns: mainStyles.gridTemplateColumns
                };
                
                // Detect layout flow
                if (mainStyles.display === 'flex' && mainStyles.flexDirection === 'row') {
                    layout.layout_flow = 'horizontal';
                } else if (mainStyles.display === 'grid' && mainStyles.gridTemplateColumns !== 'none') {
                    layout.layout_flow = 'grid';
                } else {
                    layout.layout_flow = 'vertical';
                }
                
                // Identify main sections in order
                const sections = [];
                if (header) {
                    const headerRect = header.getBoundingClientRect();
                    sections.push({
                        type: 'header',
                        bounds: {
                            x: headerRect.x,
                            y: headerRect.y,
                            width: headerRect.width,
                            height: headerRect.height
                        },
                        styles: {
                            background: window.getComputedStyle(header).backgroundColor,
                            position: window.getComputedStyle(header).position
                        }
                    });
                }
                
                if (nav && nav !== header) {
                    const navRect = nav.getBoundingClientRect();
                    sections.push({
                        type: 'navigation',
                        bounds: {
                            x: navRect.x,
                            y: navRect.y,
                            width: navRect.width,
                            height: navRect.height
                        }
                    });
                }
                
                // Find main content sections
                const contentSections = main.querySelectorAll('section, article, .section, .content-section');
                contentSections.forEach((section, index) => {
                    const rect = section.getBoundingClientRect();
                    if (rect.height > 50) { // Only significant sections
                        sections.push({
                            type: 'content',
                            index: index,
                            bounds: {
                                x: rect.x,
                                y: rect.y,
                                width: rect.width,
                                height: rect.height
                            }
                        });
                    }
                });
                
                if (sidebar) {
                    const sidebarRect = sidebar.getBoundingClientRect();
                    sections.push({
                        type: 'sidebar',
                        bounds: {
                            x: sidebarRect.x,
                            y: sidebarRect.y,
                            width: sidebarRect.width,
                            height: sidebarRect.height
                        }
                    });
                }
                
                if (footer) {
                    const footerRect = footer.getBoundingClientRect();
                    sections.push({
                        type: 'footer',
                        bounds: {
                            x: footerRect.x,
                            y: footerRect.y,
                            width: footerRect.width,
                            height: footerRect.height
                        }
                    });
                }
                
                layout.main_sections = sections;
                return layout;
            }
        """)
        
        return layout_data

    async def _map_content_sections(self) -> Dict:
        """Map content sections in their proper hierarchical order"""
        
        sections_data = await self.page.evaluate("""
            () => {
                const sections = {
                    header_content: {},
                    navigation_content: {},
                    main_content: {},
                    sidebar_content: {},
                    footer_content: {}
                };
                
                // Header content
                const header = document.querySelector('header, .header, #header, [role="banner"]');
                if (header) {
                    const headerTitle = header.querySelector('h1, .logo, .brand');
                    const headerNav = header.querySelector('nav, .nav');
                    
                    sections.header_content = {
                        title: headerTitle ? headerTitle.textContent.trim() : '',
                        has_navigation: !!headerNav,
                        background_color: window.getComputedStyle(header).backgroundColor
                    };
                }
                
                // Navigation content
                const nav = document.querySelector('nav, .nav, .navigation, [role="navigation"]');
                if (nav) {
                    const navLinks = Array.from(nav.querySelectorAll('a')).map(link => ({
                        text: link.textContent.trim(),
                        href: link.href,
                        is_active: link.classList.contains('active') || link.getAttribute('aria-current') === 'page'
                    })).filter(link => link.text);
                    
                    sections.navigation_content = {
                        links: navLinks,
                        layout: window.getComputedStyle(nav).display,
                        position: window.getComputedStyle(nav).position
                    };
                }
                
                // Main content sections
                const main = document.querySelector('main, .main, #main, [role="main"]') || document.body;
                const mainSections = [];
                
                // Find content blocks in order
                const contentElements = main.querySelectorAll('h1, h2, h3, section, article, .section, .content-block, .hero');
                let currentSection = null;
                
                contentElements.forEach(element => {
                    const rect = element.getBoundingClientRect();
                    if (rect.height < 20) return; // Skip tiny elements
                    
                    if (element.matches('h1, h2, h3')) {
                        // Start new section with heading
                        if (currentSection) {
                            mainSections.push(currentSection);
                        }
                        currentSection = {
                            type: 'text_section',
                            heading: {
                                level: element.tagName.toLowerCase(),
                                text: element.textContent.trim(),
                                styles: {
                                    fontSize: window.getComputedStyle(element).fontSize,
                                    color: window.getComputedStyle(element).color,
                                    fontWeight: window.getComputedStyle(element).fontWeight
                                }
                            },
                            content: [],
                            bounds: {
                                y: rect.y,
                                height: rect.height
                            }
                        };
                    } else if (element.matches('section, article, .section')) {
                        // Standalone section
                        const sectionHeading = element.querySelector('h1, h2, h3, h4');
                        const sectionContent = Array.from(element.querySelectorAll('p, div')).map(p => p.textContent.trim()).filter(text => text && text.length > 20);
                        
                        mainSections.push({
                            type: 'content_section',
                            heading: sectionHeading ? {
                                level: sectionHeading.tagName.toLowerCase(),
                                text: sectionHeading.textContent.trim()
                            } : null,
                            content: sectionContent.slice(0, 3), // Limit content
                            bounds: {
                                y: rect.y,
                                height: rect.height
                            }
                        });
                    }
                });
                
                // Add last section if exists
                if (currentSection) {
                    mainSections.push(currentSection);
                }
                
                // Sort sections by vertical position
                mainSections.sort((a, b) => a.bounds.y - b.bounds.y);
                
                sections.main_content = {
                    sections: mainSections,
                    total_sections: mainSections.length
                };
                
                return sections;
            }
        """)
        
        return sections_data

    async def _extract_design_system(self) -> Dict:
        """Extract the website's design system and visual patterns"""
        
        design_data = await self.page.evaluate("""
            () => {
                const design = {
                    colors: {},
                    typography: {},
                    spacing: {},
                    components: {}
                };
                
                // Extract color palette
                const body = document.body;
                const bodyStyles = window.getComputedStyle(body);
                
                design.colors.primary = {
                    background: bodyStyles.backgroundColor,
                    text: bodyStyles.color,
                    font_family: bodyStyles.fontFamily
                };
                
                // Extract heading styles
                const headingStyles = {};
                ['h1', 'h2', 'h3', 'h4'].forEach(tag => {
                    const element = document.querySelector(tag);
                    if (element) {
                        const styles = window.getComputedStyle(element);
                        headingStyles[tag] = {
                            fontSize: styles.fontSize,
                            fontWeight: styles.fontWeight,
                            color: styles.color,
                            marginTop: styles.marginTop,
                            marginBottom: styles.marginBottom,
                            lineHeight: styles.lineHeight
                        };
                    }
                });
                design.typography.headings = headingStyles;
                
                // Extract button styles
                const buttons = document.querySelectorAll('button, .btn, .button, input[type="button"], a[class*="btn"]');
                if (buttons.length > 0) {
                    const buttonStyles = window.getComputedStyle(buttons[0]);
                    design.components.button = {
                        backgroundColor: buttonStyles.backgroundColor,
                        color: buttonStyles.color,
                        border: buttonStyles.border,
                        borderRadius: buttonStyles.borderRadius,
                        padding: buttonStyles.padding,
                        fontSize: buttonStyles.fontSize,
                        fontWeight: buttonStyles.fontWeight
                    };
                }
                
                // Extract link styles
                const links = document.querySelectorAll('a:not([class*="btn"])');
                if (links.length > 0) {
                    const linkStyles = window.getComputedStyle(links[0]);
                    design.components.link = {
                        color: linkStyles.color,
                        textDecoration: linkStyles.textDecoration,
                        fontWeight: linkStyles.fontWeight
                    };
                }
                
                // Extract spacing patterns
                const spacingElements = document.querySelectorAll('section, article, .section, h1, h2, h3, p');
                const margins = [];
                const paddings = [];
                
                spacingElements.forEach(element => {
                    const styles = window.getComputedStyle(element);
                    const marginTop = parseInt(styles.marginTop) || 0;
                    const marginBottom = parseInt(styles.marginBottom) || 0;
                    const paddingTop = parseInt(styles.paddingTop) || 0;
                    const paddingBottom = parseInt(styles.paddingBottom) || 0;
                    
                    if (marginTop > 0) margins.push(marginTop);
                    if (marginBottom > 0) margins.push(marginBottom);
                    if (paddingTop > 0) paddings.push(paddingTop);
                    if (paddingBottom > 0) paddings.push(paddingBottom);
                });
                
                // Find most common spacing values
                const marginCounts = {};
                const paddingCounts = {};
                
                margins.forEach(margin => {
                    marginCounts[margin] = (marginCounts[margin] || 0) + 1;
                });
                
                paddings.forEach(padding => {
                    paddingCounts[padding] = (paddingCounts[padding] || 0) + 1;
                });
                
                design.spacing = {
                    common_margins: Object.keys(marginCounts).sort((a, b) => marginCounts[b] - marginCounts[a]).slice(0, 3),
                    common_paddings: Object.keys(paddingCounts).sort((a, b) => paddingCounts[b] - paddingCounts[a]).slice(0, 3)
                };
                
                return design;
            }
        """)
        
        return design_data

    async def _extract_structured_content(self) -> Dict:
        """Extract content in its structured form"""
        
        content_data = await self.page.evaluate("""
            () => {
                const content = {
                    page_title: document.title,
                    meta_description: '',
                    main_heading: '',
                    headings_hierarchy: [],
                    text_content: [],
                    buttons: [],
                    images: [],
                    lists: []
                };
                
                // Meta description
                const metaDesc = document.querySelector('meta[name="description"]');
                if (metaDesc) {
                    content.meta_description = metaDesc.getAttribute('content');
                }
                
                // Main heading
                const h1 = document.querySelector('h1');
                if (h1) {
                    content.main_heading = h1.textContent.trim();
                }
                
                // Headings hierarchy
                const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
                headings.forEach((heading, index) => {
                    const text = heading.textContent.trim();
                    if (text) {
                        content.headings_hierarchy.push({
                            level: parseInt(heading.tagName.substring(1)),
                            text: text,
                            order: index
                        });
                    }
                });
                
                // Text content in order
                const textElements = document.querySelectorAll('p, div[class*="text"], div[class*="content"]');
                textElements.forEach(element => {
                    const text = element.textContent.trim();
                    if (text && text.length > 30 && text.length < 500) {
                        // Check if it's not just container with other elements
                        const hasBlockChildren = element.querySelector('div, p, h1, h2, h3, h4, h5, h6');
                        if (!hasBlockChildren) {
                            content.text_content.push(text);
                        }
                    }
                });
                
                // Buttons with context
                const buttons = document.querySelectorAll('button, .btn, .button, input[type="button"], input[type="submit"], a[class*="btn"]');
                buttons.forEach(button => {
                    const text = button.textContent.trim() || button.value || button.getAttribute('aria-label');
                    if (text) {
                        content.buttons.push({
                            text: text,
                            type: button.tagName.toLowerCase(),
                            href: button.href || '',
                            classes: button.className || ''
                        });
                    }
                });
                
                // Images with context
                const images = document.querySelectorAll('img');
                images.forEach(img => {
                    if (img.src && img.alt) {
                        content.images.push({
                            alt: img.alt,
                            src: img.src,
                            width: img.naturalWidth || img.width,
                            height: img.naturalHeight || img.height
                        });
                    }
                });
                
                // Lists
                const lists = document.querySelectorAll('ul, ol');
                lists.forEach(list => {
                    const items = Array.from(list.querySelectorAll('li')).map(li => li.textContent.trim()).filter(text => text);
                    if (items.length > 0) {
                        content.lists.push({
                            type: list.tagName.toLowerCase(),
                            items: items
                        });
                    }
                });
                
                return content;
            }
        """)
        
        return content_data

    async def _analyze_navigation_structure(self) -> Dict:
        """Analyze navigation structure and patterns"""
        
        nav_data = await self.page.evaluate("""
            () => {
                const navigation = {
                    primary_nav: [],
                    secondary_nav: [],
                    breadcrumbs: [],
                    footer_nav: [],
                    nav_style: 'horizontal'
                };
                
                // Primary navigation
                const primaryNav = document.querySelector('nav, .nav, .navigation, header nav');
                if (primaryNav) {
                    const navLinks = Array.from(primaryNav.querySelectorAll('a')).map(link => ({
                        text: link.textContent.trim(),
                        href: link.href,
                        is_current: link.getAttribute('aria-current') === 'page' || link.classList.contains('active')
                    })).filter(link => link.text && link.text.length < 50);
                    
                    navigation.primary_nav = navLinks;
                    
                    // Determine nav style
                    const navStyles = window.getComputedStyle(primaryNav);
                    if (navStyles.flexDirection === 'column' || navStyles.display === 'block') {
                        navigation.nav_style = 'vertical';
                    } else {
                        navigation.nav_style = 'horizontal';
                    }
                }
                
                // Breadcrumbs
                const breadcrumbs = document.querySelector('.breadcrumbs, .breadcrumb, nav[aria-label*="breadcrumb"]');
                if (breadcrumbs) {
                    const crumbs = Array.from(breadcrumbs.querySelectorAll('a, span')).map(crumb => crumb.textContent.trim());
                    navigation.breadcrumbs = crumbs;
                }
                
                // Footer navigation
                const footer = document.querySelector('footer');
                if (footer) {
                    const footerLinks = Array.from(footer.querySelectorAll('a')).map(link => ({
                        text: link.textContent.trim(),
                        href: link.href
                    })).filter(link => link.text && link.text.length < 50);
                    
                    navigation.footer_nav = footerLinks.slice(0, 10); // Limit footer links
                }
                
                return navigation;
            }
        """)
        
        return nav_data

    async def _capture_screenshot(self) -> str:
        """Capture high-quality screenshot"""
        try:
            screenshot_bytes = await self.page.screenshot(
                full_page=True,
                type="png",
                quality=90
            )
            return base64.b64encode(screenshot_bytes).decode()
        except Exception as e:
            print(f"⚠️ Screenshot failed: {e}")
            return ""

    async def _fallback_scrape(self, url: str) -> Dict:
        """Fallback scraping method"""
        try:
            print(f"📄 Fallback scraping for: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return {
                "success": True,
                "url": url,
                "method": "fallback",
                "screenshot": "",
                "layout_structure": {"page_type": "simple", "main_sections": []},
                "content_sections": {},
                "design_system": {},
                "structured_content": {"page_title": "Website", "headings_hierarchy": []},
                "navigation_analysis": {"primary_nav": []},
                "html": response.text,
                "css": {},
                "layout": {}
            }
            
        except Exception as e:
            print(f"❌ Fallback scraping failed: {e}")
            return {"success": False, "error": str(e), "url": url}

# Utility function
async def scrape_website_data(url: str) -> Dict:
    """Layout-aware website scraping utility"""
    try:
        async with LayoutAwareScraper() as scraper:
            result = await scraper.scrape_website(url)
            return result
    except Exception as e:
        print(f"❌ Scraper utility error: {e}")
        return {
            "success": False,
            "error": f"Scraper initialization failed: {str(e)}",
            "url": url
        }