# Structural Poster

Use this style for information-first visuals that must explain a system, process, or architecture clearly.

## Core Intent

Make the viewer understand the system at a glance:
- what the major stages are
- how they connect
- where decisions happen
- where loops, audits, approvals, or branches occur

This is not a raw flowchart. It should feel like a premium product or research poster with disciplined visual hierarchy.

## Hallmarks

- landscape infographic composition, usually `16:9`
- title area at top-left
- 2-7 horizontal bands or grouped containers
- rounded module cards
- thick directional arrows
- decision diamonds, gates, legends, badges
- soft editorial shadows
- white or light background
- blue, green, teal, amber accents
- clean sans-serif typography
- occasional original mascots or tiny helper characters only when they improve approachability

## Use For

- product architecture posters
- research workflow overviews
- system lifecycle summaries
- audited pipelines
- multi-stage methodology diagrams
- "one slide explains everything" visuals

## Composition Recipe

Build prompts around these layers:

1. Title and subtitle
2. Major process bands
3. Module cards inside each band
4. Arrows, loops, branches, approval points
5. Legend or principle strip
6. Optional example outputs or small snapshots

## Prompt Vocabulary

Useful phrases:
- premium infographic poster
- product architecture overview
- audited process map
- structured systems diagram
- editorial whitepaper visual
- rounded cards, thick arrows, decision diamonds
- high information density but clean
- auditable, trustworthy, rigorous

## Text Handling

- Use short labels.
- Prefer nouns and verb phrases, not sentences.
- Avoid more than 2 short lines per module unless the user explicitly wants dense text.
- Ask the model for legible, minimal typesetting rather than paragraph blocks.

## Negative Tendencies

Avoid:
- chaotic UML energy
- tiny unreadable labels
- generic corporate PowerPoint look
- flat vector boredom
- overdecorated cartoon scene
- dark cyberpunk treatment

## Prompt Skeleton

Use or adapt this structure:

```text
Create a premium landscape infographic poster for <system/project name>.
The image should explain the full workflow clearly in a structured, product-grade visual style.

Main title:
"<title>"
Subtitle:
"<subtitle>"

Overall composition:
16:9 landscape, top title area, multiple horizontal process bands, rounded containers, module cards, thick arrows, decision diamonds, clear loops, small icons, optional original helper mascots, bottom legend.

Visual language:
white or light editorial background, navy typography, blue-green governance accents, soft shadows, crisp spacing, premium keynote poster quality.

Process content:
<band 0 ...>
<band 1 ...>
<band 2 ...>

Design goals:
high readability, clear sequencing, trustworthy audited-system feeling, not a generic flowchart, not a dashboard screenshot.
```
