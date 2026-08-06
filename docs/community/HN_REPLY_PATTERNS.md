# HN Reply Patterns

**Rule:** No promotion. No project mentions. Add value first.

---

## 1. Someone skeptical about AI agents

> "AI agents are just hype. Nothing works reliably."

**Reply pattern:**

> I think the skepticism is fair for the autonomous-agent-as-a-service category. But the protocol layer is different — it's just a standard way to describe capabilities and exchange messages.
>
> The A2A spec is essentially: here's a JSON schema for what your agent does, here's how to send it a task, here's how to get the result. No autonomy, no promises about reliability.
>
> The hype is around what people build on top. The protocol itself is boring infrastructure, which is probably a good thing.

---

## 2. Someone asking "why another protocol?"

> "Why do we need A2A when we already have MCP/OpenAPI/gRPC?"

**Reply pattern:**

> They solve different things. MCP gives LLMs access to tools — it's about capability exposure from one agent to external resources. A2A is about agent-to-agent task delegation.
>
> An agent might use MCP internally to query a database, then use A2A to hand off a subtask to another agent that specializes in something else.
>
> The confusion is understandable because both involve agents and JSON. But one is "how do I let my agent use a tool" and the other is "how do my agent and your agent talk to each other."
>
> Whether we need both long-term is an open question. Some projects are already building bridges between them.

---

## 3. Someone comparing MCP and A2A

> "MCP is better because it's simpler / more adopted / backed by Anthropic."

**Reply pattern:**

> MCP has more adoption right now, partly because it's been around longer and partly because the use case (LLM needs a tool) is more immediately obvious than (agent needs another agent).
>
> But they're not really in competition. MCP is a tool protocol. A2A is an agent protocol. You could build an A2A agent that uses MCP internally for tool access.
>
> The interesting question is whether the ecosystem converges on one or keeps both. My guess is they stay separate because the abstractions are different — MCP is about capability exposure, A2A is about task delegation. Different primitives.

---

## 4. Someone discussing agent safety

> "How do we stop agents from doing harmful things?"

**Reply pattern:**

> There are two separate problems: capability safety (what the agent can do) and identity safety (who the agent is).
>
> Capability safety is about scoping — the agent should only have access to what it needs. This is a systems architecture problem, not an AI problem.
>
> Identity safety is harder. If my agent receives a task from "your agent," how does it know it's really you? The A2A Card has a url field but no signature. Anyone could publish a Card claiming to be any agent.
>
> DNS-based verification (the Card is served from the agent's domain) is the simplest approach but doesn't prevent domain squatting. Cryptographic signing is more robust but adds friction.
>
> I don't think there's a clean answer yet. It's an open research question.

---

## 5. Someone discussing open-source infrastructure

> "Building open-source infrastructure is hard because nobody pays for it."

**Reply pattern:**

> It depends on where in the stack you are. Infrastructure that solves a clear pain point (like "I need to find X") can get adoption even without a business model. The challenge is staying focused on the problem instead of expanding scope.
>
> The pattern I've seen work: build something simple that solves one problem well, get users, then figure out sustainability. Trying to design the business model before you have users is premature.
>
> Open-source infra projects that fail usually fail because they tried to do too much too fast, not because nobody would pay.

---

## 6. Someone asking about agent discovery

> "How do you even find agents to use?"

**Reply pattern:**

> This is the question that doesn't have a good answer yet. Right now it's word of mouth, GitHub searches, and following specific projects.
>
> The A2A protocol defines a standard location for agent metadata (`/.well-known/agent.json`), which is a good start — it means every A2A agent has a predictable URL for its Card. But there's no index, no registry, no way to discover agents you don't already know about.
>
> It's like the early web before search engines. The protocol (HTTP) and the content format (HTML) existed, but finding pages required knowing the URL in advance.
>
> Someone will solve this eventually. The question is whether it's a centralized registry, a federated system, or something else entirely.

---

## 7. Someone asking about protocol adoption

> "Is anyone actually using A2A in production?"

**Reply pattern:**

> Adoption is early but growing. Google's ADK supports it, there are reference implementations in Python and TypeScript, and a few companies are experimenting with it internally.
>
> The bigger barrier isn't the protocol quality — it's the ecosystem. A2A is most valuable when there are many agents to communicate with, but there won't be many agents until the protocol is adopted. Classic chicken-and-egg.
>
> The protocol itself is solid. The Card schema is well-documented, the task lifecycle covers the common patterns, and the security model (though basic) is reasonable for v1.
>
> I'd say it's worth experimenting with if you're building multi-agent systems. Just don't expect a thriving ecosystem yet.
