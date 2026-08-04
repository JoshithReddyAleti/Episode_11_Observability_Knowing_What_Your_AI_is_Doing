# 🔐 Security & Audit — Observability That Protects and Proves

> *Observability isn't just for debugging. It's your evidence trail, your compliance record, and your first line of attack detection.*

---

## Audit Logging (`audit_logging.py`)

Audit logs are a special class of logs: immutable, comprehensive records of *who did what, when, and why*. Unlike debug logs (which you sample and expire), audit logs are complete and retained long-term (often 7 years for compliance).

**Capture for every consequential action:** the actor (user/service/agent), the action, the target, the timestamp, the result, and the authorization used. For AI: every high-stakes agent action, every data access, every model decision with real-world consequences.

Audit logs must be tamper-evident — write-once, access-controlled, ideally to a separate system from application logs.

---

## PII Detection in Logs (`pii_detection_in_logs.py`)

**The compliance landmine specific to AI.** Prompts and responses are full of PII, and it's easy to accidentally log it. This goes beyond redaction (structured_logging) — it's *detecting* PII that slipped through.

**Practice:** scan logs (at write time and via periodic audits) for PII patterns and entities. Alert when PII appears in logs where it shouldn't. Catching a PII leak in your logs before an auditor (or attacker) does is the difference between a fix and a breach notification.

---

## Access Control Logs (`access_control_logs.py`)

Record every access decision: who requested access to what, whether it was granted or denied, and why. Failed access attempts are especially important — a spike in denials can indicate an attack or a misconfiguration.

For AI systems, this includes which users/tenants accessed which data, which agents were granted which tool permissions, and every authorization check.

---

## Prompt Injection Detection (`prompt_injection_detection.py`)

Observe for the LLM-specific attack (Episodes 8, 10). Prompt injection attempts leave signatures in the input — instructions to ignore the system prompt, attempts to extract it, unusual formatting, known jailbreak patterns.

**Practice:** run detection on inputs, log flagged attempts as security events, track the injection-attempt rate as a metric, and alert on spikes. Observability turns prompt injection from an invisible threat into a monitored, measurable one. A rising injection rate is an active-attack signal.

---

## Compliance Logging (`compliance_logging.py`)

Regulations (GDPR, HIPAA, EU AI Act — Episode 8) require specific records: what data was processed, on what legal basis, with what consent, and the ability to prove it. Compliance logging captures exactly what auditors will ask for.

**Practice:** log data-processing events with their legal basis, consent records, and data-subject requests (access, deletion). Design these logs around your specific regulatory obligations — they're what you'll produce during an audit or investigation.

---

## Data Residency (`data_residency.md`)

Where your observability data physically lives is itself a compliance concern. Logs and traces contain user data; if that data must stay in the EU (GDPR) or a specific region, your observability backend must respect that too.

Covers: choosing observability tools/regions that meet residency requirements, why self-hosted tools (Langfuse, Grafana) help here, and avoiding accidental cross-border data transfer through a SaaS observability vendor.

---

## Log Retention Policies (`log_retention_policies.md`)

Different logs, different lifespans:
- **Debug logs:** days (high volume, low long-term value)
- **Application logs:** 30–90 days
- **Audit logs:** years (compliance-driven)
- **PII-containing logs:** minimized retention (delete ASAP, keep only what's required)

Retention is a balance: keep enough to debug and comply, delete enough to reduce risk and cost. Automated, policy-driven deletion is essential — manual retention doesn't scale and fails audits.

---

## Forensic Analysis (`forensic_analysis.py`)

When a security incident happens, observability data is your evidence. Forensic analysis reconstructs exactly what occurred: which requests, from whom, accessing what, with what result.

**Practice:** the same correlation that powers debugging (request IDs, traces, audit logs) powers forensics. Being able to answer "show me everything this user/tenant/agent did in this window" precisely is what turns a scary incident into a bounded, understood one. This is why comprehensive, correlated, retained logs matter.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `audit_logging.py` | Immutable who-did-what records |
| `pii_detection_in_logs.py` | Catching PII leaks in logs |
| `access_control_logs.py` | Recording every access decision |
| `prompt_injection_detection.py` | Observing the LLM-specific attack |
| `compliance_logging.py` | What auditors will ask for |
| `data_residency.md` | Where observability data lives |
| `log_retention_policies.md` | How long to keep what |
| `forensic_analysis.py` | Observability as evidence |

---

*Previous: [← Observability Tools](../observability_tools/README.md) · Next: [Data Pipeline Observability →](../data_pipeline_observability/README.md)*

*Back to [main README](../../README.md)*
