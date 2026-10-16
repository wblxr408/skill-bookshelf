# Frontend behavior and design ownership

Use the existing local design owner (impeccable or frontend-design) for art direction. ECC complements engineering through react-patterns, react-performance, vue-patterns, angular-developer, nuxt4-patterns, frontend-patterns, design-system, frontend-a11y and accessibility. Match the existing framework and preserve deliberate project style through inherit-legacy-style.

Before implementation, test the user journey and state contract: initial/loading/empty/success/error, stale responses, double actions, cancellation and persistence. Use semantic accessible controls, visible focus, keyboard order, labels/errors, reduced motion and responsive layouts. Test affected interactions and state results, not screenshot similarity, selectors existing or an idle page opening.

Measure actual performance bottlenecks and Web Vitals with a representative workload. Use traces/profiles to choose a change; regression covers visible behavior and accessibility. For mobile/native work select Android/Kotlin/Compose, Flutter/Dart, Swift/SwiftUI or React Native guidance from the catalog rather than forcing web assumptions.

UI animation remains a UI task. HyperFrames owns video deliverables under the installed global route; existing Remotion source stays with Remotion. Presentation/document owners keep PPTX/Google Slides/PDF requirements; frontend-slides supplements explicitly requested HTML decks.
