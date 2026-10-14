# Helpdesk Ticket Tracker

A small command-line tool for IT support work. It stores support tickets in a JSON file so you can add, list, update, and close tickets from the terminal.

Built as a home lab project after graduation to practise Python and the ticket workflow used in real service desk jobs (ServiceNow, Halo ITSM).

## What it does

- Create tickets with title, requester, category, and priority
- List tickets, optionally filtered by status
- Update a ticket's status and add notes
- Close tickets
- Print a summary report (open / in progress / closed, and counts by category)

## How to run it

```bash
python3 ticket_tracker.py add --title "Printer not working" --requester "Ana" --category hardware --priority high
python3 ticket_tracker.py list
python3 ticket_tracker.py list --status open
python3 ticket_tracker.py update 1 --status in-progress --note "Ordered new toner"
python3 ticket_tracker.py close 1
python3 ticket_tracker.py report
```

## Categories

hardware, software, network, account, other

## Priorities

low, medium, high

## Statuses

open, in-progress, resolved, closed

## Skills used

Python, argparse, JSON file storage, command-line tools
