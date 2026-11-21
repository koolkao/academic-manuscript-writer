# Source and license review

Checked 2026-11-21 via the GitHub API and local git inspection. Factual license review, not legal
advice.

| # | Source | Pinned revision / inspection date | License | Reuse decision |
|---|---|---|---|---|
| 1 | [Rimagination/good-story](https://github.com/Rimagination/good-story) | `main` `978c44d977c6` (2026-06-28) | MIT | Ideas synthesized (story as resolved tension, source-depth rule, audience contract, 2–4 candidate spines). All text written originally. |
| 2 | [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) `skills/figure-designer` | `main` `ab4b9ceac229` (2026-11-21); path `4c718106bd5d` (2026-11-20) | **CC-BY-NC-SA-4.0** | **Ideas only.** Never copy or closely paraphrase text; adapting wording would trigger NC-SA obligations incompatible with MIT. |
| 3 | [moonlarry/codex-paper-skills](https://github.com/moonlarry/codex-paper-skills) `paper_skills/paper-plan` | `main` `f9d62749a423` (2026-08-01); path `ca3e9e9901eb` (2026-05-31) | **None asserted** | **Ideas only.** Write all text originally. |
| 4 | [SaltGardenia/sci-story-skills](https://github.com/SaltGardenia/sci-story-skills) | `main` `56bc2d92e93e` (2026-09-12) | MIT | Ideas synthesized (one-sentence thesis test, claim-evidence mapping, impact-vs-effort revision ranking). All text written originally. |
| 5 | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) `skills/scientific-writing` & `skills/citation-management` | `main` `ec59a29a03d5` (2026-11-16); path `a92663a0214b` (2026-10-01) | MIT | Ideas synthesized (reporting-guideline awareness, claim-evidence consistency; citation tooling kept external). All text written originally. |
| 6 | [Gavin-Tao/claude-skills](https://github.com/Gavin-Tao/claude-skills) `academic-paper-writing` | `main` `713310bff97d` (2026-11-02) | **None asserted** | **Ideas only** ("sweep, don't patch", structural-not-prose mirroring, unattackable claim discipline, zero placeholders). Write all text originally. |
| 7 | [felixschrimpff/academic-writing-skill](https://github.com/felixschrimpff/academic-writing-skill) | `main` `86ea3ee3f8b9` (2026-09-14) | MIT | Ideas synthesized (structural AI-draft tells: no reading instructions, no counted prefaces, no self-ranking, proportionate caveats, field-calibrated signposting and first-person plural). All text written originally. |
| 8 | [labarba/sciwrite](https://github.com/labarba/sciwrite) | Inspected 2026-11-21 (`skills/sciwrite`, default branch) | **CC-BY-4.0** (based on Kristin Sainani CC-BY lectures) | **Ideas only** (mode scaling, source-markup preservation, Nature summary-paragraph moves). Write all text originally; cite published pedagogy conceptually. |
| 9 | [kgraph57/paper-writer-skill](https://github.com/kgraph57/paper-writer-skill) | Inspected 2026-11-21 (default branch) | **None asserted** | **Ideas only** (human-sovereign IDEA/DATA gates, adversarial red-team kill-switch, EQUATOR table). Write all text originally. |
| 10 | [koolkao/academic-humanizer](https://github.com/koolkao/academic-humanizer) (companion skill) | `53777babda5b` (2026-11-16, v0.2.0) | MIT *(with upstream attribution notice, fork of AIScientists-Dev/academic-humanizer)* | Direct integration target. Handoff contract in `references/humanizer-handoff.md` and lock-safe declaration regex grounded in this exact revision. |

## Foundational published writing pedagogy (conceptual references, not copied text)

- Mensh B, Kording K (2017). *Ten simple rules for structuring papers*. PLOS Computational Biology.
- Gopen GD, Swan JA (1990). *The science of scientific writing*. American Scientist.
- Schimel J (2012). *Writing Science: How to Write Papers That Get Cited and Proposals That Get Funded*. Oxford University Press.
- Rougier NP, Droettboom M, Bourne PE (2014). *Ten simple rules for better figures*. PLOS Computational Biology.
- Sainani K. *Writing in the Sciences* (Stanford).

## License posture

All prose, templates, scripts, tests, and worked examples in `academic-manuscript-writer` are
written from scratch and released under the MIT License. No text or code was copied from
CC-BY-NC-SA-4.0, CC-BY-4.0, or unlicensed repositories.
