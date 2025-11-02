# ZEET — Efficient Exam Terminal

Purpose
-------
ZEET (Efficient Exam Terminal) is a pipeline and toolkit to convert slide/pdf teaching materials into structured question banks. It extracts content from PDFs/slides, builds a contextual content map and hierarchy, groups related content, and generates multiple question types (MCQ, essay, exploratory). The system is designed to support subject-specific generation modes (e.g., math vs ethics), reduce hallucination via curated citations, and accept both local and online resource inputs.

High-level goals
----------------
- Extract text, images and layout from slides/PDFs (OCR when needed).
- Build a content map and hierarchical context to preserve section/slide relationships.
- Group related slides/content into coherent chunks for question generation.
- Generate question sets in different modes:
  - Discrete-flexible: anchored in slide facts but allows controlled expansion.
  - Sailboat / exploratory: uses slides as scaffolding and brings in external sources.
- Provide tooling for math/LaTeX, image-sideview processing, and a "HIVE" citation aggregator to reduce hallucinations.

Core concepts
-------------
- Content Map: structured representation of a slide deck (slides, headings, bullets, images, figures, equations).
- Hierarchy: relationships between sections, subsections, and slides used to provide context.
- Chunk / Group: one or more related slides combined into a payload for generation.
- Modes:
  - Discrete-flexible: factual, slide-focused generation (MCQs, short/long answer).
  - Sailboat / Exploratory: creative, reference-backed generation using external sources.
- HIVE: a citation-first resource aggregator (online scraper + local resource index) that provides JSON citations and mitigates hallucinations.

Pipeline (proposed)
-------------------
1. Ingest
   - Input: PDF, PPTX, images, local textbook PDFs, or URLs to online resources.
   - If needed, run OCR (fast/accurate modes).
2. Parse & Normalize
   - Extract text, layout metadata, images, embedded equations.
   - Normalize fonts, detect headings, bullets, numbered lists.
3. Build Content Map + Hierarchy
   - Identify slides → sections → subsections.
   - Tag semantic elements (definition, example, theorem, proof, diagram).
   - Store as JSON (with slide IDs and positional metadata).
4. Group Related Content
   - Use heuristics and embeddings (optional) to group slides by topic and level.
   - Example: map "layer 1" slides across CCNA modules together.
5. Chunking and Question Type Detection
   - Decide chunk size (single slide, 2–4 slides, whole section).
   - Detect suitable question types (MCQ, essay, worked problem).
   - For math/science, detect presence of equations/diagrams and route to specialized generators.
6. Question Generation
   - Two primary modes:
     - Discrete-flexible: generate MCQs, short answers, and essays relying mainly on slide content + small controlled expansions.
     - Sailboat/exploratory: use slides as scaffolding and query HIVE (online + offline) for additional context and citation-backed content.
   - Output: question JSON with type, difficulty, choices, solution, hints, and citation metadata.
7. Post-processing & QA
   - Validate LaTeX/math rendering, image referencing, and citation completeness.
   - Optionally run automatic plausibility checks (answer-key verification).
8. Export & Delivery
   - Formats: JSON, CSV, Moodle XML, printable PDFs.
   - Optionally: build a question bank with tagging, difficulty, and linked slide references.

Question types & generation strategies
--------------------------------------
- Discrete MCQ
  - Entirely slide-based factual items.
  - Distractors: generated from nearby slide bullet points or common misconceptions.
  - Minimal external context.
- Discrete Essay
  - Slide-driven prompts that ask for explanations, comparisons, short analyses using only slide content.
- Expedition / Exploratory
  - Open-ended prompts that ask for synthesis beyond slides.
  - Requires external citations pulled from HIVE (online scrapers, textbooks, past papers).
  - Good for subjects where exploring implications and applications matters (e.g., engineering ethics, systems design).
- Special handling for Math/Technical Problems
  - Use a LaTeX-aware generator and solver pipeline.
  - Include a math library for canonical derivations and a renderer for verification.
  - Provide step-by-step solution generation and optional numerical checker.

HIVE — citation aggregator idea
-------------------------------
- Purpose: reduce hallucination and provide provenance.
- Components:
  - Online scraper: configurable sources (open textbooks, past papers, reputable websites).
  - Local indexer: watches a directory for uploaded textbooks / PDFs and indexes them.
  - Fast OCR + parser for scraped PDFs.
  - Citation JSON format for each supporting document (source id, url/local path, excerpt, confidence).
- Usage:
  - Exploratory mode queries HIVE for candidate references, returns citations with snippets and confidence levels.
  - Discrete mode can still consult HIVE to check edge cases or clarify ambiguities.

Chunking & payload strategy
---------------------------
- Payload = the grouped chunk (slides + extracted text + images + hierarchy context + metadata).
- Within a chunk, the generator can produce multiple questions of varying types.
- Chunk-level metadata: topic label, estimated difficulty, required tools (LaTeX, images).
- Heuristics:
  - Prefer small chunks for dense slides (1–2 slides).
  - Group conceptually linked slides for higher-level or integrative questions.
  - Allow user override or reviewer templating to force chunk sizes and question quotas.

Subject-specific recommendations
--------------------------------
- Math/Physics:
  - Strong LaTeX support and numerical validators.
  - Prefer chunking by worked examples and theorems.
  - Use external sources for alternative problem styles and datasets.
- Engineering ethics / Humanities:
  - Slide content typically suffices for prompts; exploratory mode used sparingly for context.
  - Focus on open-ended prompts, scenario generation, and graded rubrics.
- Circuit analysis, diagrams-heavy topics:
  - Image-sideview tooling required; consider specialized OCR for circuit symbols.
  - When images are missing or low quality, degrade to concept questions only.

Limitations & caveats
---------------------
- Image-only slides may lose fidelity if diagrams are unreadable.
- Hallucination risk increases with exploratory mode — mitigate by HIVE citations and confidence scoring.
- Resource cost: scraping and indexing external content can be expensive and requires source legality checks.
- Privacy: local documents should remain private unless explicitly allowed for online indexing.

Proposed architecture & repository mapping
------------------------------------------
- Core services:
  - ingest/ — modules to accept files (pdf, pptx, image), run OCR
  - parse/ — parsers that extract text, layout, structure
  - map/ — content-map builder and hierarchy manager
  - group/ — grouping / chunking logic (embeddings & heuristics)
  - gen/ — question generation models & mode orchestrator (discrete vs exploratory)
  - hive/ — citation aggregator, scraper, and local indexer
  - tools/ — LaTeX processor, math solver, image-sideview tools
  - export/ — converters to JSON/Moodle/XML/PDF
  - web/ or cli/ — user interfaces and orchestration entrypoints
- If exact mapping is unknown: maintainers should update this section with actual directories and file roles. The repo can adopt these folders or map existing ones to these roles.

Example quick workflow (developer view)
---------------------------------------
1. Add a sample PDF to /examples.
2. Run ingest/ to produce normalized JSON (examples/output/content.json).
3. Run map/ to create content_map.json with slide hierarchy.
4. Run group/ to produce chunks/ directory (chunk_001.json...).
5. Run gen/ on chunk_001.json with mode=discrete-flexible to produce questions_001.json.
6. Run postprocessing to validate LaTeX and images.
7. Export to /exports/ as Moodle XML or JSON.

Implementation TODO (prioritized)
--------------------------------
- P0 (high priority)
  - Implement ingest parser for PDFs and PPTX with OCR fallback.
  - Create content map JSON schema and basic mapper.
  - Add a generator stub for discrete-flexible MCQs.
  - Add unit tests for parsing and mapping.
- P1
  - Grouping heuristics and simple embedding-based similarity service.
  - Chunk JSON schema and chunker implementation.
  - Simple LaTeX rendering validator and math library integration.
- P2
  - HIVE local indexer (directory watch + PDF indexing).
  - Online scraper prototype (configurable sources).
  - Exploratory generation mode with citation JSON output.
- P3
  - Advanced image-sideview tooling (diagram OCR, circuit symbol detection).
  - Exporters (Moodle, CSV, printable PDF).
  - QA dashboard and manual review tools.
- P4 (future)
  - Full web UI, user authentication, multi-user question bank management.
  - Integrations with LMSes and automated test generation.

Developer guide (short)
-----------------------
- Contributing:
  - Fork > feature branch > PR with tests.
  - Use the repository's linting and test tools (add here once known).
- Testing:
  - Add unit tests near each module (ingest/test_*, parse/test_*, gen/test_*).
  - Add example corpora in /examples for CI test runs.
- Running locally:
  - Suggested dev container or environment with Python/Node and Tesseract for OCR.
  - Document required environment variables for web scrapers/API keys (HIVE).

Example JSON outputs (brief)
----------------------------
- content_map.json
  - slides: [{id, order, headings, bullets, images, equations, raw_text}]
  - sections: [{id, title, slide_ids}]
- chunk_x.json
  - chunk_id, slide_ids, topic_labels, estimated_difficulty, payload (extracted text + images)
- question.json
  - id, chunk_id, type, prompt, choices (if MCQ), answer, hints, explanation, citations: [{source_id, excerpt, url_or_path, confidence}]

Notes & next steps
------------------
- This README is intended to be actionable; it supports creating a prioritized issue list from the TODOs above.
- Recommended immediate next action: add the ingest/parser and content-map schema as a first PR so downstream modules can rely on stable JSON formats.

- Add your preferred license (e.g., MIT) to LICENSE.
- Add an AUTHORS or CONTRIBUTORS file as desired.
