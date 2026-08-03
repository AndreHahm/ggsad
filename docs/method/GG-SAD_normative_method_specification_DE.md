# GG-SAD — Normative Methodenbeschreibung

**Version:** 1.2  
**Status:** Normative Baseline  
**Zielgruppe:** KI-Agenten, Workflow-Engines, Automatisierungen und technische Projektverantwortliche

---

## 1. Zweck

**Goal-Gated Spec-Anchored Development (GG-SAD)** ist ein schlankes, zielorientiertes Entwicklungsmodell für spezifikationsgesteuerte Softwareentwicklung.

GG-SAD definiert:

- eine verbindliche Dokumenthierarchie,
- einen phasenbasierten Entwicklungsfluss,
- explizite Eintritts-, Abschluss-, Warte- und Abbruchbedingungen,
- minimale Artefakte pro Änderung,
- Regeln für Abweichungen, Entscheidungen und Nachweise,
- einen kontrollierten Einsatz von KI-Agenten.

GG-SAD verwendet keine verpflichtenden Epics, Sprints, Story Points, Rollenmodelle oder Zeremonien. Die führende Arbeitseinheit ist eine **zielgebundene Änderung**.

GG-SAD MUSS in zwei Betriebsarten einsetzbar sein:

- **Stand-alone-Betrieb**, in dem GG-SAD die führende Methode und den Ausführungsflow bereitstellt;
- **Kombinationsbetrieb**, in dem GG-SAD Ziele, Gates, Evidence, Zustand und Prioritäten steuert, während eine andere Methode, ein Framework, Tool oder eine Agentenplattform Planung, Ausführung, Review, Context Engineering oder Automatisierung bereitstellt.

---

## 2. Normative Begriffe

Die Schlüsselwörter **MUSS**, **DARF NICHT**, **SOLL**, **SOLL NICHT** und **KANN** sind normativ zu verstehen.

- **MUSS / DARF NICHT:** verbindliche Anforderung.
- **SOLL / SOLL NICHT:** starke Empfehlung; Abweichungen sind zu begründen.
- **KANN:** optionale Fähigkeit oder Vorgehensweise.

---

## 3. Grundprinzipien

### 3.1 Goal First

Jede Änderung MUSS ein explizites Ziel besitzen.

Das Ziel MUSS beschreiben:

- welches Problem gelöst wird,
- welcher gewünschte Zustand erreicht werden soll,
- woran die Zielerreichung erkannt wird,
- welche Ergebnisse ausdrücklich nicht Teil der Änderung sind.

### 3.2 Spec Anchoring

Die Spezifikation ist der verbindliche Anker einer Änderung.

Code, Tests, Pläne und Nachweise MÜSSEN mit der freigegebenen Spezifikation übereinstimmen. Die Spezifikation ersetzt nicht Architekturentscheidungen oder projektweite Regeln.

### 3.3 Gate-Controlled Flow

Jeder Phasenübergang MUSS durch definierte Gates kontrolliert werden:

- **Definition of Ready (DoR):** Darf die nächste Phase beginnen?
- **Definition of Done (DoD):** Ist die aktuelle Phase erfolgreich abgeschlossen?
- **Definition of Wait (DoW):** Muss der Ablauf kontrolliert pausieren?
- **Definition of Fail (DoF):** Muss der Ablauf erfolglos beendet werden?

### 3.4 Evidence over Assertion

Ein Status DARF NICHT ausschließlich durch Behauptung gesetzt werden. Für relevante Abschlusskriterien MUSS überprüfbare Evidence vorliegen.

### 3.5 One Fact, One Home

Jede Information SOLL genau einen autoritativen Ablageort besitzen.

Wiederholungen zwischen Dokumenten SOLLEN vermieden werden. Referenzen sind Kopien vorzuziehen.

### 3.6 Risk-Based Scaling

Artefakte und Prozessschritte MÜSSEN nach Risiko, Unsicherheit, Tragweite und dem gewählten Compliance-Profil skaliert werden, nicht allein nach geschätztem Arbeitsumfang.

### 3.7 Anpassbarer, aber unveränderlicher Kern

GG-SAD-Workflows MÜSSEN anpassbar sein. Tailoring KANN aktivierte Phasen, erforderliche Artefakte, Review-Tiefe, Genehmigungsregeln, Evidence-Tiefe, Berechtigungen und Automatisierung verändern.

Tailoring DARF den unveränderlichen Kern NICHT entfernen:

- ein explizites Ziel,
- einen zur Change-Größe passenden Spezifikationsanker,
- Gate-Prüfung,
- zum gewählten Profil passende Evidence,
- kontrolliertes Wait- und Fail-Verhalten,
- einen nachvollziehbaren Abschlussstatus.

### 3.8 Stand-alone- und Kombinationsbetrieb

GG-SAD MUSS unabhängig von einem bestimmten Planungsframework, Coding-Agenten, einer IDE, einem Issue-Tracker oder einer Delivery-Plattform bleiben.

Im Kombinationsbetrieb gilt:

- GG-SAD besitzt die Governance-Semantik, den Zustand, die Gates, Prioritäten und den Abschluss;
- die integrierte Methode oder das Tool KANN untergeordnete Planungs- oder Ausführungsartefakte besitzen;
- zugeordnete externe Artefakte MÜSSEN ihre GG-SAD-Rolle ausweisen;
- externe Workflows DÜRFEN GG-SAD-Gates nicht umgehen oder das aktive Compliance-Profil abschwächen;
- Konflikte MÜSSEN nach der GG-SAD-Dokumenthierarchie gelöst werden.

---

### 3.9 Example-Driven Specification

Jedes verhaltensbezogene Requirement MUSS mindestens ein konkretes Akzeptanzbeispiel besitzen.

Ein Akzeptanzbeispiel SOLL enthalten:

- den relevanten Ausgangszustand,
- die auslösende Aktion oder das Ereignis,
- das erwartete beobachtbare Ergebnis,
- risikogerechte Negativ-, Fehler- oder Grenzfälle.

Given/When/Then KANN verwendet werden; GG-SAD schreibt keine bestimmte Notation vor. Ein Requirement KANN nur dann ohne Beispiel auskommen, wenn ein Beispiel die Klarheit nicht erhöhen würde. Dann MUSS eine alternative prüfbare Akzeptanzbedingung einschließlich Begründung dokumentiert werden.

Akzeptanzbeispiele MÜSSEN auf Requirements und Verifikations-Evidence zurückführbar sein.

### 3.10 Pair Review

GG-SAD unterstützt **Pair Review** als kontrolliertes Zusammenarbeitsmodell zwischen zwei unterschiedlichen Teilnehmern:

- der **Requestor** erzeugt oder ändert ein gesteuertes Arbeitsergebnis;
- der **Reviewer** prüft, verifiziert, testet, validiert oder bewertet dieses Arbeitsergebnis unabhängig und gibt nachvollziehbare Findings an den Requestor zurück.

Requestor und Reviewer MÜSSEN innerhalb desselben Review-Zyklus unterschiedliche Teilnehmer sein. Zulässig sind Human–Human, Human–Agent, Agent–Human, Agent–Agent sowie Human oder Agent mit einem externen Review-Dienst.

Pair Review ist standardmäßig OPTIONAL. Einsatz und Tiefe MÜSSEN aus aktivem Compliance-Profil, Projektumfang, Change-Klasse, Risiko, Auswirkung und projektspezifischer Policy abgeleitet werden. Ein Projekt KANN Pair Review für bestimmte Phasen, Artefakte oder Risikokategorien verpflichtend machen.

Der Reviewer DARF das gesteuerte Arbeitsergebnis des Requestors im Rahmen des Reviews NICHT stillschweigend ändern. Findings MÜSSEN zur Entscheidung an den Requestor zurückgegeben werden. Eine separat zugewiesene Änderungsaktion KANN den Reviewer in einem späteren Korrekturzyklus zum Requestor machen.

Pair Review DARF eine erforderliche menschliche Genehmigung NICHT ersetzen. Bei Funktionstrennung KANN das Projekt Requestor, Reviewer und Approver als drei unterschiedliche Teilnehmer verlangen.

## 4. Dokumenthierarchie

### 4.1 Verbindliche Reihenfolge

Bei Konflikten gilt folgende Priorität:

1. `docs/constitution.md`
2. bestehende akzeptierte ADRs unter `docs/adr/`
3. `docs/project-brief.md`
4. `docs/architecture.md`
5. genehmigte fachliche oder operative Decision Records, sofern sie kein ADR ersetzen
6. genehmigte Änderungsspezifikation `spec.md`
7. genehmigter Implementierungsplan `plan.md`
8. lokale Taskliste `tasks.md`
9. Implementierung und Tests
10. Evidence, ergänzende Notizen und temporäre Arbeitsartefakte

Eine Änderung DARF höherrangige Dokumente nicht stillschweigend überschreiben.

### 4.2 Projektweite Dokumente

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
    └── ADR-<nummer>-<titel>.md
```

#### `constitution.md`

Enthält nicht verhandelbare projektweite Regeln, insbesondere:

- Qualitätsprinzipien,
- Sicherheitsgrundsätze,
- Architekturprinzipien,
- Genehmigungsregeln,
- verbotene Aktionen und Abhängigkeiten,
- Regeln für Breaking Changes,
- Ressourcen- und Budgetgrenzen,
- Mindestanforderungen an Tests und Evidence.

#### `project-brief.md`

Beschreibt den stabilen Produkt- und Projektkontext:

- Problem und Opportunity,
- Zielnutzer und Stakeholder,
- gewünschte Outcomes und Erfolgssignale,
- Projekttyp und Lifecycle-Kontext,
- Scope-Grenzen und Non-Goals,
- Business-, Delivery-, Budget- und Zeit-Constraints,
- gewähltes Compliance-Profil,
- im Kombinationsbetrieb verwendete Methoden, Frameworks, Tools oder Agenten.

Der Project Brief DARF keine Architekturentscheidungen enthalten, die in ADRs gehören.

#### `architecture.md`

Beschreibt den aktuellen strukturellen Zustand des Systems:

- Systemkontext,
- Komponenten und Verantwortlichkeiten,
- Modul- und Integrationsgrenzen,
- Datenflüsse,
- Deployment- und Betriebsstruktur,
- bekannte technische Einschränkungen,
- Verweise auf relevante ADRs.

#### `roadmap.md`

Beschreibt die beabsichtigte Entwicklungsrichtung. Die Roadmap SOLL schlank bleiben und KANN die Bereiche `Now`, `Next`, `Later` und `Open` verwenden.

Die Roadmap ist kein Sprint- oder Epic-Backlog.

#### `docs/definitions/`

Enthält die projektweiten Standard-Gates. Lokale Spezifikationen DÜRFEN diese Regeln verschärfen, aber nicht ohne genehmigte Ausnahme abschwächen.

#### `docs/adr/`

Enthält langlebige Architekturentscheidungen. Bestehende akzeptierte ADRs haben Vorrang vor neuen Requirements und Plänen.

### 4.3 Änderungsbezogene Dokumente

```text
specs/<change-id>/
├── spec.md
├── plan.md
├── tasks.md
└── evidence.md
```

`spec.md` ist für normale Änderungen verpflichtend. `plan.md`, `tasks.md` und `evidence.md` sind abhängig von Größe, Risiko und Nachweispflicht.

---

## 5. Workflow- und Compliance-Tailoring

### 5.1 Compliance-Profile

Jedes Projekt MUSS genau ein aktives Compliance-Profil in `.ggsad/config.yaml` auswählen und in `docs/project-brief.md` dokumentieren.

| Profil | Typischer Einsatz | Mindestmerkmale |
|---|---|---|
| `lean` | Pre-PMF MVPs, Prototypen, Solo-Entwicklung, schnelle Iteration | minimale Artefakte, möglichst automatische Checks, Selbstfreigabe sofern keine kritische Regel entgegensteht |
| `standard` | normale Produkt- und Teamentwicklung | separate Spezifikation für normale Changes, definierte Qualitätsgates, dokumentierte Evidence, Peer Review wenn praktikabel |
| `governed` | Enterprise- oder High-Impact-Delivery | starke Traceability, explizite Genehmigungen, Security- und Architekturreview, kontrollierte Release-Evidence |
| `regulated` | regulierte, sicherheitskritische oder extern auditierte Arbeit | Funktionstrennung, unveränderliche oder aufbewahrte Evidence, formale Genehmigungen, Compliance-Mappings, auditfähige History |

Projekte KÖNNEN zusätzliche Profile definieren. Custom Profiles MÜSSEN von einem Default-Profil erben oder alle Invarianten und Abweichungen explizit dokumentieren.

### 5.2 Tailoring-Dimensionen

Ein Profil KANN Phasen, Artefakte, Pflichtsektionen, Kritikalität von Kriterien, Checks, Evidence-Aufbewahrung, Genehmigungen, Agentenautonomie, Release-Regeln und Integrationsmappings anpassen.

Ein niedrigeres Compliance-Profil KANN optionale Kontrollen reduzieren. Es DARF den unveränderlichen Kern aus Abschnitt 3.7 NICHT abschalten.

### 5.3 Profilauflösung

Der wirksame Workflow MUSS in dieser Reihenfolge aufgelöst werden:

1. GG-SAD-Invariant Core,
2. gewähltes Compliance-Profil,
3. projektspezifische Konfiguration,
4. Anforderungen der Change-Klasse,
5. lokale Verschärfung in der Change-Spezifikation,
6. Integrationsmappings externer Frameworks und Tools.

Eine niedrigere Ebene DARF eine höhere Ebene nicht stillschweigend abschwächen.

## 6. Größenklassen

### 5.1 Klasse S — Patch

Geeignet für kleine, klar begrenzte Änderungen mit bekannter Lösung und geringem Risiko.

Mindestartefakt:

- Inline-Spezifikation in Issue, Change Request oder Commit-Kontext.

Minimalinhalt:

- Ziel,
- Scope,
- Akzeptanzbedingungen,
- Verifikation.

### 5.2 Klasse M — Change

Geeignet für eigenständige funktionale oder technische Änderungen.

Pflichtartefakt:

- `spec.md`

Optionale Artefakte:

- `plan.md`
- `tasks.md`
- `evidence.md`

### 5.3 Klasse L — Initiative

Geeignet für mehrere unabhängige oder voneinander abhängige Changes.

Eine Initiative MUSS in mehrere Change-Spezifikationen zerlegt werden. Eine kurze Roadmap oder Abhängigkeitsübersicht KANN verwendet werden. Ein Epic ist nicht erforderlich.

---

## 7. Phasenmodell

GG-SAD definiert folgende Standardphasen:

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

Nicht jede Änderung MUSS jede Phase durchlaufen.

### 6.1 Zulässige verkürzte Flows

#### Patch Flow

```text
SPECIFY → BUILD → VERIFY → CLOSED
```

#### Standard Flow

```text
SPECIFY → PLAN → BUILD → VERIFY → CLOSED
```

#### Release Flow

```text
SPECIFY → PLAN → BUILD → VERIFY → RELEASE → CLOSED
```

#### Exploration Flow

```text
EXPLORE → DECIDE → SPECIFY
```

Exploration DARF nicht stillschweigend in produktive Implementierung übergehen.

---

## 8. Zustandsmodell

Jede Phase besitzt einen Status.

### 7.1 Standardstatus

```text
draft
ready
active
waiting
failed
done
cancelled
superseded
```

Empfohlenes Metadatenformat:

```yaml
phase: build
status: waiting
reason: user-approval-required
owner: requestor
resume_when: approval-recorded
```

### 7.2 Zustandsübergänge

```text
DRAFT
  └── DoR erfüllt → READY

READY
  └── Start autorisiert → ACTIVE

ACTIVE
  ├── DoF erfüllt → FAILED
  ├── DoW erfüllt → WAITING
  ├── DoD erfüllt → DONE
  └── sonst → ACTIVE

WAITING
  ├── Resume-Bedingung erfüllt → ACTIVE
  ├── Neuplanung erforderlich → frühere Phase
  ├── Abbruchentscheidung → CANCELLED
  └── DoF erfüllt → FAILED

DONE
  ├── DoR nächste Phase erfüllt → nächste Phase READY
  └── DoR nicht erfüllt → WAITING
```

### 7.3 Auswertungspriorität

Bei jeder Gate-Prüfung MUSS folgende Reihenfolge gelten:

1. DoF
2. DoW
3. DoD
4. DoR der nächsten Phase

Ein erfülltes DoD hebt ein erfülltes DoF oder DoW nicht auf.

---

## 9. Definition of Ready

DoR bestimmt, ob eine Phase beginnen darf.

### 8.1 Ready-to-Spec

Mindestens:

- Ziel oder Problem ist beschrieben.
- erwarteter Nutzen ist verständlich.
- Requestor oder Entscheidungsverantwortlicher ist identifiziert.
- bekannte Constraints sind verfügbar.
- betroffene Systembereiche sind grob bekannt.
- keine offensichtliche Kollision mit der Constitution liegt vor.

### 8.2 Ready-to-Plan

Mindestens:

- Ziel, Scope und Non-Goals sind definiert.
- Requirements und Akzeptanzbedingungen sind verständlich.
- relevante Architektur- und ADR-Vorgaben wurden geprüft.
- offene Fragen sind beantwortet oder explizit akzeptiert.
- keine ungelösten Widersprüche bestehen.

### 8.3 Ready-to-Build

Mindestens:

- Spezifikation ist genehmigt.
- technischer Ansatz ist ausreichend geklärt.
- kritische Risiken wurden bewertet.
- notwendige Abhängigkeiten sind verfügbar.
- Test- und Verifikationskriterien sind definiert.
- keine blockierende Entscheidung steht aus.

### 8.4 Ready-to-Verify

Mindestens:

- geplante Implementierung ist vollständig oder testbar.
- relevante Tests sind vorhanden.
- Build- und Analysewerkzeuge sind verfügbar.
- bekannte Abweichungen sind dokumentiert.

### 8.5 Ready-to-Release

Mindestens:

- Build und erforderliche Tests sind erfolgreich.
- Sicherheits- und Qualitätsgates sind erfüllt.
- Migration und Rollback sind geklärt.
- bekannte Einschränkungen sind dokumentiert.
- erforderliche Genehmigungen liegen vor.

---

## 10. Definition of Done

DoD bestimmt, ob eine Phase erfolgreich abgeschlossen ist.

### 9.1 Spec-Done

Mindestens:

- Ziel, Nutzen und Erfolgssignale sind beschrieben.
- Scope und Non-Goals sind definiert.
- Requirements sind eindeutig und prüfbar.
- jedes verhaltensbezogene Requirement besitzt mindestens ein konkretes Akzeptanzbeispiel oder eine begründete alternative prüfbare Akzeptanzbedingung.
- Constraints sind dokumentiert.
- offene Fragen sind geschlossen oder explizit akzeptiert.
- ADR-Konflikte sind gelöst oder an den Requestor zurückgegeben.
- Spezifikation ist genehmigt.

### 9.2 Plan-Done

Mindestens:

- technischer Ansatz ist beschrieben.
- betroffene Komponenten sind identifiziert.
- Architektur-, Daten-, API- und Betriebsfolgen sind bewertet.
- Teststrategie ist festgelegt.
- Migrations- und Rollbackbedarf ist geklärt.
- Risiken und Entscheidungen sind dokumentiert.
- Umsetzung ist sinnvoll zerlegt.

### 9.3 Build-Done

Mindestens:

- alle genehmigten Änderungen sind implementiert.
- kein unbeabsichtigter Scope wurde aufgenommen.
- Tests wurden ergänzt oder angepasst.
- lokale Qualitätsgates sind erfolgreich.
- erforderliche Dokumentation ist aktualisiert.
- Abweichungen zur Spezifikation sind erklärt und genehmigt.

### 9.4 Verify-Done

Mindestens:

- alle Akzeptanzbedingungen wurden geprüft.
- erforderliche automatisierte Tests sind erfolgreich.
- relevante Negativ- und Fehlerfälle wurden geprüft.
- Regressionstests sind erfolgreich.
- Evidence ist vollständig.
- verbleibende Einschränkungen sind dokumentiert.

### 9.5 Release-Done

Mindestens:

- Deployment oder Veröffentlichung ist erfolgreich.
- Smoke Tests sind erfolgreich.
- Version und Release Notes sind dokumentiert.
- Monitoring zeigt keine kritischen Probleme.
- Rollback ist möglich oder ausdrücklich nicht erforderlich.
- Roadmap und Status sind aktualisiert.

---

## 11. Definition of Wait

DoW beschreibt Bedingungen, unter denen der Flow kontrolliert pausieren MUSS, ohne als fehlgeschlagen zu gelten.

### 10.1 Typische Wait-Kategorien

- `WAIT_USER_INPUT`
- `WAIT_DECISION`
- `WAIT_DEPENDENCY`
- `WAIT_PROCESS`
- `WAIT_APPROVAL`
- `WAIT_EXTERNAL_SYSTEM`

### 10.2 Pflichtinhalt eines Wait-Zustands

Jeder Wait-Zustand MUSS enthalten:

- Grund,
- ausstehende Information oder Entscheidung,
- verantwortliche Person oder Quelle,
- Resume-Bedingung,
- sicheren aktuellen Zustand,
- nächste Aktion nach Fortsetzung.

Template:

```yaml
status: waiting
reason: architecture-decision-required
waiting_for: requestor
resume_when: ADR-approved
safe_state: no-uncommitted-destructive-change
resume_at: planning
next_action: update-plan
```

### 10.3 Verhalten von KI-Agenten im Wait-Zustand

Ein KI-Agent MUSS:

- alle riskanten oder scope-verändernden Aktionen stoppen,
- den bisherigen Zustand sichern,
- die fehlende Entscheidung konkret benennen,
- eine minimale, entscheidbare Frage formulieren,
- keine Annahme als Genehmigung interpretieren,
- nach Erfüllung der Resume-Bedingung an der definierten Stelle fortsetzen.

---

## 12. Definition of Fail

DoF beschreibt Bedingungen, bei denen der Flow erfolglos beendet werden MUSS.

### 11.1 Typische Fail-Kategorien

- kritischer technischer Fehler,
- Datenverlust oder Repository-Korruption,
- kritische Sicherheitsverletzung,
- nicht genehmigter Breaking Change,
- Verstoß gegen Constitution oder ADR,
- Aktion außerhalb des erlaubten Scopes,
- Überschreitung harter Budget-, Kosten- oder Wiederholungsgrenzen,
- nicht wiederherstellbarer Build- oder Migrationszustand,
- dauerhaft nicht erfüllbare Akzeptanzbedingungen.

### 11.2 Pflichtinhalt einer Fail-Regel

Jede Fail-Regel MUSS enthalten:

- Trigger,
- erforderliche Reaktion,
- erlaubte Sicherungsmaßnahmen,
- Abschlussstatus,
- erforderliche Dokumentation.

Template:

```markdown
### F-01 — Unauthorized Breaking Change

**Trigger**  
Ein Breaking Change ist erforderlich, aber nicht genehmigt.

**Required response**

- Implementierung stoppen.
- nicht genehmigte Änderungen zurücksetzen oder isolieren.
- vorhandene Evidence sichern.
- Konflikt in der Spezifikation dokumentieren.
- Flow als fehlgeschlagen markieren.

**Final status**  
`FAILED_POLICY_VIOLATION`
```

---

## 13. Konflikt- und Entscheidungsregeln

### 12.1 ADR-Konflikte

Bestehende akzeptierte ADRs haben Vorrang.

Wenn ein Requirement einem ADR widerspricht, MUSS der Agent:

1. den Konflikt im Requirement oder in der Spezifikation dokumentieren,
2. die Planung oder Umsetzung stoppen,
3. das Requirement an den Requestor zurückgeben,
4. eine Entscheidung anfordern,
5. die Entscheidung kommunizieren und referenzieren.

Ein bestehendes ADR DARF nur durch einen ausdrücklich genehmigten Änderungsflow geändert oder ersetzt werden.

### 12.2 Spezifikationsdrift

Wenn Implementierung oder Tests von der Spezifikation abweichen, MUSS eine der folgenden Aktionen erfolgen:

- Implementierung anpassen,
- Spezifikation vor Fortsetzung ändern und erneut genehmigen,
- Abweichung als akzeptierte Ausnahme dokumentieren,
- Flow bei unzulässiger Abweichung stoppen.

### 12.3 Breaking Changes

Breaking Changes MÜSSEN ausdrücklich markiert, bewertet und genehmigt werden. Ohne Genehmigung gilt die entsprechende DoF-Regel.

---

## 14. Pair-Review-Modell

### 14.1 Aktivierung

Pair Review KANN durch Compliance-Profil, Projektumfang, Change-Klasse, Risiko, Artefakttyp oder lokale Verschärfung aktiviert oder verpflichtend werden. Lean- und risikoarme Class-S-Flows KÖNNEN Pair Review auslassen. Governed- oder Regulated-Profile SOLLEN Pair Review für relevante High-Impact-Changes verlangen.

### 14.2 Teilnehmer und Identität

Teilnehmer können Menschen, KI-Agenten, Coding-Agenten, Review-Agenten oder externe Review-Dienste sein. Requestor und Reviewer MÜSSEN im selben Review-Zyklus unterschiedliche Teilnehmeridentitäten besitzen.

Beispiele:

- Requestor: Human; Reviewer: Human
- Requestor: Human; Reviewer: Claude Code
- Requestor: Claude Code; Reviewer: Codex
- Requestor: Codex; Reviewer: Human
- Requestor: Claude Code; Reviewer: CodeRabbit

Getrennte Sessions derselben Teilnehmeridentität erfüllen die Unabhängigkeitsregel nicht, sofern das Projekt sie nicht ausdrücklich und begründet als unabhängig kontrollierte Teilnehmer definiert.

### 14.3 Review-Zyklus

Ein Pair-Review-Zyklus MUSS Requestor und Reviewer identifizieren, Scope und Kriterien definieren, ein stabiles prüfbares Arbeitsergebnis bereitstellen, Findings dokumentieren, Findings an den Requestor zurückgeben, Disposition und Korrekturen erfassen, erforderliche Blocking-Findings nachprüfen und das Endergebnis als Evidence sichern.

### 14.4 Findings

Ein Finding SOLL stabile IDs, Review-Zyklus, Teilnehmer, Kategorie, Severity, betroffenes Artefakt, Beschreibung, erforderliche oder empfohlene Aktion, Status und Disposition enthalten.

Empfohlene Severities: `informational`, `minor`, `major`, `blocking`, `critical`.

Empfohlene Status: `open`, `accepted`, `rejected`, `resolved`, `verified`, `withdrawn`.

Offene Blocking-Findings MÜSSEN das relevante Abschluss- oder Übergangsgate blockieren, sofern sie nicht durch einen autorisierten Decision Owner formal entschieden wurden.

### 14.5 Review-Artefakte

Pair-Review-Evidence KANN inline in `evidence.md` geführt werden. Ein separates `review.md` ist bedingt und SOLL nur bei ausreichender Komplexität, Aufbewahrungspflicht, Auditierbarkeit oder Compliance erforderlich sein.

Findings sind keine Requirements und überschreiben keine höherrangigen Artefakte. Findings mit Requirement- oder Architekturänderungen MÜSSEN den entsprechenden Spec- oder ADR-Flow auslösen.

## 15. Evidence-Modell

Evidence MUSS nachvollziehbar zeigen, ob Requirements, Gates und Qualitätskriterien erfüllt wurden.

Zulässige Evidence umfasst:

- Testresultate,
- Build-Ausgaben,
- statische Analyse,
- Security-Scans,
- Review-Freigaben,
- Logs,
- Screenshots,
- Messwerte,
- Deploy- oder Release-Nachweise,
- Referenzen auf Commits und Pull Requests.

Minimales Evidence-Template:

```markdown
# Verification Evidence

## Requirement Coverage

| Requirement | Evidence | Result |
|---|---|---|
| R1 | `tests/...` | Pass |
| R2 | `tests/...` | Pass |

## Quality Gates

- Build: Pass
- Unit tests: Pass
- Integration tests: Pass
- Static analysis: Pass
- Security checks: Pass

## Deviations

None.

## Final Status

Done.
```

Bei kleinen Changes KANN Evidence direkt in `spec.md` dokumentiert werden.

---

## 16. Mindesttemplates

### 16.1 `spec.md`

```markdown
# Change: <Titel>

## Metadata

- Change ID: <id>
- Class: S | M | L
- Phase: specify
- Status: draft
- Requestor: <name-or-role>

## Goal

<Gewünschter Zielzustand und Nutzen>

## Success Signals

- <messbares oder prüfbares Signal>

## Non-Goals

- <ausdrücklich nicht enthalten>

## Context

<relevanter Ist-Zustand>

## Scope

### Included

- <enthalten>

### Excluded

- <nicht enthalten>

## Requirements

### R1 — <Titel>

<prüfbare Anforderung>

## Acceptance Examples

### E1 — <Titel>

- Covers: R1

Given <Ausgangslage>  
When <Aktion>  
Then <Ergebnis>

## Constraints

- <projektweite oder lokale Einschränkung>

## Flow Gates

### Additional Ready Conditions

- <optional>

### Additional Done Conditions

- <optional>

### Additional Wait Conditions

- <optional>

### Additional Fail Conditions

- <optional>

## Verification

- <Nachweis oder Test>

## Pair Review

- Required: yes | no
- Requestor: <participant-id>
- Reviewer: <different-participant-id>
- Scope: <Artefakte und Kriterien>

## Open Questions

- None.
```

### 16.2 `plan.md`

```markdown
# Implementation Plan: <Titel>

## Technical Approach

<gewählter Ansatz>

## Affected Components

- <Komponente>

## Architecture Impact

- <Auswirkung oder None>

## Data and API Impact

- <Auswirkung oder None>

## Test Strategy

- <Testebene und Abdeckung>

## Migration and Rollback

- <Strategie oder Not required>

## Risks

- <Risiko und Maßnahme>

## Decisions

- <Entscheidung mit Referenz>

## Implementation Sequence

1. <Schritt>
2. <Schritt>
```

### 16.3 `tasks.md`

```markdown
# Implementation Checklist

- [ ] <umsetzbarer Schritt>
- [ ] Tests ergänzen oder aktualisieren.
- [ ] Qualitätsgates ausführen.
- [ ] Dokumentation aktualisieren.
- [ ] Spec-Code-Abgleich durchführen.
- [ ] Evidence erfassen.
```

### 16.4 `evidence.md`

```markdown
# Verification Evidence

## Requirement Coverage

| Requirement | Evidence | Result |
|---|---|---|

## Quality Gates

- Build:
- Tests:
- Static analysis:
- Security:

## Deviations

- None.

## Final Gate Evaluation

- DoF triggered: No
- DoW triggered: No
- DoD satisfied: Yes | No
- Next DoR satisfied: Yes | No | Not applicable

## Final Status

<status>
```

### 16.5 `project-brief.md`

```markdown
# Project Brief

## Problem and Opportunity

<Problem, Bedarf oder Opportunity>

## Target Users and Stakeholders

- <Nutzer oder Stakeholder>

## Desired Outcomes and Success Signals

- <prüfbares Outcome>

## Project Type and Lifecycle Context

- Greenfield | Brownfield | Migration | Modernization | Re-engineering

## Scope and Non-Goals

### Included

- <enthalten>

### Excluded

- <ausgeschlossen>

## Constraints

- Time:
- Budget:
- Technology:
- Delivery:

## Compliance Profile

`lean | standard | governed | regulated | <custom>`

## Operating Mode

`stand-alone | combination`

## Integrated Methods and Tools

- <Methode, Framework, Tool, Agent oder None>
```

### 16.6 `architecture.md`

```markdown
# Architecture

## System Context

<System und externe Akteure>

## Components

| Component | Responsibility | Dependencies |
|---|---|---|

## Boundaries and Constraints

- <Grenze oder Constraint>

## Data Flows

- <wichtiger Datenfluss>

## Deployment and Operations

- <Betriebsmodell>

## Known Limitations

- <Limitation>

## Related ADRs

- <ADR reference>
```

### 16.7 `roadmap.md`

```markdown
# Roadmap

## Now

- <aktives Ziel>

## Next

- <nächstes Ziel>

## Later

- <späteres Ziel>

## Open

- <ungeklärte Richtung oder Option>
```

---


## 17. Kombinationsverträge

Jede externe Integration MUSS ein Mapping mit Integrationsname und Version, Zweck, zugeordneten GG-SAD-Phasen und Artefakten, autoritativen Quellen, Berechtigungen, Gate-Interaktion, Zustandssynchronisation sowie Fehler-, Rollback- und Deinstallationsverhalten definieren.

GG-SAD KANN beispielsweise mit GSD, OpenSpec, Spec Kit oder BMAD sowie mit Tools wie Hermes oder Kiro kombiniert werden. Diese Namen sind Beispiele und keine normativen Abhängigkeiten.

## 18. GG-SAD-Memory-Modell

GG-SAD KANN einen Project Memory bereitstellen. Bis eine Referenzimplementierung existiert, ist Memory optional und DARF führende Dokumente nicht ersetzen.

Memory MUSS mindestens folgende Record-Typen unterstützen:

- **Decision** — fachliche, prozessuale, Implementierungs- oder Betriebsentscheidungen, die keine Architekturentscheidungen sind;
- **Learning** — wiederverwendbares Wissen aus Delivery oder Betrieb;
- **Failure** — fehlgeschlagene Ansätze, Incidents, Ursachen, Maßnahmen und Prävention;
- **Definition** — Glossarbegriffe, Domain Language, Abkürzungen und kanonische Bedeutungen;
- **External Source** — externe Informationen mit Provenance, Abrufdatum, Relevanz und Trust-Metadaten.

Architekturentscheidungen MÜSSEN ADRs bleiben. Eine Memory-Decision DARF nicht zur Umgehung des ADR-Prozesses verwendet werden.

Memory Records MÜSSEN stabile IDs, Scope, Provenance, Status, Zeitstempel und Verweise auf zugehörige Artefakte besitzen. Retrieval MUSS Projektberechtigungen und das aktive Compliance-Profil respektieren.

## 19. Agenten-Ausführungsalgorithmus

Ein KI-Agent MUSS für jede aktive Phase folgenden Ablauf verwenden:

```text
1. Project Brief, projektweite Regeln, relevante ADRs, Architektur, aktives Compliance-Profil, Integrationsmappings und anwendbare Memory Records laden.
2. Aktuelle Phase, Status, Ziel und Scope bestimmen.
3. DoF prüfen.
4. DoW prüfen.
5. DoD der aktuellen Phase prüfen.
6. Falls DoD erfüllt: Evidence sichern.
7. DoR der nächsten Phase prüfen.
8. Nur bei erfüllter DoR die nächste Phase starten.
9. Änderungen ausschließlich innerhalb des genehmigten Scopes ausführen.
10. Nach jeder relevanten Änderung Spec-, Architektur- und Policy-Konformität prüfen.
11. Bei Konflikt, Unsicherheit oder fehlender Genehmigung kontrolliert warten.
12. Vor Abschluss finalen Drift- und Evidence-Check durchführen.
```

### 19.1 Agentenverbote

Ein KI-Agent DARF NICHT:

- Ziele, Requirements oder Genehmigungen erfinden,
- fehlende Informationen als Zustimmung interpretieren,
- höherrangige Dokumente stillschweigend ändern,
- Breaking Changes ohne Genehmigung umsetzen,
- Wartezustände durch Spekulation umgehen,
- einen Flow als erledigt markieren, wenn Evidence fehlt,
- Fehler verbergen oder als erfolgreiche Abweichung umdeuten,
- über den genehmigten Scope hinaus arbeiten.

---

## 20. Abschlusskriterium für einen Change

Ein Change darf nur den Status `closed` oder `done` erhalten, wenn:

- keine DoF-Bedingung aktiv ist,
- keine DoW-Bedingung aktiv ist,
- alle erforderlichen DoD-Kriterien erfüllt sind,
- Requirement- und Acceptance-Example-Abdeckung nachgewiesen ist,
- erforderliche Pair-Review-Zyklen abgeschlossen und Blocking-Findings gelöst oder formal entschieden sind,
- Spezifikation, Implementierung, Tests und Dokumentation konsistent sind,
- relevante Roadmap-, Architektur- oder ADR-Verweise aktualisiert wurden,
- der finale Status nachvollziehbar dokumentiert wurde.

---

## 21. Kurzreferenz

```text
Goal
  ↓
Definition of Ready
  ↓
Active Phase
  ├── Definition of Fail → FAILED
  ├── Definition of Wait → WAITING
  └── Definition of Done → DONE
                              ↓
                    Next Definition of Ready
                              ↓
                         Next Phase
```

Führende Wahrheit:

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

GG-SAD optimiert nicht auf maximale Dokumentmenge, sondern auf **klare Ziele, kontrollierte Übergänge und überprüfbare Ergebnisse**.
