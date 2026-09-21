# ChiSoSecure

ChiSoSecure is a full-stack security operations platform built to demonstrate security event ingestion, rule-based threat detection, incident management, automated response workflows, authentication, role-based access control, and external API integration.

The project combines cybersecurity concepts with backend API development, database design, frontend development, containerization, automated testing, and CI/CD.

## Overview

ChiSoSecure receives security telemetry, analyzes events using detection rules, generates alerts when suspicious behavior is identified, and creates incidents for high-severity threats.

Security analysts can use the web dashboard to review events and alerts, investigate incidents, execute response actions, and manage platform access.

External applications and security tools can also submit events through an API-key authenticated ingestion endpoint.

## Security Pipeline

```text
Security Event
      |
      v
Event Ingestion
      |
      v
Detection Engine
      |
      v
    Alert
      |
      v
Incident Creation
      |
      v
Investigation
      |
      v
Response Action
