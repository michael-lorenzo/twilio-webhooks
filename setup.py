import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twilio-webhooks",
    version="0.1.0",
    author="Michael Lorenzo",
    author_email="python@michael-lorenzo.com",
    description="A collection of webhooks for Twilio using Flask.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michael-lorenzo/twilio-webhooks",
    packages=setuptools.find_packages(),
    install_requires=["flask", "twilio"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
