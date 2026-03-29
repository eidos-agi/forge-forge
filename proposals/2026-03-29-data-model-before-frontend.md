# Proposal: improve-forge should deprioritize UI when data model is unstable

## Learning
Building 30 UI features on top of an unvalidated data model wastes effort. The data model is the product. The UI is a view into it. Improving the UI when the underlying model hasn't been tested with real data is polishing a house with no foundation.

## Source
eidos-assistant build session (2026-03-29). Built calendar view, export views, search, drag-and-drop, 5 humanistic export formats — before validating that the core loop (record → transcribe → store) worked with real input. All the UI features worked fine. The core loop failed.

## Proposed Change
- **Target forge:** improve-forge
- **Target file:** `.claude/skills/improve.md` Step 4 (Prioritize)
- **Change:** Add prioritization rule: "If the project has a data model (database, file structure, API schema) that hasn't been validated with real input, that's higher priority than any UI improvement. Test the model before polishing the view."

## Why This Matters
This is a common pattern in AI-assisted development: the agent builds many features quickly, creating a false sense of completeness. The improve-forge should catch this pattern and redirect effort to the foundation.

## Evidence
eidos-assistant: 30+ UI features, 10 passing CI tests, 0 real-input validations. The bucket-per-recording data model was sound but untested. Calendar view was pixel-perfect but useless without working transcription.
