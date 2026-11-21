# Figure strategy and visual audit

Readers and reviewers routinely inspect the title, abstract, and figures before reading a paragraph
of Results. Figures are the visual spine of the argument, not decorations glued onto finished prose.

## 1. Visual-Empirical Boundary Rule (core)

Compelling graphics can accidentally deceive reviewers. Enforce a hard line between measured data
and conceptual framing:

- Tag every panel or visual element in `figure-plan.md` as `[measured data]` or
  `[conceptual schematic]`.
- Quantitative plots must reproduce exact supplied values (axes, intervals, sample sizes). Never
  sketch smooth "illustrative" curves that look like real experimental outputs.
- Never show a clinical outcome icon, patient-benefit arrow, or causal pathway arrow implying
  validated clinical efficacy when the evidence is observational, retrospective, or purely
  computational/in silico.
- Keep conceptual schematics visibly schematic (clear labels such as "Hypothesized pathway" or
  "Study architecture") and place measured metrics only where tied to an actual data source.

## 2. Making the figure sequence carry the paper (core)

Design the main figures (typically 3–6 depending on venue display caps) as a **standalone
narrative**:

1. **One question per figure.** If a figure requires eight panels answering three unrelated
   questions, split it or move secondary panels to Supplementary Figures.
2. **The standalone caption test.** Read only the figure titles, panel layouts, and captions in
   sequence (`Fig. 1 → Fig. 2 → … → Fig. K`). A field reader should grasp the study design, main
   finding, key robustness check, and boundary condition without opening the Results prose.
3. **First sentence = finding, not topic.**
   - Weak: *"Figure 2. Subgroup analysis of 12-month PROMIS scores."*
   - Strong: *"Figure 2. Early rehabilitation (<6 weeks) is associated with larger 12-month physical
     function gains predominantly among patients with baseline neuropathic pain."*
4. **Main text vs. Supplement allocation:**
   - **Main text:** cohort/workflow clarity (when non-obvious), primary endpoint/result, decisive
     control/ablation/sensitivity test, and key mechanism or subgroup boundary.
   - **Supplement:** routine QC, full covariate balance tables, hyper-parameter grids, redundant
     stratifications, and secondary endpoints that confirm the main picture without changing it.
5. **Consistent visual grammar:** Keep identical color assignments across every figure (e.g., if
   Early Rehab is Okabe–Ito blue `#0072B2` in Fig. 1, keep it `#0072B2` in Figs. 2–4).

## 3. Central synthesis figure (default when warranted; opt-in for clinical reports)

Propose a **central synthesis figure** (Figure 1, concluding summary figure, or graphical abstract)
when the paper has a multi-part mechanism, method workflow, or synthesis message that benefits from
one anchor visual.

- **Opt-in for clinical cohort/trial reports:** Many clinical journals impose a strict 4–5 display
  item cap where a STROBE/CONSORT flow diagram, primary outcome plot, and subgroup forest plot
  already tell the complete story. Do not force a synthesis graphic when primary data figures carry
  the paper — note `Central synthesis figure: omitted — <reason>` in `figure-plan.md` and proceed.
- **When a synthesis graphic *is* warranted, offer three genuinely different visual architectures**
  (never three palettes of the same box-and-arrow flowchart):
  1. **Integrated scientific illustration:** connects clinical/biological/physical context,
     mechanism or workflow, and primary quantitative takeaway in one visual landscape.
  2. **Comparative / explanatory architecture:** contrasts comparator vs. proposed regime or failure
     mode vs. fix without strawmen.
  3. **Data-led / novel relationship visual:** anchors the graphic in an actual measured tradeoff
     surface, dose–response spline, trajectory, or frontier plot.
- For each concept, specify 5 crisp items: **Core takeaway**, **Panel layout & focal anchor**,
  **`[measured data]` vs. `[conceptual schematic]` boundary**, **Key annotations + draft
  finding-first caption**, and **Effort & tradeoff**. Recommend one concept and confirm with the
  author before locking downstream prose.

## 4. Universal visual quality rules

Apply to every proposed brief and every audited draft figure:

- **Typography:** Design at final print width (single-column ~85 mm or double-column ~175 mm) so
  every axis label and annotation stays ≥ 7–8 pt after scaling.
- **Color & accessibility:** Use colorblind-safe palettes (Okabe–Ito: e.g., blue `#0072B2`,
  vermilion `#D55E00`, bluish green `#009E73`, orange `#E69F00`, paired with neutral non-Okabe–Ito
  gray `#7F8C8D` for muted comparators; or Viridis/Cividis for continuous scales). Never encode
  groups by red vs. green alone. Pair color with **dual encoding** (line dash, marker shape, direct
  label) so figures survive grayscale printing. Cap categorical colors at ≤ 5–6.
- **Honest axes & uncertainty:** Label every axis with quantity and units. Show uncertainty
  (95% CI, IQR, SD, or individual points where `n` allows) and state `n` per group. Mark broken or
  log axes explicitly. Do not distort bar-chart baselines away from zero.
- **No chartjunk:** No decorative 3D, drop shadows, heavy gridlines, or redundant in-plot titles
  that duplicate the caption.
- **Format:** Vector export (PDF/SVG/EPS) for plots and diagrams; high-DPI (≥ 300–600 dpi) only
  for micrographs, medical imaging, or raster photography.

## 5. Multimodal visual audit protocol (when draft images exist)

When the user supplies rendered figure files (`.png`, `.jpg`, `.pdf`), inspect them directly using
image reading before giving feedback:

1. **First-glance test (5 seconds):** What jumps out first? Does the visual focal point match the
   caption's claimed finding?
2. **Legibility check:** Are axis ticks, legends, p-values, and panel letters (`a`, `b`, `c`)
   crisp and readable at column width? Any overlapping labels?
3. **Encoding & honesty check:** Colorblind/grayscale discriminability, axis range honesty, error
   bars present, sample sizes visible, `[measured data]` clearly distinct from schematic elements.
4. **Text-figure redundancy check:** Does Results prose recite every bar height, or does it
   interpret patterns while letting the figure carry the detail?

In **text-only mode** (no image file provided), audit structure, data mapping, caption strength,
and encoding plan, and mark visual-only checks (post-scaling font size, overlap, raster artifacts,
color contrast) as **`[user-verify]`** rather than guessing.
