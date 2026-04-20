import reflex as rx

config = rx.Config(
    app_name="student_manager",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)