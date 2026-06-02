"""learning_os.py — [learner] Milestone M3 — the ORCHESTRATOR. Route → dispatch → synthesize.

This is the OS: one entrypoint over many specialists. It implements the orchestrator-workers pattern
— a central component that routes a request, "delegates [it] to worker [subsystems], and synthesizes
their results" (sources/articles/building-effective-agents.md). The synthesis step is where PROVENANCE
gets attached: every Response says which route handled the request and which stored items it used.

Keep `handle` THIN. Its whole job is: classify, dispatch to EXACTLY ONE subsystem, and wrap the
result with provenance. It must NOT retrieve, save, or touch the graph itself — that's a worker's job
(the provided SAVE worker is what persists and links). An orchestrator doing worker logic is the
§8 red flag.

PROVIDED: the Response dataclass.
LEARNER:  LearningOS.handle (M3).

Run:  python -m pytest tests/test_learning_os.py
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from router import route_query


@dataclass
class Response:
    """[provided] The OS's reply to one request — answer PLUS the audit trail.

    `route`/`reason`/`provenance` are not decoration: they're what make the system auditable. A caller
    (UI, test, evaluator) can always see which specialist ran, why, and which items the answer used.
    """
    answer: str
    route: str                       # which subsystem handled it (SAVE/RECALL/TASK/CHAT)
    reason: str                      # why the router chose that route
    provenance: list = field(default_factory=list)   # ids / sources the answer was built from


class LearningOS:
    """[learner] The Personal Learning OS — the front door over the provided subsystem kernel.

    subsystems: the route -> worker dispatch table from subsystems.make_subsystems(...).
    graph:      the KnowledgeGraph (held for inspection / extensions; the SAVE worker owns linking).
    """

    def __init__(self, subsystems: dict[str, Callable], graph=None) -> None:
        self.subsystems = subsystems
        self.graph = graph

    def handle(self, query: str) -> Response:
        """[learner] Route the request, dispatch to ONE subsystem, return a Response with provenance. (M3)

        Steps:
          1. route = route_query(query)                         # M1 — classify (precedence + safe default)
          2. worker = self.subsystems[route.name]               # look up the ONE specialist
          3. result = worker(query)                             # dispatch — a SubsystemResult(answer, sources)
          4. return Response(answer=result.answer, route=route.name, reason=route.reason,
                             provenance=result.sources)

        That's the whole orchestrator. Notice what it does NOT do: it doesn't search the store, doesn't
        save anything, doesn't add graph edges. Each worker owns its capability; `handle` only routes,
        calls exactly one worker, and attaches the audit trail.

        The traps:
          - Dispatch to EXACTLY ONE subsystem via the table — don't call several and merge, and don't
            inline a worker's logic here.
          - Put route/reason/provenance IN THE RETURNED Response (not a print) — that's the contract.

        Example (mirrors tests/test_learning_os.py::test_handle_*):
            os_.handle("remember the demo is June 20").route   -> "SAVE"   (provenance = [new item id])
            os_.handle("what did I save about the demo?").route -> "RECALL"
            os_.handle("explain routing").route                 -> "CHAT"  (provenance = [])
            # every Response carries route + provenance; exactly one worker is invoked.
        """
        route = route_query(query)
        worker = self.subsystems[route.name]
        result = worker(query)
        return Response(
            answer=result.answer,
            route=route.name,
            reason=route.reason,
            provenance=result.sources,
        )
