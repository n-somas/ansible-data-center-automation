# Ansible Data Center Automation

Automatisierung und Überwachung eines Ubuntu-Servers mit Ansible und Python.

## Projektziel

Das Projekt bildet einen typischen DevOps- und 3rd-Level-Support-Ablauf ab:

1. Server über SSH anbinden
2. Basiskonfiguration automatisieren
3. Nginx installieren und konfigurieren
4. Systemzustand erfassen
5. Health Report als JSON speichern
6. Report mit Python analysieren
7. Analysefunktionen mit Pytest testen

## Architektur

```text
Windows Host
│
├── WSL / Ubuntu
│   └── Ansible Control Node
│
└── VirtualBox
    └── Ubuntu Server
        └── Ansible Managed Node
```

Ansible läuft innerhalb von WSL und verwaltet die Ubuntu-VM über SSH.

## Funktionen

- Verwaltung eines Ubuntu-Servers über SSH
- YAML-basiertes Ansible Inventory
- Rollenbasierte Projektstruktur
- Installation von Administrationswerkzeugen
- Installation und Konfiguration von Nginx
- Dynamische Statusseite mit Jinja2
- Erfassung von Festplatten- und Arbeitsspeicherinformationen
- Überwachung des Nginx-Servicezustands
- Lokale Speicherung eines JSON-Health-Reports
- Python-basierte Bewertung des Serverzustands
- Automatisierte Tests mit Pytest
- Qualitätsprüfung mit `ansible-lint`
- Rollenbasierte Ausführung über Ansible-Tags

## Technologien

- Ansible
- Python
- Pytest
- YAML
- Jinja2
- JSON
- Nginx
- Linux
- SSH
- Git und GitHub
- WSL
- VirtualBox

## Projektstruktur

```text
ansible-data-center-automation/
├── ansible.cfg
├── inventories/
│   └── lab/
│       └── hosts.yml
├── playbooks/
│   ├── install_tools.yml
│   ├── server_info.yml
│   ├── site.yml
│   └── test.yml
├── roles/
│   ├── common/
│   ├── health_check/
│   └── webserver/
├── reports/
├── scripts/
│   ├── __init__.py
│   └── analyze_health_report.py
├── tests/
│   └── test_health_analyzer.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Rollen

### Common

Installiert grundlegende Administrationswerkzeuge wie `htop`, `curl`, `git` und `unzip`.

### Webserver

Installiert Nginx, startet den Service, erzeugt eine dynamische Jinja2-Statusseite und lädt Nginx bei Änderungen über einen Handler neu.

### Health Check

Erfasst Festplattenauslastung, Arbeitsspeicher, Betriebssysteminformationen, Hostname und den Zustand des Nginx-Service. Die Ergebnisse werden lokal als JSON gespeichert.

## Voraussetzungen

### Control Node

- Linux oder WSL
- Python
- SSH
- Git

### Managed Node

- Ubuntu Server
- aktiver SSH-Zugang
- Benutzer mit `sudo`-Berechtigung
- Python auf dem Zielsystem

## Installation

```bash
git clone git@github.com:n-somas/ansible-data-center-automation.git
cd ansible-data-center-automation
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Inventory

Datei:

```text
inventories/lab/hosts.yml
```

Beispiel:

```yaml
---
all:
  children:
    datacenter:
      hosts:
        managed-server:
          ansible_host: 192.168.xx.xxx
          ansible_user: ansible
```

Die Platzhalter müssen an die eigene Umgebung angepasst werden.

> Sicherheitsregel: Keine echten IP-Adressen, Benutzernamen, Passwörter, privaten Schlüssel oder Tokens im öffentlichen Repository veröffentlichen.

## Verwendung

SSH-Verbindung testen:

```bash
ssh ansible@192.168.xx.xxx
```

Ansible-Verbindung prüfen:

```bash
ansible all -m ping
```

Syntax prüfen:

```bash
ansible-playbook playbooks/site.yml --syntax-check
```

Komplettes Playbook ausführen:

```bash
ansible-playbook playbooks/site.yml --ask-become-pass
```

Nur Health Check ausführen:

```bash
ansible-playbook playbooks/site.yml --tags health_check --ask-become-pass
```

Webserver konfigurieren und anschließend prüfen:

```bash
ansible-playbook playbooks/site.yml --tags webserver,health_check --ask-become-pass
```

## Health Report analysieren

```bash
python scripts/analyze_health_report.py reports/managed-server.json
```

Mögliche Zustände:

```text
healthy
warning
critical
```

## Tests

```bash
python -m pytest -v
```

Getestet werden:

- Extraktion der Festplattenauslastung
- gesunder Serverzustand
- kritische Festplattenauslastung
- gestoppter Nginx-Service

## Codequalität

```bash
ansible-lint
```

Aktueller Stand:

```text
Passed: 0 failure(s), 0 warning(s)
```

## Idempotenz

Ansible beschreibt den gewünschten Systemzustand. Ein wiederholter Lauf soll keine unnötigen Änderungen erzeugen.

```text
Erster Lauf:  changed > 0
Zweiter Lauf: changed = 0
```

## Getesteter Fehlerfall

1. Nginx stoppen
2. Health Check ausführen
3. JSON-Report erzeugen
4. Python-Auswertung starten
5. kritischen Zustand erkennen
6. Nginx über Ansible wieder starten
7. gesunden Zustand bestätigen

## Lernziele

- Control Node und Managed Node
- SSH-Key-Authentifizierung
- Inventory-Verwaltung
- Playbooks und Rollen
- Tasks und Handler
- Variablen und Facts
- Jinja2-Templates
- Idempotenz
- Serviceverwaltung
- JSON-Verarbeitung
- Python-Auswertung
- automatisierte Tests
- Ansible-Codequalität
- Git-basierte Versionsverwaltung

## Projekt

Öffentliches GitHub-Repository:

`github.com/n-somas/ansible-data-center-automation`
