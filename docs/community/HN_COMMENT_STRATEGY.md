# Founder Comment Strategy

**Rule:** Do not promote A2A Hub. Only contribute technical insight.

The goal is to be a useful participant in the community. When people recognize your username as someone who knows what they're talking about, the Show HN becomes a natural next step.

---

## Example Comments

### 1. On an A2A protocol discussion

> I've been working with the A2A protocol for a few months. The Agent Card schema is well-designed for describing capabilities, but there are a few gaps worth noting:
>
> - Cards are static — there's no heartbeat or liveness check. If an agent goes offline, its Card doesn't reflect that.
> - There's no standard way to express pricing or rate limits in the Card.
> - The `/.well-known/agent.json` convention is borrowed from web standards, which is sensible, but it means every agent needs an HTTP server just to be discoverable.
>
> The protocol handles task delegation well, but discovery and trust are left as ecosystem problems. That's probably intentional — Google scoped A2A to communication, not discovery.

### 2. On an "Ask HN: Is anyone using the A2A protocol?" thread

> Yes, we've been experimenting with it. The protocol itself is straightforward — the Card schema is well-documented and the task lifecycle (tasks/submit → tasks/send → tasks/get → tasks/cancel) covers the common patterns.
>
> The harder part is the ecosystem around it. Finding other A2A agents requires either knowing their URL in advance or relying on word of mouth. There's no directory, no registry, no way to discover agents you don't already know about.
>
> We ended up building a small crawler that indexes Agent Cards from known sources. It's not a product — more of an experiment to understand what a discovery layer would need.
>
> The protocol is solid. The discovery problem is unsolved.

### 3. On an MCP vs A2A discussion

> I've worked with both MCP and A2A. They're solving different problems, which isn't always clear from the coverage.
>
> MCP gives LLMs access to tools (files, databases, APIs). It's about capability exposure from a single agent to external resources.
>
> A2A is about agent-to-agent communication — task delegation between independently operated agents.
>
> They're complementary. An agent could use MCP internally to access tools, and A2A externally to coordinate with other agents. The confusion comes from people comparing them as alternatives when they're really different layers of the stack.
>
> The interesting question is whether they'll converge. Some projects are already building bridges.

### 4. On an agent trust/safety discussion

> One challenge I keep coming back to: how do you verify an agent is who it claims to be?
>
> The A2A Card includes a `url` field pointing to the agent's endpoint, but there's no signature, no certificate, no way to prove the Card publisher controls the endpoint. Anyone could publish a Card claiming to be any agent.
>
> For the protocol to work at scale, there needs to be some form of identity binding — either DNS-based (the Card is served from the agent's domain) or cryptographic (the Card is signed by a key the agent controls).
>
> The DNS approach is simpler but doesn't prevent domain squatting. The cryptographic approach is more robust but adds friction to onboarding.
>
> I don't have a clean answer, but it's the question that keeps me up at night.

### 5. On an open-source infrastructure discussion

> We chose SQLite for our MVP specifically because we wanted zero operational overhead. No Postgres to manage, no Redis to configure, no background workers.
>
> The trade-off is obvious: SQLite doesn't scale to concurrent writes. But for an early-stage project, the ability to deploy with a single `docker run` command is worth more than theoretical scalability.
>
> Our philosophy: make it work, make it right, make it fast — in that order. SQLite gets us through "make it work" with room to grow.

### 6. On a "Show HN: [agent-related project]" thread

> Interesting approach. I've been thinking about the same problem from a different angle.
>
> One thing I'd be curious about: how do you handle agent metadata freshness? If an agent changes its capabilities or goes offline, how does your index reflect that?
>
> We ran into this with our own experiment. Our current solution is a TTL-based re-crawl, but it's naive — we re-crawl everything on a fixed schedule instead of prioritizing agents that are likely to have changed.

---

## Comment Checklist

Before posting any comment:

- [ ] Does this add technical substance?
- [ ] Am I promoting A2A Hub? (If yes, don't post)
- [ ] Am I speaking from experience?
- [ ] Is my tone curious, not certain?
- [ ] Would this be valuable if I had no project to promote?

If the answer to any of the first three is "no," rewrite.
