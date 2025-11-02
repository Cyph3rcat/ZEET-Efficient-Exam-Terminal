# ZEET — Zuper Efficient Exam Terminal

**ZEET** is an intelligent, terminal-based examination system that extracts content from educational materials (PDFs, slides, documents) and automatically generates contextually-aware exam questions using AI. The system supports multiple question types, adaptive difficulty modes, and provides an interactive exam-taking experience with real-time grading.

## 🎯 Project Goal

ZEET aims to revolutionize exam creation by:
- **Extracting** structured content from PDF slides, presentations, and documents
- **Mapping** content hierarchy and relationships across slides and topics
- **Grouping** related slides and content chunks for contextual question generation
- **Generating** diverse question types (MCQ, short answer, essay) with intelligent context awareness
- **Supporting** two primary generation modes:
  - **Discrete-Flexible**: Single-focus questions on specific concepts
  - **Sailboat/Exploratory**: Multi-layered, interconnected questions that explore relationships

## 📋 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ZEET System Pipeline                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. EXTRACTION LAYER                                         │
│     ├─ PDF/PPTX/DOCX Parser (pdfplumber, python-pptx)       │
│     ├─ OCR Fallback (pytesseract, pdf2image)                │
│     └─ Image/Circuit Detection                               │
│                                                               │
│  2. CONTENT MAPPING & HIERARCHY                              │
│     ├─ Build Content Map (slides → topics → concepts)        │
│     ├─ Establish Hierarchical Relationships                  │
│     └─ Cross-Reference Slides (map layers across courses)    │
│                                                               │
│  3. GROUPING & CHUNKING                                      │
│     ├─ Related Slide Grouping                                │
│     ├─ Content Chunking Strategy                             │
│     └─ Payload Generation (group → AI prompt)                │
│                                                               │
│  4. QUESTION GENERATION ENGINE                               │
│     ├─ AI Model Integration (GPT-4, Claude, etc.)            │
│     ├─ Question Type Detection & Selection                   │
│     ├─ Mode Selection (Discrete vs Exploratory)              │
│     └─ LaTeX/Math Processing                                 │
│                                                               │
│  5. PRESENTATION & INTERACTION                               │
│     ├─ Terminal UI (prompt_toolkit, Rich)                    │
│     ├─ Interactive Carousel Navigation                       │
│     ├─ Real-time Input & Auto-grading                        │
│     └─ Session Management (save/resume)                      │
│                                                               │
│  6. ENHANCEMENT COMPONENTS                                   │
│     ├─ HIVE Citation System (internet/offline aggregator)    │
│     ├─ Image Sideview Tool (visual context)                  │
│     ├─ Math Library & LaTeX Processor                        │
│     └─ Citation JSON (reduce hallucination)                  │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Implementation Pipeline

### Phase 1: Content Extraction ✅ (Partial)
**Status**: Basic extraction implemented, needs enhancement

**Tasks**:
- [x] Basic PDF text extraction (pdfplumber)
- [x] PPTX slide content extraction
- [x] DOCX paragraph extraction
- [ ] Enhanced OCR for image-heavy slides
- [ ] Circuit diagram detection and extraction
- [ ] Mathematical equation recognition (LaTeX)
- [ ] Image metadata extraction and cataloging
- [ ] Multi-column layout handling

**Files**: `ZEET/extractor.py`

### Phase 2: Content Mapping & Hierarchy ⏳
**Status**: Not yet implemented

**Tasks**:
- [ ] Build content hierarchies (course → topic → subtopic)
- [ ] Identify slide relationships and dependencies
- [ ] Create topic maps across multiple documents
- [ ] Tag slides with subject matter categories
- [ ] Extract learning objectives from content
- [ ] Build knowledge graph of concepts

**Proposed Files**: `ZEET/mapper.py`, `ZEET/hierarchy.py`

### Phase 3: Grouping & Chunking Strategy ⏳
**Status**: Not yet implemented

**Tasks**:
- [ ] Implement slide grouping algorithm
- [ ] Smart chunking based on content type
- [ ] Create payload structure for AI prompts
- [ ] Cross-slide context aggregation
- [ ] Related content clustering
- [ ] Optimal chunk size determination (token limits)

**Proposed Files**: `ZEET/chunker.py`, `ZEET/grouping.py`

### Phase 4: Question Generation Engine ⏳
**Status**: Template structure exists, AI integration needed

**Tasks**:
- [ ] Integrate AI model API (OpenAI, Anthropic, local LLMs)
- [ ] Implement question type detection
- [ ] Build prompt templates for each question type
- [ ] Create discrete-flexible mode generator
- [ ] Create sailboat/exploratory mode generator
- [ ] Implement difficulty level adjustment
- [ ] Add subject-specific generation rules
- [ ] Generate multiple questions per payload
- [ ] LaTeX math expression generation

**Files**: `ZEET/gen.py` (stub exists), `ZEET/adapter.py` (API integration)

### Phase 5: LaTeX & Math Processing ⏳
**Status**: Not yet implemented

**Tasks**:
- [ ] LaTeX parser and renderer
- [ ] Math expression extraction from PDFs
- [ ] Symbolic math question generation
- [ ] Math library integration (default formulas)
- [ ] Equation verification system

**Proposed Files**: `ZEET/latex_processor.py`, `ZEET/math_lib.py`

### Phase 6: HIVE Citation System ⏳
**Status**: Not yet implemented

**Tasks**:
- [ ] Web scraper for relevant educational content
- [ ] Local textbook ingestion pipeline
- [ ] Citation JSON format definition
- [ ] Offline knowledge aggregator
- [ ] Source attribution system
- [ ] Hallucination reduction via citations
- [ ] Fact-checking against sources

**Proposed Files**: `ZEET/hive/scraper.py`, `ZEET/hive/aggregator.py`, `ZEET/hive/citations.py`

### Phase 7: Image Sideview Tool ⏳
**Status**: Not yet implemented

**Tasks**:
- [ ] Image extraction and display
- [ ] Side-by-side image viewer in terminal
- [ ] Image-based question support
- [ ] Circuit diagram visualization
- [ ] Image annotation capabilities

**Proposed Files**: `ZEET/image_viewer.py`

### Phase 8: UI Enhancements ✅ (Partial)
**Status**: Core UI implemented, needs polish

**Tasks**:
- [x] Terminal UI framework (prompt_toolkit)
- [x] Interactive menu system
- [x] Question carousel navigation
- [x] Session save/resume functionality
- [ ] Progress visualization improvements
- [ ] Help system and documentation
- [ ] Keyboard shortcuts documentation
- [ ] Accessibility features

**Files**: `ZEET/zeet.py`, `ZEET/render.py`, `ZEET/animate.py`

## 📝 Question Generation Types & Modes

### Question Types

#### 1. Multiple Choice Questions (MCQ)
- **Best for**: Facts, definitions, quick recall
- **Generation**: Extract key concepts, generate plausible distractors
- **Auto-grading**: Exact match comparison
- **Subjects**: All subjects, especially foundational concepts

#### 2. Short Answer
- **Best for**: Definitions, brief explanations, calculations
- **Generation**: Focused on specific concepts from slide content
- **Auto-grading**: Token overlap, keyword matching
- **Subjects**: All subjects, technical definitions

#### 3. Essay/Long Answer
- **Best for**: Analysis, synthesis, critical thinking
- **Generation**: Complex prompts requiring multi-slide context
- **Auto-grading**: AI-assisted evaluation (requires human review)
- **Subjects**: Ethics, philosophy, engineering design

### Generation Modes

#### Discrete-Flexible Mode
- **Focus**: Single concept per question
- **Context**: Limited to 1-3 slides
- **Complexity**: Low to medium
- **Use cases**: 
  - Quick assessments
  - Foundational knowledge testing
  - Mathematics (isolated problems)
  - Engineering fundamentals
- **Question flow**: Independent, can be randomized

#### Sailboat/Exploratory Mode
- **Focus**: Multi-layered, interconnected concepts
- **Context**: Spans multiple slides/topics
- **Complexity**: Medium to high
- **Use cases**:
  - Ethics discussions (multi-perspective analysis)
  - Engineering design (system-level thinking)
  - Complex problem-solving
  - Cross-domain applications
- **Question flow**: Progressive, building on previous answers

### Subject-Specific Recommendations

| Subject | Recommended Mode | Question Types | Special Considerations |
|---------|------------------|----------------|------------------------|
| **Mathematics** | Discrete-Flexible | MCQ, Short Answer | Requires LaTeX support, step-by-step solutions |
| **Ethics** | Sailboat/Exploratory | Essay, Short Answer | Multi-perspective analysis, case studies |
| **Engineering** | Both | All types | Circuit diagrams, system design, calculations |
| **Computer Science** | Discrete-Flexible | MCQ, Short Answer | Code snippets, algorithm analysis |
| **Physics** | Discrete-Flexible | MCQ, Short Answer | Equations, diagrams, problem-solving |

### Limitations

- **Images**: Current OCR may struggle with complex diagrams
- **Circuits**: Specialized extraction for circuit diagrams not yet implemented
- **Handwriting**: OCR performance varies with handwritten content
- **Mathematical notation**: LaTeX extraction needs improvement
- **Context understanding**: AI may miss nuanced relationships without proper grouping

## 🗂️ Current Repository Structure

```
ZEET-Efficient-Exam-Terminal/
├── README.md                    # This file
├── ZEET/                        # Main application directory
│   ├── zeet.py                  # Entry point, main terminal UI orchestration
│   ├── structures.py            # Data models (QuestionState, Session)
│   ├── extractor.py             # PDF/PPTX/DOCX extraction (basic impl)
│   ├── gen.py                   # Question generation (stub, needs AI integration)
│   ├── adapter.py               # API adapter (placeholder for LLM integration)
│   ├── render.py                # UI rendering, menu and carousel
│   ├── animate.py               # Boot sequence and splash screen animations
│   ├── soundsfn.py              # Sound effects wrapper (pygame)
│   ├── config.json              # User configuration and styling
│   └── __pycache__/             # Python cache
├── sessions/                    # Session save files (created at runtime)
├── documents/                   # Input documents directory (user-provided)
└── sounds/                      # Optional sound effect files

Proposed additions:
├── ZEET/
│   ├── mapper.py                # Content hierarchy mapping
│   ├── hierarchy.py             # Hierarchical relationship builder
│   ├── chunker.py               # Content chunking engine
│   ├── grouping.py              # Slide grouping logic
│   ├── latex_processor.py       # LaTeX parsing and rendering
│   ├── math_lib.py              # Default math formulas library
│   ├── image_viewer.py          # Terminal image display
│   └── hive/                    # HIVE citation system
│       ├── scraper.py           # Web content scraper
│       ├── aggregator.py        # Offline knowledge aggregator
│       └── citations.py         # Citation management
├── tests/                       # Unit and integration tests
└── docs/                        # Extended documentation
```

## 🚀 Example Workflow

### Basic Usage Flow

```bash
# 1. Start ZEET
cd ZEET
python zeet.py

# 2. Select "New Session" from menu

# 3. System scans documents/ directory for PDFs, PPTX, DOCX

# 4. Select file to extract

# 5. Extractor parses content → creates content blocks

# 6. Mapper builds hierarchy and relationships

# 7. Grouper creates content payloads

# 8. Generator calls AI to create questions

# 9. Interactive carousel displays questions

# 10. Student answers questions

# 11. Auto-grading provides immediate feedback

# 12. Session saved for resume later
```

### Advanced: Sailboat Mode for Ethics

```
Input: Ethics course slides on "Ethical Frameworks"
↓
Extraction: Pulls content on Utilitarianism, Deontology, Virtue Ethics
↓
Grouping: Creates payload spanning all three frameworks
↓
Generation (Sailboat Mode):
  Q1: Define each ethical framework (warmup)
  Q2: Compare utilitarianism and deontology (connection)
  Q3: Apply frameworks to a real-world scenario (synthesis)
  Q4: Critique the limitations of each approach (analysis)
↓
Student progresses through interconnected questions
```

## ✅ TODO Checklist & Priorities

### High Priority (MVP - Minimum Viable Product)
- [ ] **Issue #1**: Implement AI model integration (adapter.py)
  - Connect to OpenAI/Anthropic API
  - Create prompt templates
  - Handle API responses
- [ ] **Issue #2**: Build content mapper and hierarchy builder
  - Extract slide titles and structure
  - Create topic taxonomy
  - Link related content
- [ ] **Issue #3**: Implement chunking and grouping algorithm
  - Define optimal chunk sizes
  - Group related slides
  - Generate AI prompts from groups
- [ ] **Issue #4**: Complete question generation engine (gen.py)
  - Discrete-flexible mode
  - Basic MCQ and short answer generation
  - Integration with extractor

### Medium Priority (Enhanced Features)
- [ ] **Issue #5**: LaTeX and math processing
  - Parse mathematical expressions
  - Render LaTeX in terminal
  - Generate math-specific questions
- [ ] **Issue #6**: Sailboat/Exploratory mode implementation
  - Progressive question chains
  - Context preservation across questions
  - Difficulty ramping
- [ ] **Issue #7**: Enhanced OCR for images and circuits
  - Better image preprocessing
  - Circuit diagram detection
  - Technical diagram extraction
- [ ] **Issue #8**: Image sideview tool
  - Extract and display images
  - Image-based question support
  - Terminal image rendering

### Low Priority (Nice-to-Have)
- [ ] **Issue #9**: HIVE citation system
  - Web scraper
  - Local textbook ingestion
  - Citation JSON format
  - Hallucination reduction
- [ ] **Issue #10**: UI/UX polish
  - Better progress indicators
  - Help documentation
  - Themes and customization
- [ ] **Issue #11**: Advanced grading
  - AI-assisted essay grading
  - Partial credit algorithms
  - Rubric-based evaluation
- [ ] **Issue #12**: Multi-user support
  - User profiles
  - Class management
  - Grade export

### Future Enhancements
- [ ] **Issue #13**: Real-time collaboration mode
- [ ] **Issue #14**: Question bank management
- [ ] **Issue #15**: Analytics dashboard
- [ ] **Issue #16**: Mobile/web interface
- [ ] **Issue #17**: LMS integration (Moodle, Canvas)

## 🛠️ Developer Guide

### Setup

```bash
# Clone repository
git clone https://github.com/Cyph3rcat/ZEET-Efficient-Exam-Terminal.git
cd ZEET-Efficient-Exam-Terminal

# Install dependencies
pip install rich prompt_toolkit pygame python-dotenv
pip install pdfplumber python-pptx python-docx pytesseract pdf2image pillow

# Optional: Install system dependencies for OCR
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr poppler-utils

# macOS:
brew install tesseract poppler

# Configure API keys (for AI integration)
# Edit ZEET/config.json and add your API key:
# "model": {
#   "api_key": "your_api_key_here",
#   "model": "gpt-4"
# }

# Create required directories
mkdir -p documents sessions sounds

# Optional: Add sound effects
# Place switch.mp3, button.mp3, grade.mp3 in sounds/

# Run ZEET
cd ZEET
python zeet.py
```

### Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/your-feature`)
3. **Make** your changes with clear, focused commits
4. **Test** your changes thoroughly
5. **Document** new features in relevant docstrings
6. **Submit** a pull request with a clear description

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings for all public functions
- Keep functions focused and modular
- Write descriptive variable names

### Testing

```bash
# Currently, no automated tests exist
# Manual testing workflow:

# 1. Test extraction
python -c "from extractor import extract_pdf; print(extract_pdf('test.pdf'))"

# 2. Test UI components
python animate.py  # View animations
python zeet.py     # Full application test

# 3. Test session save/resume
# - Create new session
# - Answer questions
# - Quit and save
# - Resume session
# - Verify state persisted

# Future: Add pytest framework
# pip install pytest
# pytest tests/
```

### Project Conventions

- **Session files**: JSON format in `sessions/` directory
- **Input documents**: Place in `documents/` directory
- **Configuration**: Edit `ZEET/config.json` for customization
- **Color scheme**: Cyan/green terminal theme (configurable)
- **Data models**: Use dataclasses in `structures.py`

## 📚 Additional Resources

### Dependencies Documentation
- [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/) - Terminal UI framework
- [Rich](https://rich.readthedocs.io/) - Rich text and formatting
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF text extraction
- [python-pptx](https://python-pptx.readthedocs.io/) - PowerPoint manipulation
- [pytesseract](https://pypi.org/project/pytesseract/) - OCR engine

### AI Model APIs
- [OpenAI API](https://platform.openai.com/docs/) - GPT models
- [Anthropic API](https://docs.anthropic.com/) - Claude models
- [Ollama](https://ollama.ai/) - Local LLM deployment

## 📄 License

This project is open source. Please check the repository for license details.

## 🤝 Contributing & Support

Contributions are welcome! Please follow the developer guide above and submit PRs for review.

For issues, questions, or feature requests, please open an issue on the GitHub repository.

---

**Built with ❤️ for efficient exam creation and taking**