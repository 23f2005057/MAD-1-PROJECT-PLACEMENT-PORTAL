# Placement Portal

A role-based web application for managing campus recruitment, built as a solo project for the IIT Madras BS Degree "Modern Application Development" course.

## Overview

The Placement Portal streamlines the campus placement process by giving each stakeholder a dedicated dashboard:

- **Admin** — approves companies and placement drives, oversees the overall process
- **Company** — posts placement drives, reviews and manages student applications
- **Student** — browses drives, applies, and tracks application status

## Tech Stack

- **Backend:** Flask
- **ORM:** SQLAlchemy
- **Database:** SQLite
- **Templating:** Jinja2
- **Styling:** Bootstrap

## Database Schema

The schema was designed from scratch around five related tables:

| Table | Purpose |
|---|---|
| `User` | Base authentication/identity record, linked to role-specific profiles |
| `Student` | Student profile data and academic details |
| `Company` | Recruiter/company profile and verification status |
| `Placement_drive` | A recruitment drive posted by a company (role, eligibility, dates) |
| `Application` | A student's application to a drive, with status tracking |

## Key Features

- Role-based access control across three distinct dashboards
- Company and drive approval workflow (Admin)
- End-to-end application lifecycle: post → apply → review → status update
- Relational schema enforcing data integrity across users, drives, and applications

## Setup

```bash
git clone https://github.com/23f2005057/MAD-1-PROJECT-PLACEMENT-PORTAL.git
cd "MAD-1-PROJECT-PLACEMENT-PORTAL/Mad placement app"
pip install -r requirements.txt
python app.py
```

> Note: fill in exact filenames/commands above if they differ from your local setup — this is a starting template.

## Project Context

Built independently (schema design, routing, and templates), with Claude used for roughly 20–25% of the work (primarily debugging Flask errors and SQLAlchemy relationship issues), per the AI/LLM usage declaration submitted with the project report.
