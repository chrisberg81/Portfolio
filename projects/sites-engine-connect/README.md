# Sites Engine + Connect

Two shared layers that let one platform power many branded sites.

- **Sites Engine:** host to tenant routing, typed client, themes and layout archetypes, section components with variants, Shopify cart bridge.
- **Connect:** directory layer for spots, schools and shops: a globe-based explorer, tabs, region filters and detail cards. Each site supplies only style tokens.

```mermaid
flowchart TB
  A[Site A] & B[Site B] & C[Site C] --> ENG[Sites Engine]
  A & B & C --> CON[Connect directory]
  ENG & CON --> SDK[Typed API client] --> API[AllyOS API]
```
Shipped as TypeScript source packages consumed by monorepos.

## Size
Sites Engine ~1.8k LOC (63 files); Connect ~9.2k LOC (66 files).
