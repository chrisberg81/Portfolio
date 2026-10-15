# SoftWing

Parametric design software for soft wings (kites and parawings): define the shape, get a solved, buildable pattern.

## How it is built

[Interactive diagram](../../assets/softwing/architecture.html) (explore, trace paths, light/dark; open after cloning or via Pages).
```mermaid
flowchart LR
  P[Parameters] --> CORE[pattern-core<br/>pure .NET geometry and solver]
  CORE --> RH[Rhino plugin<br/>3D surfaces, panels]
  CORE --> WEB[Standalone web editor<br/>2D design, tailoring view]
  WEB --> OUT[Panel patterns for sewing]
```
- **Host-free core:** geometry and solver compile with no CAD dependency, so the same math drives the Rhino plugin and the browser editor.
- **Test discipline:** offline test consoles plus in-Rhino harnesses.
- Runs as an always-on local app.

## Size
~22k lines of C# in total; solver core ~1.3k, Rhino plugin ~5.9k, web editor ~3.5k LOC.
