# NPC Qatar LMS — Visual Mockup

A static, front-end **visual prototype** of the Learning Management System described in the
NPC Qatar (National Planning Council — Statistical & Training Center) requirements document.

> ⚠️ This is a **look-and-feel mockup only**. There is no backend, database, or authentication —
> all data is hard-coded for demonstration. It is **not deployed/launched** anywhere.

## How to preview

It's plain HTML/CSS/JS — no build step. Either:

- **Double-click `index.html`** to open it in your browser, or
- Serve the folder locally:
  ```bash
  cd lms-mockup
  python3 -m http.server 8080
  # then open http://localhost:8080
  ```

## Pages

| File | Screen | Highlights |
|------|--------|-----------|
| `index.html` | Public landing page | Hero, announcements, featured courses, feature & role overview |
| `login.html` | Sign in | Tawtheeq (QID) / Active Directory SSO mock, role preview shortcuts |
| `dashboard.html` | Learner dashboard | Progress, learning path, AI recommendations, skill gaps, badges |
| `catalog.html` | Course catalog | Filters, semantic search, internal + aggregated external courses |
| `course.html` | Course player | Video/lesson, AI summary, curriculum, assessments, resources |
| `instructor.html` | Instructor studio | Grading queue (AI pre-graded), authoring tools, engagement analytics, sessions |
| `admin.html` | Admin console | KPIs, enrollment charts, users/roles, entities, approvals, finance |
| `ai.html` | AI assistant | Working demo chatbot, Learning DNA, adaptive next steps, AI capabilities |

## Demo touches that work

- **Language toggle (EN / ع)** in the top bar — flips the layout direction to RTL to preview Arabic support.
- **Chatbot** on `ai.html` — type a message (try "deadlines", "recommend a course", "progress") for a canned reply.
- All navigation links and role shortcuts are wired between pages.

## Requirement coverage (illustrative)

The mockup visually represents the major requirement areas from the scope document, including:
user & role management, course catalog & creation, course execution, assignments & assessments,
certification & badging, reporting & analytics dashboards (learner / instructor / admin / entity),
communication, **AI usability** (recommendations, auto-grading, conversational agent, avatars,
skill-gap analysis, adaptive paths), mobile & accessibility, integrations (Tawtheeq, AD/SSO,
HRMS/Mawared, Teams/Zoom, SCORM/xAPI), finance & cost management, and gamification.

## Design

- **Brand:** Qatar maroon (`#8a1538`) with gold accents.
- Self-contained design system in `assets/styles.css`; small interactions in `assets/app.js`.
- Responsive (desktop / tablet / mobile) and direction-aware (LTR/RTL).
