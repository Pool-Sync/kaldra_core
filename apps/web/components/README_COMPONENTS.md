# 4IAM.AI Components

This directory contains global, reusable UI components for the 4IAM.AI platform.

## Components

### Layout Components

#### `header.tsx`
Global header with navigation and branding.
- **Status**: Placeholder
- **TODO**: Implement logo, navigation menu, user authentication menu

#### `footer.tsx`
Global footer with links and information.
- **Status**: Placeholder
- **TODO**: Implement footer sections, links, social media icons

#### `sidebar.tsx`
Collapsible sidebar navigation for dashboard views.
- **Status**: Placeholder
- **TODO**: Implement navigation tree, collapse functionality, active states

#### `nav.tsx`
Main navigation component used in header.
- **Status**: Basic structure
- **TODO**: Implement active states, dropdown menus, mobile responsive menu

#### `container.tsx`
Reusable container component for consistent page layouts.
- **Status**: Basic implementation with size variants
- **TODO**: Add more responsive sizing options, padding variants

## Usage

All components are designed to work with the KALDRA Design System and Visual Engine.

```tsx
import Header from '@/components/header';
import Footer from '@/components/footer';
import Container from '@/components/container';

export default function Page() {
  return (
    <>
      <Header />
      <Container size="lg">
        {/* Page content */}
      </Container>
      <Footer />
    </>
  );
}
```

## Integration with Design System

All components should:
- Use design tokens from `design_system/tokens/`
- Follow KALDRA branding guidelines
- Implement responsive design patterns
- Support dark mode (future)

## Next Steps

1. Integrate components with root layout
2. Implement navigation routing
3. Add authentication UI
4. Create mobile-responsive variants
5. Add accessibility features (ARIA labels, keyboard navigation)
