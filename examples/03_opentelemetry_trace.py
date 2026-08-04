"""03 — An OpenTelemetry trace with nested spans (conceptual)."""
print("Trace: chat_request")
print("  ├── retrieve_context (300ms)")
print("  │   ├── embed_query (50ms)")
print("  │   └── vector_search (250ms)")
print("  └── llm_call (1500ms)  ← the long pole")
print("\nSee src/distributed_tracing/README.md for the real OTel SDK setup.")
