"""
Small CLI to run any maintenance task by name.
Run with: python -m tasks.task_runner <task_name>
"""
import sys

from tasks.cleanup_tasks import clear_failed_emails, clear_old_generated_resumes
from tasks.retry_tasks import retry_failed_emails

TASKS = {
    "clear_failed_emails": clear_failed_emails,
    "clear_old_resumes": clear_old_generated_resumes,
    "retry_failed_emails": retry_failed_emails,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in TASKS:
        print(f"Usage: python -m tasks.task_runner <{'|'.join(TASKS)}>")
        sys.exit(1)

    TASKS[sys.argv[1]]()


if __name__ == "__main__":
    main()
