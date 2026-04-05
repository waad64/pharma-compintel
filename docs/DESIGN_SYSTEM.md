# PCI Dashboard - Design System & Style Guide

## Color Palette

### Primary Colors
- **Primary Blue**: `#667eea` - Main brand color, CTAs, active states
- **Secondary Purple**: `#764ba2` - Accents, gradients, hover states
- **Dark Text**: `#1a365d` - Primary text, headers
- **Light Text**: `#718096` - Secondary text, labels, hints

### Status Colors
- **Success**: `#48bb78` - Completed, active, positive
- **Warning**: `#ed8936` - In progress, caution
- **Error**: `#f56565` - Failed, terminated, negative
- **Info**: `#4299e1` - Information, neutral

### Neutral Colors
- **Background Light**: `#f5f7fa` - Page background
- **Background White**: `#ffffff` - Card backgrounds
- **Border**: `#e2e8f0` - Dividers, borders
- **Disabled**: `#cbd5e0` - Disabled states

## Typography

### Font Family
```
-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif
```

### Font Sizes
- **Display**: 2.8rem (44px) - Page titles
- **Heading 1**: 2.2rem (35px) - Section headers
- **Heading 2**: 1.4rem (22px) - Subsection headers
- **Body Large**: 1.1rem (18px) - Large text
- **Body**: 1rem (16px) - Default text
- **Body Small**: 0.95rem (15px) - Secondary text
- **Caption**: 0.85rem (13px) - Labels, hints
- **Code**: 0.875rem (14px) - Monospace

### Font Weights
- **Light**: 300 - Disabled, hints
- **Regular**: 400 - Body text
- **Medium**: 500 - Secondary headers
- **Semibold**: 600 - Labels, buttons
- **Bold**: 700 - Headers, emphasis
- **Black**: 900 - Display text

### Line Heights
- **Tight**: 1.2 - Headers
- **Normal**: 1.5 - Body text
- **Relaxed**: 1.75 - Long-form content

## Spacing System

### Base Unit: 0.5rem (8px)

```
xs: 0.25rem (4px)
sm: 0.5rem (8px)
md: 1rem (16px)
lg: 1.5rem (24px)
xl: 2rem (32px)
2xl: 3rem (48px)
3xl: 4rem (64px)
```

### Padding
- **Compact**: 0.75rem (12px) - Buttons, small components
- **Standard**: 1.5rem (24px) - Cards, sections
- **Spacious**: 2rem (32px) - Page sections

### Margins
- **Between sections**: 2rem (32px)
- **Between elements**: 1rem (16px)
- **Between items**: 0.5rem (8px)

## Shadows

### Shadow System
```
sm: 0 2px 8px rgba(0,0,0,0.08)
md: 0 4px 16px rgba(0,0,0,0.12)
lg: 0 8px 24px rgba(0,0,0,0.15)
```

### Usage
- **sm**: Cards, small components
- **md**: Hover states, elevated components
- **lg**: Modals, dropdowns, overlays

## Border Radius

```
sm: 8px - Small components, buttons
md: 10px - Cards, inputs
lg: 12px - Large sections, containers
```

## Transitions & Animations

### Timing
- **Duration**: 300ms (standard)
- **Easing**: cubic-bezier(0.4, 0, 0.2, 1)

### Common Transitions
```css
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

### Animation Examples
- **Hover**: translateY(-2px) + shadow increase
- **Active**: scale(0.98)
- **Fade**: opacity 0 → 1
- **Slide**: translateX/Y with easing

## Component Styles

### Buttons
- **Primary**: Blue background, white text
- **Secondary**: White background, blue text, border
- **Danger**: Red background, white text
- **Disabled**: Gray background, gray text

### Cards
- **Background**: White
- **Border Radius**: 10px
- **Shadow**: sm (0 2px 8px)
- **Padding**: 1.5rem
- **Border Left**: 4px solid primary color

### Inputs
- **Border**: 1px solid #e2e8f0
- **Border Radius**: 8px
- **Padding**: 0.75rem 1rem
- **Focus**: Blue border, shadow

### Tables
- **Header Background**: #f5f7fa
- **Row Hover**: #f9fafb
- **Border**: 1px solid #e2e8f0
- **Padding**: 1rem

### Badges
- **Padding**: 0.25rem 0.75rem
- **Border Radius**: 12px
- **Font Size**: 0.85rem
- **Font Weight**: 600

## Responsive Design

### Breakpoints
```
Mobile: < 640px
Tablet: 640px - 1024px
Desktop: > 1024px
```

### Responsive Adjustments
- **Mobile**: Single column, larger touch targets
- **Tablet**: Two columns, optimized spacing
- **Desktop**: Multi-column, full layout

## Accessibility

### Color Contrast
- **Normal Text**: 4.5:1 minimum
- **Large Text**: 3:1 minimum
- **UI Components**: 3:1 minimum

### Focus States
- **Visible Focus**: 2px outline, 2px offset
- **Focus Color**: Primary blue (#667eea)

### Keyboard Navigation
- **Tab Order**: Logical, left-to-right, top-to-bottom
- **Skip Links**: Available for main content
- **Keyboard Shortcuts**: Documented

### Screen Readers
- **Semantic HTML**: Proper heading hierarchy
- **ARIA Labels**: For icon buttons
- **Alt Text**: For all images

## Icons & Emojis

### Icon Usage
- **Size**: 16px (small), 24px (medium), 32px (large)
- **Color**: Inherit from text color
- **Spacing**: 0.5rem from text

### Emoji Usage
- **Consistent**: Use same emoji set
- **Meaningful**: Only for clarity
- **Accessible**: Include text alternative

## Data Visualization

### Chart Colors
- **Primary Series**: #667eea
- **Secondary Series**: #764ba2
- **Tertiary Series**: #48bb78
- **Neutral**: #cbd5e0

### Chart Styling
- **Background**: White or transparent
- **Grid**: Light gray (#e2e8f0)
- **Axis**: Dark text (#1a365d)
- **Legend**: Positioned right or bottom

### Chart Interactions
- **Hover**: Tooltip with data
- **Click**: Drill-down or filter
- **Zoom**: Pan and zoom enabled

## Forms

### Form Layout
- **Label**: Above input, bold, required indicator
- **Input**: Full width, 40px height
- **Help Text**: Below input, gray, small
- **Error**: Red text, red border

### Validation
- **Real-time**: As user types
- **On Blur**: When leaving field
- **On Submit**: Before submission
- **Error Messages**: Clear, actionable

## Modals & Dialogs

### Modal Styling
- **Overlay**: Semi-transparent black (rgba(0,0,0,0.5))
- **Modal**: White background, rounded corners
- **Shadow**: lg (0 8px 24px)
- **Padding**: 2rem

### Modal Behavior
- **Backdrop Click**: Close modal
- **Escape Key**: Close modal
- **Focus Trap**: Keep focus inside modal
- **Animation**: Fade in/out

## Loading States

### Loading Indicators
- **Spinner**: Animated circle, primary color
- **Skeleton**: Gray placeholder, pulse animation
- **Progress**: Linear progress bar

### Loading Messages
- **Short**: "Loading..."
- **Long**: "This may take a moment..."
- **Estimated**: "About 30 seconds remaining"

## Error States

### Error Display
- **Toast**: Top-right, auto-dismiss after 5s
- **Inline**: Below field, red text
- **Modal**: For critical errors
- **Page**: Full-page error with recovery options

### Error Messages
- **Clear**: Explain what went wrong
- **Actionable**: Suggest how to fix
- **Friendly**: Avoid technical jargon
- **Consistent**: Use same tone

## Success States

### Success Display
- **Toast**: Top-right, green background
- **Checkmark**: Green icon
- **Message**: Confirmation text
- **Auto-dismiss**: After 3-5 seconds

## Best Practices

### Do's ✓
- Use consistent spacing and sizing
- Maintain color contrast ratios
- Provide clear feedback for actions
- Use semantic HTML
- Test on multiple devices
- Document design decisions
- Keep animations subtle
- Prioritize accessibility

### Don'ts ✗
- Don't use more than 3 colors per section
- Don't use animations for critical content
- Don't rely on color alone for meaning
- Don't use auto-playing media
- Don't create keyboard traps
- Don't use placeholder text as labels
- Don't disable zoom on mobile
- Don't use outdated patterns

## Implementation Examples

### Card Component
```html
<div class="metric-card">
  <div class="metric-label">Total Companies</div>
  <div class="metric-value">24</div>
</div>
```

### Button Component
```html
<button class="btn btn-primary">
  Download Report
</button>
```

### Alert Component
```html
<div class="info-box">
  <strong>Note:</strong> Data updated daily
</div>
```

---

**Version**: 2.0
**Last Updated**: 2024
**Status**: Production Ready ✓
