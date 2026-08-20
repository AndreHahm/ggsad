# GG-SAD verständlich erklärt

## Ein schlankes Entwicklungsmodell mit klaren Zielen und sicheren Übergängen

**GG-SAD** steht für **Goal-Gated Spec-Anchored Development**.

Die Grundidee ist einfach:

> Eine Änderung beginnt mit einem klaren Ziel, wird durch eine verständliche Spezifikation geführt und darf nur dann in die nächste Phase wechseln, wenn definierte Bedingungen erfüllt sind.

Dabei bleibt das Modell bewusst schlank. Es benötigt weder Epics noch vollständige Sprints, Story Points, Rollenzeremonien oder einen großen Agentenapparat.

---

## Warum GG-SAD?

Viele Spec-driven-Development-Frameworks bringen wertvolle Ideen mit. In der Praxis erzeugen sie jedoch oft zu viele Dokumente, zu viele Prozessschritte oder zu starre Workflows.

GG-SAD konzentriert sich auf das Wesentliche:

- **Was wollen wir erreichen?**
- **Was genau soll sich ändern?**
- **Wann dürfen wir beginnen?**
- **Wann sind wir wirklich fertig?**
- **Wann müssen wir warten?**
- **Wann müssen wir abbrechen?**
- **Welche Nachweise zeigen, dass das Ergebnis stimmt?**

So bleibt der Prozess kontrolliert, ohne schwerfällig zu werden.

GG-SAD kann **stand-alone** oder als **Governance-Schicht um eine andere Methode oder ein Tool** eingesetzt werden. Beispielsweise kann ein Team GSD für Context Engineering, OpenSpec für schlanke Spezifikationen, Spec Kit für konfigurierbare Workflows, BMAD für Produkt- und Architekturarbeit oder Kiro und Hermes als Ausführungsumgebungen verwenden, während GG-SAD Gates, Zustand, Evidence und Abschluss steuert.

---

## Die vier Bausteine

GG-SAD ruht auf vier Bausteinen:

### 1. Goal

Jede Änderung besitzt ein klares Ziel.

Ein gutes Ziel beschreibt nicht nur eine Aufgabe wie *„Login-Code ändern“*, sondern den gewünschten Zustand:

> Benutzerkonten sollen nach mehreren fehlgeschlagenen Anmeldeversuchen automatisch geschützt werden.

Dazu kommen Erfolgssignale:

- Ein gesperrtes Konto weist weitere Anmeldeversuche zurück.
- Eine erfolgreiche Anmeldung setzt den Fehlerzähler zurück.
- Bestehende Clients bleiben kompatibel.

Das Ziel hilft bei Entscheidungen. Wenn mehrere Lösungen möglich sind, gewinnt diejenige, die das Ziel am besten erfüllt und gleichzeitig Architektur, Regeln und Scope respektiert.

### 2. Specification

Die Spezifikation beschreibt, **was** erreicht werden soll.

Sie enthält typischerweise:

- Ziel und Nutzen,
- Scope und Ausschlüsse,
- Requirements,
- konkrete Beispiele,
- technische oder organisatorische Constraints,
- Verifikationskriterien,
- offene Fragen.

Sie soll klar genug sein, damit ein Mensch oder KI-Agent daraus arbeiten kann. Sie soll aber nicht jeden Implementierungsdetail vorwegnehmen.

### 3. Gates

Gates steuern, wann der Workflow weitergehen darf.

GG-SAD verwendet vier Arten:

| Gate | Frage |
|---|---|
| **Definition of Ready** | Darf die nächste Phase beginnen? |
| **Definition of Done** | Ist die aktuelle Phase abgeschlossen? |
| **Definition of Wait** | Müssen wir kontrolliert pausieren? |
| **Definition of Fail** | Müssen wir den Flow beenden? |

### 4. Evidence

Evidence ist der überprüfbare Nachweis, dass eine Anforderung erfüllt wurde.

Beispiele:

- bestandene Tests,
- Build-Ausgaben,
- Security-Scans,
- Review-Freigaben,
- Deploy-Nachweise,
- Messwerte,
- Verweise auf Commits oder Pull Requests.

Ohne Evidence ist *„fertig“* nur eine Behauptung.

---

## Die projektweiten Dokumente

GG-SAD verwendet wenige, klar getrennte Dokumente.

```text
docs/
├── constitution.md
├── project-brief.md
├── architecture.md
├── roadmap.md
├── definitions/
│   ├── definition-of-ready.md
│   ├── definition-of-done.md
│   ├── definition-of-wait.md
│   └── definition-of-fail.md
└── adr/
```

### `constitution.md`

Die Constitution enthält die nicht verhandelbaren Regeln des Projekts.

Dazu können gehören:

- Sicherheitsgrundsätze,
- Qualitätsanforderungen,
- erlaubte oder verbotene Technologien,
- Regeln für Breaking Changes,
- Mindestanforderungen an Tests,
- Budget- oder Ressourcenlimits,
- Grenzen für autonome Agenten.

Die Constitution ändert sich selten.

### `project-brief.md`

Der Project Brief erklärt, was das Projekt ist, warum es existiert, wem es dient und welche Rahmenbedingungen gelten.

Er dokumentiert Problem und Opportunity, Nutzer und Stakeholder, gewünschte Outcomes, Projekttyp, Scope, Non-Goals, Constraints, Compliance-Profil und die Betriebsart von GG-SAD.

### `architecture.md`

Dieses Dokument zeigt, wie das System heute aufgebaut ist.

Es beantwortet Fragen wie:

- Welche Komponenten gibt es?
- Wer ist wofür verantwortlich?
- Welche Abhängigkeiten bestehen?
- Wie fließen Daten durch das System?
- Wo liegen technische Grenzen?
- Wie wird das System betrieben und deployed?

`architecture.md` ist das aktuelle Gesamtbild. Einzelne Architekturentscheidungen gehören dagegen in ADRs.

### `roadmap.md`

Die Roadmap beschreibt die Entwicklungsrichtung, ohne daraus ein komplettes Projektmanagementsystem zu machen.

Ein einfaches Format reicht:

```markdown
## Now

- Authentication Hardening

## Next

- Session Management

## Later

- External Identity Providers

## Open

- Multi-region Deployment
```

Damit ersetzt die Roadmap in vielen Fällen ein Epic-Modell.

### ADRs

Architecture Decision Records dokumentieren wichtige, langlebige Entscheidungen.

Beispiel:

- Warum wurde PostgreSQL gewählt?
- Warum bleibt die Kommunikation synchron?
- Warum ist eine bestimmte Abhängigkeit verboten?

Ein neues Requirement darf ein bestehendes ADR nicht stillschweigend überschreiben. Bei einem Konflikt wird der Flow angehalten und eine Entscheidung eingeholt.

---

## GG-SAD an das Projekt anpassen

Ein Pre-PMF-MVP und eine regulierte Enterprise-Plattform müssen nicht denselben Workflow verwenden.

| Profil | Typischer Kontext | Auswirkung |
|---|---|---|
| **Lean** | MVP, Prototyp, Solo-Entwicklung | kurze Inline-Specs, wenige Artefakte, überwiegend automatische Checks |
| **Standard** | normale Produktentwicklung | separate Specs, definierte Qualitätsgates, pragmatisches Peer Review |
| **Governed** | Enterprise oder High Impact | starke Traceability, Architektur- und Security-Reviews, explizite Freigaben |
| **Regulated** | auditierte oder sicherheitskritische Systeme | Funktionstrennung, aufbewahrte Evidence, formale Freigaben, Compliance-Mappings |

Der Kern bleibt in allen Profilen bestehen: Goal, Spec Anchor, Gates, passende Evidence, kontrolliertes Wait/Fail und ein nachvollziehbarer Abschluss.

## Stand-alone- und Kombinationsbetrieb

Im Stand-alone-Betrieb liefert GG-SAD den vollständigen führenden Flow. Im Kombinationsbetrieb kann ein anderes Framework Planung, Umsetzung, Context Management, Tests oder Agentenausführung bereitstellen. GG-SAD entscheidet weiterhin über führende Fakten, Gates, Wait/Fail, Evidence und Abschluss.

## Die Dokumente pro Änderung

Für eine normale Änderung reicht oft folgende Struktur:

```text
specs/042-user-lockout/
├── spec.md
├── plan.md
└── evidence.md
```

Optional kommt eine Taskliste hinzu:

```text
tasks.md
```

### `spec.md`

Die Spezifikation ist das zentrale Dokument der Änderung.

### `plan.md`

Der Plan beschreibt den technischen Ansatz. Er ist nur nötig, wenn die Lösung nicht offensichtlich ist oder relevante Risiken bestehen.

### `tasks.md`

Die Taskliste ist eine Ausführungshilfe. Sie ist kein Sprint-Backlog und nicht die führende Wahrheit.

### `evidence.md`

Hier werden die Nachweise gesammelt, die zeigen, dass Requirements und Qualitätsgates erfüllt sind.

Bei kleinen Änderungen können Plan, Tasks und Evidence direkt in `spec.md` stehen.

---

## Der typische Ablauf

Ein vollständiger Workflow sieht so aus:

```text
INTAKE
  ↓
SPECIFY
  ↓
PLAN
  ↓
BUILD
  ↓
VERIFY
  ↓
RELEASE
  ↓
CLOSED
```

Nicht jede Änderung benötigt alle Phasen.

### Kleine Änderung

```text
SPECIFY → BUILD → VERIFY → CLOSED
```

### Normale Änderung

```text
SPECIFY → PLAN → BUILD → VERIFY → CLOSED
```

### Release-relevante Änderung

```text
SPECIFY → PLAN → BUILD → VERIFY → RELEASE → CLOSED
```

### Exploration

```text
EXPLORE → DECIDE → SPECIFY
```

Wichtig: Eine Exploration darf nicht heimlich zur produktiven Implementierung werden.

---

## Definition of Ready

Die **Definition of Ready** beantwortet:

> Haben wir genug Klarheit und Freigabe, um die nächste Phase zu starten?

### Ready-to-Spec

Eine Spezifikation kann beginnen, wenn:

- Ziel oder Problem verständlich sind,
- der erwartete Nutzen bekannt ist,
- ein Ansprechpartner oder Entscheider feststeht,
- wichtige Constraints bekannt sind,
- keine offensichtliche Kollision mit Projektregeln besteht.

### Ready-to-Plan

Die Planung kann beginnen, wenn:

- Scope und Non-Goals klar sind,
- Requirements verständlich sind,
- Akzeptanzbedingungen vorliegen,
- relevante ADRs geprüft wurden,
- offene Fragen geklärt oder bewusst akzeptiert wurden.

### Ready-to-Build

Die Umsetzung kann beginnen, wenn:

- die Spezifikation freigegeben ist,
- der technische Ansatz ausreichend klar ist,
- Risiken bewertet wurden,
- Abhängigkeiten verfügbar sind,
- Tests und Verifikationskriterien definiert sind.

### Ready-to-Release

Ein Release kann beginnen, wenn:

- Build und Tests erfolgreich sind,
- Sicherheits- und Qualitätsgates bestanden wurden,
- Migration und Rollback geklärt sind,
- notwendige Genehmigungen vorliegen.

---

## Definition of Done

Die **Definition of Done** beantwortet:

> Woran erkennen wir, dass eine Phase wirklich abgeschlossen ist?

### Spec-Done

Eine Spezifikation ist fertig, wenn:

- Ziel und Nutzen klar beschrieben sind,
- Scope und Ausschlüsse feststehen,
- Requirements prüfbar sind,
- Beispiele oder Akzeptanzbedingungen existieren,
- offene Fragen gelöst oder ausdrücklich akzeptiert wurden,
- Konflikte mit ADRs geklärt sind,
- die Spezifikation freigegeben wurde.

### Plan-Done

Ein Plan ist fertig, wenn:

- der technische Ansatz beschrieben ist,
- betroffene Komponenten bekannt sind,
- Architektur-, Daten- und API-Auswirkungen bewertet wurden,
- Teststrategie und Rollback geklärt sind,
- Risiken und Entscheidungen dokumentiert wurden.

### Build-Done

Die Umsetzung ist fertig, wenn:

- alle genehmigten Änderungen umgesetzt sind,
- kein unbeabsichtigter Scope hinzugekommen ist,
- Tests ergänzt wurden,
- lokale Qualitätsgates bestanden sind,
- Dokumentation aktualisiert wurde,
- keine unerklärten Abweichungen zur Spezifikation bestehen.

### Verify-Done

Die Prüfung ist fertig, wenn:

- alle Akzeptanzbedingungen getestet wurden,
- automatisierte Tests bestanden sind,
- Fehler- und Negativfälle geprüft wurden,
- Regressionstests erfolgreich sind,
- Evidence vollständig ist.

### Release-Done

Ein Release ist fertig, wenn:

- Deployment oder Veröffentlichung erfolgreich war,
- Smoke Tests bestanden wurden,
- Version und Release Notes dokumentiert sind,
- keine kritischen Betriebsprobleme sichtbar sind,
- Roadmap und Status aktualisiert wurden.

---

## Definition of Wait

Die **Definition of Wait** ist eine besondere Stärke von GG-SAD.

Sie trennt zwei Situationen, die häufig verwechselt werden:

- *Wir können gerade nicht weiterarbeiten.*
- *Die Änderung ist gescheitert.*

Ein Wartezustand ist kein Fehler. Er bedeutet, dass eine konkrete Voraussetzung fehlt.

Typische Gründe:

- Antwort des Benutzers fehlt,
- Architekturentscheidung steht aus,
- Review oder Genehmigung fehlt,
- externes System ist nicht verfügbar,
- anderer Prozess muss zuerst abgeschlossen werden,
- Breaking Change braucht Zustimmung.

Ein guter Wait-Eintrag beschreibt:

```yaml
status: waiting
reason: architecture-decision-required
waiting_for: requestor
resume_when: ADR-approved
safe_state: no-destructive-change
next_action: update-plan
```

Ein KI-Agent muss in diesem Zustand stoppen, den sicheren Zustand erhalten und eine präzise Frage stellen. Er darf fehlende Informationen nicht durch eigene Annahmen ersetzen.

---

## Definition of Fail

Die **Definition of Fail** beschreibt harte Abbruchbedingungen.

Typische Beispiele:

- kritischer Datenverlust,
- Repository-Korruption,
- schwere Sicherheitsverletzung,
- nicht genehmigter Breaking Change,
- Verstoß gegen Constitution oder ADR,
- Arbeit außerhalb des genehmigten Scopes,
- Überschreitung einer harten Budgetgrenze,
- nicht wiederherstellbare Migration,
- dauerhaft unerfüllbare Akzeptanzbedingungen.

Eine Fail-Regel sollte immer festlegen:

1. Was löst sie aus?
2. Welche Aktionen müssen sofort stoppen?
3. Welche Sicherungsmaßnahmen sind noch erlaubt?
4. Welcher Endstatus gilt?
5. Was muss dokumentiert werden?

So weiß auch ein autonom arbeitender Agent genau, wann er nicht weiter improvisieren darf.

---

## Die Reihenfolge der Gate-Prüfung

GG-SAD prüft Gates immer in dieser Reihenfolge:

1. **DoF** — Müssen wir abbrechen?
2. **DoW** — Müssen wir warten?
3. **DoD** — Ist die Phase abgeschlossen?
4. **DoR** — Darf die nächste Phase starten?

Diese Reihenfolge verhindert problematische Abkürzungen.

Beispiel:

Die Spezifikation kann vollständig sein, aber die nächste Phase darf trotzdem nicht starten, weil eine Architekturfreigabe fehlt.

```text
Spec-Done = erfüllt
Ready-to-Plan = nicht erfüllt
Ergebnis = warten
```

---

## Was passiert bei einem ADR-Konflikt?

Angenommen, eine neue Anforderung verlangt eine Änderung, die einem bestehenden ADR widerspricht.

Dann gilt:

1. Der Konflikt wird in der Spezifikation dokumentiert.
2. Planung oder Umsetzung werden gestoppt.
3. Das Requirement geht an den Requestor zurück.
4. Eine Entscheidung wird eingeholt.
5. Erst danach geht der Flow weiter.

Das ADR wird nicht beiläufig geändert. Eine Änderung benötigt einen eigenen genehmigten Entscheidungsflow.

---

## Wie viel Dokumentation braucht eine Änderung?

GG-SAD verwendet drei Größenklassen.

### S — Patch

Für kleine, klare Änderungen.

Benötigt meist nur:

- Ziel,
- Scope,
- Akzeptanzbedingungen,
- Verifikation.

Das kann direkt in einem Issue stehen.

### M — Change

Für normale eigenständige Änderungen.

Benötigt:

- `spec.md`

Je nach Risiko zusätzlich:

- `plan.md`
- `tasks.md`
- `evidence.md`

### L — Initiative

Für größere Vorhaben mit mehreren unabhängigen Changes.

Die Initiative wird in mehrere Change-Spezifikationen zerlegt. Eine kurze Roadmap oder Abhängigkeitsübersicht reicht. Ein Epic ist optional, nicht vorgeschrieben.

---

## Minimalbeispiel einer Spezifikation

```markdown
# Change: User Lockout

## Goal

Konten nach mehreren fehlgeschlagenen Anmeldeversuchen schützen.

## Success Signals

- Nach fünf Fehlversuchen wird das Konto gesperrt.
- Eine erfolgreiche Anmeldung setzt den Fehlerzähler zurück.
- Bestehende Clients bleiben kompatibel.

## Non-Goals

- Administrator-Oberfläche zum Entsperren.
- E-Mail-Benachrichtigungen.
- IP-basiertes Rate Limiting.

## Requirements

### R1 — Failed Attempts

Das System zählt aufeinanderfolgende fehlgeschlagene Anmeldeversuche pro Konto.

### R2 — Lockout

Nach fünf Fehlversuchen wird das Konto gesperrt.

## Acceptance Example

Given ein aktives Konto mit vier Fehlversuchen  
When ein weiteres falsches Passwort eingegeben wird  
Then wird das Konto gesperrt  
And die Anmeldung wird abgelehnt

## Constraints

- Bestehende Authentication-ADRs haben Vorrang.
- Keine neue externe Abhängigkeit.
- Das vorhandene API-Format bleibt kompatibel.

## Verification

- Unit Tests für R1 und R2.
- Integrationstest für den fünften Fehlversuch.
- Bestehende Authentication-Tests bleiben erfolgreich.
```

---

## Evidence statt zusätzlicher Statusberichte

GG-SAD vermeidet separate Completion-, Review- und Statusdokumente, wenn sie keinen zusätzlichen Nutzen bringen.

Ein kompaktes Evidence-Dokument reicht oft:

```markdown
# Verification Evidence

| Requirement | Evidence | Result |
|---|---|---|
| R1 | `AccountLockoutTests.cs` | Pass |
| R2 | `AuthenticationIntegrationTests.cs` | Pass |

## Quality Gates

- Build: Pass
- Unit tests: Pass
- Integration tests: Pass
- Static analysis: Pass
- Security checks: Pass

## Deviations

None.
```

---

## Zukünftiger GG-SAD Memory

Eine spätere GG-SAD-Implementierung erhält einen Project Memory für Decisions, die keine Architekturentscheidungen sind, Learnings, Failures, Definitions und Glossarbegriffe sowie externe Quellen mit Provenance und Trust-Informationen.

Architekturentscheidungen bleiben ADRs. Memory darf führende Dokumente niemals versteckt überschreiben.

## GG-SAD und KI-Agenten

GG-SAD eignet sich besonders für KI-Agenten, weil es klare Grenzen schafft.

Ein Agent kann jederzeit beantworten:

- Welches Ziel verfolge ich?
- In welcher Phase befinde ich mich?
- Was darf ich ändern?
- Welche Regeln haben Vorrang?
- Wann bin ich fertig?
- Wann muss ich warten?
- Wann muss ich abbrechen?
- Welche Evidence fehlt noch?

Ein Agent darf jedoch nicht:

- Anforderungen erfinden,
- fehlende Freigaben unterstellen,
- ADRs stillschweigend überschreiben,
- Breaking Changes ungefragt umsetzen,
- außerhalb des Scopes arbeiten,
- fehlende Evidence ignorieren,
- Wartezustände durch Spekulation umgehen.

---

## Example-Driven Specification und Pair Review

### Konkrete Beispiele als Standard

GG-SAD verwendet Example-Driven Specification als Standard. Jedes verhaltensbezogene Requirement erhält mindestens ein konkretes Akzeptanzbeispiel oder eine begründete alternative Akzeptanzbedingung. Die Notation bleibt frei: Given/When/Then, Tabellen, API-Beispiele oder Zustandsübergänge sind gleichermaßen zulässig.

Beispiele verbinden Requirements, Implementierung, Tests und Evidence. Bei höherem Risiko werden zusätzlich Negativ-, Fehler- und Grenzfälle verlangt.

### Pair Review

Pair Review trennt Erstellung und Prüfung:

```text
Requestor erstellt oder ändert ein Arbeitsergebnis
→ Reviewer prüft, testet, verifiziert oder validiert
→ Reviewer liefert Findings
→ Requestor entscheidet und korrigiert
→ Reviewer prüft Blocking-Findings nach
```

Requestor und Reviewer müssen unterschiedliche Teilnehmer sein. Zulässig sind:

- Human → Human
- Human → Agent
- Agent → Human
- Agent → Agent
- Human oder Agent → externer Review-Dienst

Pair Review ist nicht immer verpflichtend. Compliance-Profil, Projektumfang, Change-Klasse, Risiko und Projektregeln bestimmen, ob und wie tief es eingesetzt wird. Lean- oder kleine Low-Risk-Changes können ohne Pair Review auskommen; Governed- und Regulated-Flows können es für relevante Änderungen verlangen.

Der Reviewer ändert das geprüfte Arbeitsergebnis nicht stillschweigend. Er gibt Findings an den Requestor zurück. Pair Review ersetzt keine erforderliche menschliche Freigabe.

## Die wichtigste Regel

GG-SAD ist nicht dokumentgetrieben, sondern zielgetrieben.

Die führende Kette lautet:

```text
Goal
→ Spec
→ Gates
→ Implementation
→ Verification
→ Evidence
```

Projektweit gilt:

```text
Constitution
→ ADRs
→ Project Brief
→ Architecture
→ Scoped Decisions
→ Change Spec
→ Plan
→ Tasks
→ Code and Tests
→ Evidence
```

Tasks sind Hilfsmittel. Die Spezifikation ist der Anker. Das Ziel gibt die Richtung vor. Die Gates kontrollieren den Weg. Evidence zeigt, ob das Ergebnis stimmt.

---

## Zusammenfassung

GG-SAD bietet einen Mittelweg zwischen informeller Entwicklung und schwergewichtigen SDD-Frameworks.

Es ist:

- schlank und compliance-adaptierbar,
- zielorientiert,
- risikobasiert,
- spezifikationsgeführt,
- agententauglich,
- überprüfbar,
- ohne verpflichtende Epics oder Sprints nutzbar,
- stand-alone oder mit anderen Methoden und Tools kombinierbar.

Der Kern lässt sich in einem Satz ausdrücken:

> Eine Änderung darf nur dann beginnen, weitergehen oder abgeschlossen werden, wenn Ziel, Spezifikation, Gates und Evidence dies nachvollziehbar erlauben.
