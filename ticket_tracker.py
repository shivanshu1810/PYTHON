"""Helpdesk Ticket Tracker - a small command-line tool for IT support.

This is a beginner project: it stores support tickets in a JSON file
so you can add, list, update, and close tickets from the terminal.

Usage:
    python3 ticket_tracker.py add --title "Printer not working" --requester "Ana" --category hardware --priority high
    python3 ticket_tracker.py list
    python3 ticket_tracker.py list --status open
    python3 ticket_tracker.py update 1 --status in-progress --note "Ordered new toner"
    python3 ticket_tracker.py close 1
    python3 ticket_tracker.py report
"""

import argparse
import json
import os
from datetime import datetime

DATA_FILE = "tickets.json"
CATEGORIES = ["hardware", "software", "network", "account", "other"]
PRIORITIES = ["low", "medium", "high"]
STATUSES = ["open", "in-progress", "resolved", "closed"]


def load_tickets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tickets(tickets):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)


def next_id(tickets):
    if not tickets:
        return 1
    return max(t["id"] for t in tickets) + 1


def add_ticket(title, requester, category, priority):
    tickets = load_tickets()
    ticket = {
        "id": next_id(tickets),
        "title": title,
        "requester": requester,
        "category": category,
        "priority": priority,
        "status": "open",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "notes": [],
    }
    tickets.append(ticket)
    save_tickets(tickets)
    print(f"Ticket #{ticket['id']} created: {title}")


def list_tickets(status=None):
    tickets = load_tickets()
    if status:
        tickets = [t for t in tickets if t["status"] == status]
    if not tickets:
        print("No tickets found.")
        return
    print(f"{'ID':<4} {'Status':<12} {'Priority':<9} {'Category':<9} {'Title'}")
    print("-" * 70)
    for t in tickets:
        print(f"{t['id']:<4} {t['status']:<12} {t['priority']:<9} {t['category']:<9} {t['title']}")


def update_ticket(ticket_id, status=None, note=None):
    tickets = load_tickets()
    for t in tickets:
        if t["id"] == ticket_id:
            if status:
                t["status"] = status
            if note:
                t["notes"].append(note)
            save_tickets(tickets)
            print(f"Ticket #{ticket_id} updated.")
            return
    print(f"Ticket #{ticket_id} not found.")


def close_ticket(ticket_id):
    update_ticket(ticket_id, status="closed")


def report():
    tickets = load_tickets()
    total = len(tickets)
    open_count = len([t for t in tickets if t["status"] == "open"])
    in_progress = len([t for t in tickets if t["status"] == "in-progress"])
    closed = len([t for t in tickets if t["status"] == "closed"])
    print(f"Total tickets: {total}")
    print(f"Open: {open_count} | In progress: {in_progress} | Closed: {closed}")
    print("\nBy category:")
    for category in CATEGORIES:
        count = len([t for t in tickets if t["category"] == category])
        print(f"  {category}: {count}")


def main():
    parser = argparse.ArgumentParser(description="Helpdesk Ticket Tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Create a new ticket")
    add.add_argument("--title", required=True)
    add.add_argument("--requester", required=True)
    add.add_argument("--category", choices=CATEGORIES, default="other")
    add.add_argument("--priority", choices=PRIORITIES, default="medium")

    list_p = sub.add_parser("list", help="List tickets")
    list_p.add_argument("--status", choices=STATUSES)

    update = sub.add_parser("update", help="Update a ticket")
    update.add_argument("id", type=int)
    update.add_argument("--status", choices=STATUSES)
    update.add_argument("--note")

    close = sub.add_parser("close", help="Close a ticket")
    close.add_argument("id", type=int)

    sub.add_parser("report", help="Show a summary report")

    args = parser.parse_args()
    if args.command == "add":
        add_ticket(args.title, args.requester, args.category, args.priority)
    elif args.command == "list":
        list_tickets(args.status)
    elif args.command == "update":
        update_ticket(args.id, args.status, args.note)
    elif args.command == "close":
        close_ticket(args.id)
    elif args.command == "report":
        report()


if __name__ == "__main__":
    main()
