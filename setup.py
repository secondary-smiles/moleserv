from setuptools import find_packages, setup

setup(
        name="moleserv",
        version="0.1.0",
        description="Molerat protocol server library.",
        url="https://git.trinket.icu/moleserv.git",

        author="Shav Kinderlehrer",
        author_email="molerat@git.trinket.icu",

        license="0BSD",

        packages=find_packages(include=["moleserv"]),

        install_requires=["pyOpenSSL"],

        project_urls={
            "Source": "https://git.trinket.icu/moleserv.git",
            "Github": "https://github.com/secondary-smiles/moleserv",
        },

        keywords="network server library molerat protocol",
        classifiers=[
            "License :: OSI Approved :: BSD License",

            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.11",

            "Topic :: Communications",
            "Topic :: Communications :: File Sharing",
            "Topic :: Internet",
            "Topic :: Software Development :: Libraries",
        ],
)
