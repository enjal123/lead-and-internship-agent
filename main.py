"""
AI Outreach & Internship Discovery Agent -- CLI entry point.

Usage:
    python main.py businesses [--query "..."] [--max N]
    python main.py internships [--query "..."] [--max N] [--no-resume]
    python main.py outreach [--send]
    python main.py all

Examples:
    python main.py businesses --query "restaurants Sonoma County" --max 15
    python main.py internships --query "backend engineering internship 2027"
    python main.py outreach --send
"""
import argparse

from orchestrators.business_pipeline import run_business_pipeline
from orchestrators.internship_pipeline import run_internship_pipeline
from orchestrators.outreach_pipeline import run_outreach_pipeline
from utils.logger import logger


def main():
    parser = argparse.ArgumentParser(description="AI Outreach & Internship Discovery Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    businesses_parser = subparsers.add_parser("businesses", help="Find and analyze business leads")
    businesses_parser.add_argument("--query", default=None, help="Search query override")
    businesses_parser.add_argument("--max", type=int, default=10, help="Max leads to process")

    internships_parser = subparsers.add_parser("internships", help="Find and analyze internships")
    internships_parser.add_argument("--query", default=None, help="Search query override")
    internships_parser.add_argument("--max", type=int, default=10, help="Max postings to process")
    internships_parser.add_argument("--no-resume", action="store_true", help="Skip resume tailoring")

    outreach_parser = subparsers.add_parser("outreach", help="Queue (and optionally send) outreach emails")
    outreach_parser.add_argument("--send", action="store_true", help="Actually send queued emails")

    subparsers.add_parser("all", help="Run businesses, then internships, then queue outreach")

    args = parser.parse_args()

    if args.command == "businesses":
        results = run_business_pipeline(query=args.query, max_results=args.max)
        print(f"\nSaved {len(results)} business lead(s) to the database.")

    elif args.command == "internships":
        results = run_internship_pipeline(
            query=args.query, max_results=args.max, build_resumes=not args.no_resume
        )
        print(f"\nSaved {len(results)} internship posting(s) to the database.")

    elif args.command == "outreach":
        queued = run_outreach_pipeline(send=args.send)
        print(f"\nQueued {queued} outreach email(s).")

    elif args.command == "all":
        run_business_pipeline()
        run_internship_pipeline()
        run_outreach_pipeline()
        print("\nDone. Check the database (see README) for results.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
