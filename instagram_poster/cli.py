import argparse
from datetime import datetime

from instagram_poster import projects, queue, scheduler
from instagram_poster.timeutil import parse_local_time


def cmd_add(args) -> None:
    scheduled_time = parse_local_time(args.time)
    carousel_urls = args.carousel_url or None
    post = queue.add_post(
        media_type=args.type,
        caption=args.caption or "",
        scheduled_time=scheduled_time,
        media_url=args.media_url,
        carousel_urls=carousel_urls,
    )
    print(f"Queued post {post['id']} for {post['scheduled_time']} (UTC)")


def cmd_list(args) -> None:
    posts = queue.load_all()
    if args.status:
        posts = [p for p in posts if p["status"] == args.status]
    if not posts:
        print("No posts.")
        return
    for p in posts:
        print(f"{p['id']}  {p['status']:9s}  {p['media_type']:9s}  {p['scheduled_time']}  {p['caption'][:40]!r}")


def cmd_cancel(args) -> None:
    post = queue.cancel_post(args.id)
    print(f"Cancelled post {post['id']}")


def cmd_run_once(args) -> None:
    scheduler.run_once()


def cmd_projects(args) -> None:
    for row in projects.load_projects():
        print(f"{row['#']:>3}  {row['Project Name']:35s}  {row['Area / Neighbourhood']}")


def cmd_queue_project(args) -> None:
    row = projects.get_project(args.project)
    caption = projects.generate_caption(row)
    scheduled_time = parse_local_time(args.time)
    post = queue.add_post(
        media_type=args.type,
        caption=caption,
        scheduled_time=scheduled_time,
        media_url=args.media_url,
    )
    print(f"Queued post {post['id']} for {row['Project Name']} at {post['scheduled_time']} (UTC)")
    print("\n--- caption ---\n")
    print(caption)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="instagram_poster", description="Queue and publish Instagram posts")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Queue a new post")
    add.add_argument("--type", required=True, choices=["IMAGE", "REELS", "VIDEO", "CAROUSEL"])
    add.add_argument("--media-url", help="Public URL of the image/video (not needed for CAROUSEL)")
    add.add_argument("--carousel-url", action="append", help="Repeatable: public URL of each carousel image")
    add.add_argument("--caption", default="")
    add.add_argument("--time", required=True, help="e.g. '2026-09-20 09:00' (Africa/Nairobi) or ISO 8601 with offset")
    add.set_defaults(func=cmd_add)

    list_cmd = sub.add_parser("list", help="List queued posts")
    list_cmd.add_argument("--status", choices=sorted(queue.VALID_STATUSES))
    list_cmd.set_defaults(func=cmd_list)

    cancel = sub.add_parser("cancel", help="Cancel a pending post")
    cancel.add_argument("id")
    cancel.set_defaults(func=cmd_cancel)

    run_once = sub.add_parser("run-once", help="Publish any posts that are due right now")
    run_once.set_defaults(func=cmd_run_once)

    projects_cmd = sub.add_parser("projects", help="List the Nest Kenya portfolio projects")
    projects_cmd.set_defaults(func=cmd_projects)

    queue_project = sub.add_parser(
        "queue-project",
        help="Auto-write an on-brand caption for a portfolio project and queue it (still needs a photo URL)",
    )
    queue_project.add_argument("project", help="Project # from `projects` (e.g. 15 for Galaxy ONE)")
    queue_project.add_argument("--media-url", required=True, help="Public URL of the photo/video to post")
    queue_project.add_argument("--type", default="IMAGE", choices=["IMAGE", "REELS", "VIDEO"])
    queue_project.add_argument("--time", required=True, help="e.g. '2026-09-20 09:00' (Africa/Nairobi) or ISO 8601 with offset")
    queue_project.set_defaults(func=cmd_queue_project)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
