import os
from tf.convert.tei import TEI


AUTHOR = "Herman Melville"
TITLE = "Moby Dick"
INSTITUTE = "Oxford Text Archive"
SOURCE = "DBNL"
SOURCE_URL = "https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/3049"

SECTION_MODEL = dict(
    model="II",
    element="head",
)
GENERIC = dict(
    author=AUTHOR,
    title=TITLE,
    institute=INSTITUTE,
    language="en",
    dateWritten="1851",
    source=SOURCE,
    sourceUrl=SOURCE_URL,
    converters="Dirk Roorda (Text-Fabric)",
    sourceFormat="TEI",
    descriptionTf=(
        "Originally transcribed and deposited by Prof. Eugene F. Irey, "
        "University of Colorado"
    ),
    license="CC-BY-SA 3.0",
    licenseUrl="https://creativecommons.org/licenses/by-sa/3.0/",
)

APP_CONFIG = dict(
    provenanceSpec=dict(
        doi="10.5281/zenodo.nnnnnn",
    )
)

ABOUT_TEXT = """
# Description

This is the novel
[Moby Dick](https://en.wikipedia.org/wiki/Moby-Dick)
written by
[Herman Melville, 1819-1891](https://en.wikipedia.org/wiki/Herman_Melville)
in 1851.

# Source

Cite the source as
[Melville, Herman, 1819-1891, Moby Dick, Oxford Text Archive](http://hdl.handle.net/20.500.12024/3049.).

The url of this link is a persistent (handle) identifier.

# Copyright

Distributed by the University of Oxford under a
[Creative Commons Attribution-ShareAlike 3.0 Unported License](https://creativecommons.org/licenses/by-sa/3.0/).
"""

TRANSCRIPTION_TEXT = """

The conversion to TEI is done with sectioning model II.
"""

DOC_MATERIAL = dict(
    about=ABOUT_TEXT,
    transcription=TRANSCRIPTION_TEXT,
)


def transform(text):
    return text


T = TEI(
    schema=None,
    sourceVersion="2019-07-04",
    testSet=None,
    wordAsSlot=True,
    sectionModel=SECTION_MODEL,
    generic=GENERIC,
    transform=transform,
    tfVersion="0.1",
    appConfig=APP_CONFIG,
    docMaterial=DOC_MATERIAL,
    force=False,
)

T.run(os.path.basename(__file__))
