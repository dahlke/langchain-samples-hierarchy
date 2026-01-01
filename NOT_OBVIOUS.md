# Repositories Needing Category Labels

This file tracks repositories that don't have obvious categorization based on their current topics/labels. These should be labeled to match the LangChain product structure.

## Recommended Category Structure

Based on [LangChain's product hierarchy](https://www.langchain.com/):

### LangSmith (Agent Engineering Platform)
- **Observability** - Tracing, debugging, monitoring
- **Evaluation** - Evals, testing, quality assurance
- **Deployment** - CI/CD, production, infrastructure

### Open Source Frameworks
- **LangGraph** - Agent building, workflows, state machines
- **Deep Agents** - Planning, memory, long-running tasks
- **LangChain** - Framework integrations, utilities

### Integrations
- **MCP** - Model Context Protocol
- **Cloud Providers** - Azure, AWS Bedrock, etc.

---

## Repos Needing Labels

### Should be labeled `langsmith` + `observability`
| Repository | Current Topics | Suggested Topics |
|------------|---------------|------------------|
| `tracing-concepts` | _(none)_ | `langsmith`, `observability`, `beginner` |
| `langsmith-debug-concepts` | _(none)_ | `langsmith`, `observability`, `beginner` |
| `langsmith-debug` | _(none)_ | `langsmith`, `observability`, `intermediate` |
| `langsmith-in-code` | _(none)_ | `langsmith`, `observability`, `intermediate` |
| `remote-graph-distributed-tracing` | _(none)_ | `langsmith`, `observability`, `langgraph`, `advanced` |
| `ls-deployments-multi-project-tracing` | _(none)_ | `langsmith`, `observability`, `deployment`, `advanced` |
| `bedrock-otel-tracing-guide` | _(none)_ | `langsmith`, `observability`, `aws`, `intermediate` |
| `strands-otel-tracing-example` | _(none)_ | `langsmith`, `observability`, `strands`, `intermediate` |

### Should be labeled `langsmith` + `evaluation`
| Repository | Current Topics | Suggested Topics |
|------------|---------------|------------------|
| `eval-concepts` | _(none)_ | `langsmith`, `evaluation`, `beginner` |
| `eval-runner` | _(none)_ | `langsmith`, `evaluation`, `intermediate` |
| `eval-driven-dev` | _(none)_ | `langsmith`, `evaluation`, `intermediate` |

### Should be labeled `langsmith` + `deployment`
| Repository | Current Topics | Suggested Topics |
|------------|---------------|------------------|
| `cicd-pipeline-example` | _(none)_ | `langsmith`, `deployment`, `ci-cd`, `intermediate` |
| `strands-langsmith-deployment-instructions` | _(none)_ | `langsmith`, `deployment`, `strands`, `beginner` |
| `openai-compatible-endpoint` | _(none)_ | `langsmith`, `deployment`, `intermediate` |

### Should be labeled `langsmith` + `agent-builder`
| Repository | Current Topics | Suggested Topics |
|------------|---------------|------------------|
| `langsmith-agent-building` | _(none)_ | `langsmith`, `agent-builder`, `beginner` |

### Should be labeled `langgraph`
| Repository | Current Topics | Suggested Topics |
|------------|---------------|------------------|
| `azure-langgraph-agent` | _(none)_ | `langgraph`, `azure`, `intermediate` |
| `agent-oauth-example` | _(none)_ | `langgraph`, `authentication`, `intermediate` |
| `agent2agent` | _(none)_ | `langgraph`, `multi-agent`, `advanced` |

### Should be labeled `deep-agents`
| Repository | Current Topics | Suggested Topics |
|------------|---------------|------------------|
| `deepagent-gen-ui` | _(none)_ | `deep-agents`, `gen-ui`, `intermediate` |
| `deepagent-coder` | _(none)_ | `deep-agents`, `coding`, `intermediate` |

### Should be labeled `mcp` (Model Context Protocol)
| Repository | Current Topics | Suggested Topics |
|------------|---------------|------------------|
| `mcp-auth-demo` | _(none)_ | `mcp`, `authentication`, `intermediate` |

### Should be labeled `langchain`
| Repository | Current Topics | Suggested Topics |
|------------|---------------|------------------|
| `structured-prompt-hub` | _(none)_ | `langchain`, `prompts`, `intermediate` |

### Unclear / Needs Investigation
| Repository | Current Topics | Notes |
|------------|---------------|-------|
| `assistants-demo` | _(none)_ | OpenAI Assistants? LangGraph Assistants? Needs clarification |
| `inbox-demo` | _(none)_ | Purpose unclear from name alone |

### Meta / Should be excluded from display
| Repository | Notes |
|------------|-------|
| `.github` | GitHub org configuration, not a sample |

---

## Summary

**Total repos without proper labels: 25**

- Observability: 8 repos
- Evaluation: 3 repos
- Deployment: 3 repos
- Agent Builder: 1 repo
- LangGraph: 3 repos
- Deep Agents: 2 repos
- MCP: 1 repo
- LangChain: 1 repo
- Unclear: 2 repos
- Meta: 1 repo

