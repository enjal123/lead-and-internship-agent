"""
Prints everything currently saved in the database in a readable format.
This is the easiest way to see what the pipelines have found -- results
are stored in a local SQLite file (agent.db by default) rather than
printed to the console during the run.

Run with: python view_results.py
"""
from database.business_queries import get_all_businesses
from database.internship_queries import get_unapplied_internships


def main():
    businesses = get_all_businesses()
    internships = get_unapplied_internships()

    print(f"\n=== Business Leads ({len(businesses)}) ===")
    for b in businesses:
        print(f"- [{b['lead_score']}/10] {b['business_name']} — {b['website']} "
              f"(contacted: {'yes' if b['outreach_sent'] else 'no'})")

    print(f"\n=== Internships not yet applied to ({len(internships)}) ===")
    for i in internships:
        friendly = "good fit" if i["freshman_friendly"] else "reach"
        print(f"- [{friendly}] {i['title']} — {i['link']}")

    if not businesses and not internships:
        print("\nNothing saved yet. Run `python main.py businesses` or "
              "`python main.py internships` first.")


if __name__ == "__main__":
    main()
