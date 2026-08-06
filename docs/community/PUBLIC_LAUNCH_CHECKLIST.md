# Public Launch Checklist

---

## Before Announcement

### Repository

- [ ] README is clear and complete
- [ ] Quick start works end-to-end
- [ ] API examples are accurate
- [ ] Architecture diagram is up to date
- [ ] Roadmap is visible
- [ ] License is present (Apache 2.0)
- [ ] CONTRIBUTING.md is clear
- [ ] CODE_OF_CONDUCT.md is present
- [ ] SECURITY.md is present
- [ ] CHANGELOG.md is updated
- [ ] .gitignore is correct

### GitHub Settings

- [ ] Repository description is set
- [ ] Topics are configured (9+ relevant topics)
- [ ] Issues are enabled
- [ ] Discussions are enabled
- [ ] Issue templates are configured (bug, feature, question)
- [ ] PR template is configured
- [ ] Labels are configured (good first issue, help wanted, etc.)
- [ ] Branch protection is configured (optional for MVP)

### Release

- [ ] Release tag is created (v0.1.0)
- [ ] Release notes are published
- [ ] Release artifacts are attached (if any)
- [ ] Release link is verified working

### Demo

- [ ] Local demo works: `python -m a2a_hub crawl && python -m a2a_hub serve`
- [ ] Tests pass: `pytest -q`
- [ ] Docker build works: `docker build -t a2a-hub .`
- [ ] Docker run works: `docker run --rm -p 8000:8000 a2a-hub`
- [ ] Screenshots or GIF of UI are prepared
- [ ] Public demo deployment is live (Railway/Render/Fly.io)

### Content

- [ ] Announcement post is drafted (LinkedIn, X/Twitter)
- [ ] Show HN submission is drafted
- [ ] Reddit posts are drafted
- [ ] GitHub Discussion announcement is drafted
- [ ] Outreach template is prepared

---

## After Announcement

### First 24 Hours

- [ ] Monitor GitHub Issues and Discussions
- [ ] Respond to all comments within 4 hours
- [ ] Fix any reported bugs immediately
- [ ] Thank early starrers and contributors
- [ ] Share announcement on personal networks

### First Week

- [ ] Publish first "Agents in the Wild" post
- [ ] Reach out to 10 A2A-compatible projects
- [ ] Respond to all feedback
- [ ] Update README based on initial feedback
- [ ] Fix any onboarding friction

### First Month

- [ ] Measure against 30-day goals
- [ ] Publish adoption retrospective
- [ ] Prioritize Phase 2 based on feedback
- [ ] Thank community publicly
