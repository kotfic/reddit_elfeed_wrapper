from setuptools import setup

setup(
    name="reddit_wrapper",
    version="0.0",
    author="Christoper Kotfila",
    author_email="kotfic@gmail.com",
    license="GPL",
    py_modules=['reddit_wrapper'],
    entry_points={
        "console_scripts": [
            "elfeed_wrapper = reddit_elfeed_wrapper.app:main"
        ]
    })
