# AI Tool Pick Site Structure Guide

This document explains the structure of the AI Tool Pick static site for future Claude sessions to generate new articles in the correct format.

## Site Overview
- **Domain**: aitoolpick.co.uk
- **Purpose**: Blog reviewing AI tools for UK small businesses
- **Tech Stack**: Pure HTML/CSS (no frameworks)
- **Pages**: Homepage (index.html), Blog index (blog.html), Article pages

## File Structure
```
/
├── index.html          # Homepage
├── blog.html           # Blog index page
├── article-template.html # Sample article template
├── styles.css          # Main stylesheet
└── CLAUDE.md          # This guide
```

## Page Templates

### 1. Homepage (index.html)
- **Purpose**: Landing page with hero section, featured articles, affiliate links
- **Key Sections**:
  - Navigation header
  - Hero section with main CTA
  - Featured articles grid (3 articles)
  - Affiliate recommendations section
  - About section
  - Footer

### 2. Blog Index (blog.html)
- **Purpose**: List all blog articles
- **Structure**:
  - Same nav/footer as homepage
  - Blog header section
  - List of blog posts with meta info (date, category)

### 3. Article Pages
- **Naming Convention**: `tool-name-review.html` (e.g., `chatgpt-business-review.html`)
- **Structure**:
  - Article schema markup (JSON-LD)
  - SEO meta tags (title, description, Open Graph, Twitter)
  - Article header with meta info
  - Article body with H2/H3 headings
  - Affiliate boxes within content
  - Related articles section
  - Share buttons

## Content Guidelines

### Article Structure
1. **Introduction**: Hook + problem statement + overview
2. **Why It Matters**: Benefits for small businesses
3. **Tool Reviews**: 3-5 tools with pros/cons, pricing, use cases
4. **Affiliate Boxes**: Integrated throughout content
5. **Comparison/Decision Guide**: How to choose
6. **Conclusion**: Final recommendations

### Categories
- Writing & Content
- Customer Service
- Accounting
- Marketing
- Productivity
- Analytics

### SEO Requirements
- **Title Format**: "Tool Category for Small Business - AI Tool Pick"
- **Meta Description**: 150-160 characters
- **Keywords**: Include "UK small businesses", "AI tools", specific tool names
- **Schema Markup**: Article schema with proper dates, author, publisher

### Affiliate Integration
- **Placement**: Within tool reviews, as dedicated boxes
- **Format**: 
  ```html
  <div class="affiliate-box">
      <h4>Try Tool Name Today</h4>
      <p>Description</p>
      <a href="#" class="affiliate-link" target="_blank" rel="nofollow">Get Tool Name (Affiliate Link)</a>
  </div>
  ```
- **Attributes**: `target="_blank" rel="nofollow"`

## Styling Notes
- **Colors**: Blue (#3498db) for CTAs, Dark blue (#2c3e50) for headers
- **Typography**: Segoe UI, clean and readable
- **Layout**: Responsive grid system, card-based design
- **Spacing**: Generous padding, good contrast

## Generation Process for New Articles

1. **Choose Topic**: Select relevant AI tool category for UK small businesses
2. **Research**: Gather accurate info on 3-5 tools
3. **Create File**: Use `article-template.html` as base
4. **Update Content**:
   - Change title, meta tags, schema markup
   - Replace article content
   - Update affiliate links (placeholders)
   - Add to blog.html list
   - Update homepage featured articles if needed
5. **SEO Check**: Ensure proper meta tags and schema
6. **Test**: Open in browser to verify layout

## Maintenance Notes
- Keep footer copyright year current
- Update blog.html with new articles
- Maintain consistent styling across pages
- Ensure all links are relative or properly formatted
- Test responsiveness on mobile devices

## Future Enhancements
- Add images directory for article images
- Consider adding category pages
- Implement search functionality (if needed)
- Add newsletter signup
- Create author pages if multiple contributors