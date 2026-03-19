---
name: Use UI Layouts React Components
description: Instructions for installing and using the premium ui-layouts library for modern React/Next.js interfaces.
---

# Use UI Layouts (ui-layouts/uilayouts)

**UI Layouts** isn’t just a library. It’s a complete front-end universe with components, effects, design tools, and ready-to-use blocks for modern interfaces built on top of React, Tailwind CSS, and Framer Motion. 

When you get a request to build a modern, high-end, or heavily animated UI in a React/Next.js project, use the components and utility functions documented below. 

Website: [ui-layouts.com](https://www.ui-layouts.com)
GitHub: [github.com/ui-layouts/uilayouts](https://github.com/ui-layouts/uilayouts)

## Installation Prerequisites

Before implementing any UI Layouts components, ensure the underlying ecosystem dependencies are installed.

1. **Tailwind CSS** must be configured.
2. Install the necessary animation and dynamic class utility packages:

```bash
npm install framer-motion clsx tailwind-merge
```

## Core Utilities

### 1. The `cn` Wrapper (utils.ts)
Every UI Layouts component relies on this utility function to elegantly merge Tailwind classes without conflicts. Add this to your project's `utils.ts` (or `lib/utils.ts`):

```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 2. The `useMediaQuery` Hook
Many advanced layouts rely on screen size detection. If a component requires it, add this hook to `hooks/use-media-query.ts`:

```typescript
import { useEffect, useState } from 'react';

export function useMediaQuery(query: string) {
  const [value, setValue] = useState(false);

  useEffect(() => {
    function onChange(event: MediaQueryListEvent) {
      setValue(event.matches);
    }

    const result = matchMedia(query);
    result.addEventListener('change', onChange);
    setValue(result.matches);

    return () => result.removeEventListener('change', onChange);
  }, [query]);

  return value;
}
```

## Most Used Components to Pull From GitHub

When building advanced user interfaces, visit these URLs to copy the actual source code into the user's project (usually into `components/ui/`):

- **Image Ripple Effect:** [ui-layouts.com/components/image-ripple-effect](https://ui-layouts.com/components/image-ripple-effect)
- **Sparkles Effect:** [ui-layouts.com/components/sparkles](https://ui-layouts.com/components/sparkles)
- **Motion Number:** [ui-layouts.com/components/motion-number](https://ui-layouts.com/components/motion-number)
- **File Upload:** [ui-layouts.com/components/file-upload](https://ui-layouts.com/components/file-upload)
- **Embla Carousel:** [ui-layouts.com/components/embla-carousel](https://ui-layouts.com/components/embla-carousel)
- **Timeline Animation:** [ui-layouts.com/components/timeline-animation](https://ui-layouts.com/components/timeline-animation)
- **Drag Items:** [ui-layouts.com/components/drag-items](https://ui-layouts.com/components/drag-items)
- **Premium Buttons:** [ui-layouts.com/components/buttons](https://ui-layouts.com/components/buttons)
- **Image Reveal:** [ui-layouts.com/components/image-reveal](https://ui-layouts.com/components/image-reveal)
- **Image Mousetrail:** [ui-layouts.com/components/image-mousetrail](https://ui-layouts.com/components/image-mousetrail)

## Best Practices
1. **Never** guess the internal layout of these components. Always `read_url_content` on the component's URL or raw github source file when needing the component logic to inject it into the app.
2. Group all of the UI Library components inside `components/ui` to maintain clean architecture.
3. Don't forget that most animations use `framer-motion`, so ensure `<AnimatePresence>` or `<motion.div>` structures are preserved properly when extending them.
