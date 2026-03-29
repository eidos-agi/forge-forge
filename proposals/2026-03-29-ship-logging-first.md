# Proposal: New guardrail — ship logging before features

## Learning
An app with built-in chain logging and no calendar view finds bugs in hour one. An app with 30 features and no logging wastes five hours on "it doesn't work."

## Source
eidos-assistant build session (2026-03-29). Built 30 features (calendar view, export, search, drag-and-drop, etc.) before adding any instrumentation. When the app failed on real use, had zero visibility into why. Adding ChainLogger found the bug immediately.

## Proposed Change
- **Target:** forge-forge guardrail or ship-forge guardrail
- **Change:** Add ecosystem guardrail: "Every app must have built-in logging/instrumentation before shipping features. A Debug view or chain log is a prerequisite, not an afterthought."

## Why This Matters
This applies to every software project in the ecosystem. The pattern repeats: build features → ship → it breaks → no idea why → add logging → find obvious bug. Inverting the order (logging first, features second) prevents this entirely.

## Evidence
eidos-assistant: 30 features built, 10 CI tests passing, zero instrumentation. First real test failed. Added ChainLogger (1 file, ~100 lines). Found the bug in one log line.
