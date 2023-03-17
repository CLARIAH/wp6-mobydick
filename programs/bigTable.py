import os
import pandas as pd
from tf.app import use


def makeTable():
    A = use("CLARIAH/wp6-ferdinandhuyck:clone", checkout="clone")
    api = A.api
    Fall = api.Fall
    Fs = api.Fs
    F = api.F
    N = api.N
    L = api.L

    TEMP_DIR = os.path.abspath("../_temp")
    RESULT_DIR = os.path.abspath("../pandas")
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)

    TABLE_FILE = f"{TEMP_DIR}/data-{A.version}.tsv"
    TABLE_FILE_PD = f"{RESULT_DIR}/data-{A.version}.pd"

    TEXT_FEATURES = ("str", "after")
    FEATURES = sorted(set(Fall()) - {"otype", "oslots"} - set(TEXT_FEATURES))
    LEVEL_TYPES = ("chapter", "chunk")

    INT = "Int64"
    STR = "str"

    dtype = dict(nd=INT, element=STR)
    for f in TEXT_FEATURES:
        dtype[f] = STR
    for f in LEVEL_TYPES:
        dtype[f"in.{f}"] = INT
    for f in FEATURES:
        if f.startswith("empty_"):
            parts = f.split("_", 2)
            tp = INT if len(parts) == 2 else STR
            dtype[f] = tp
        elif f.startswith("is_") or f.startswith("rend_") or f == "chunk":
            dtype[f] = INT
        else:
            dtype[f] = STR

    naValues = dict((x, set() if dtype[x] == STR else {""}) for x in dtype)

    with open(TABLE_FILE, "w") as hr:
        hr.write(
            "{}\t{}\t{}\t{}\t{}\n".format(
                "nd",
                "element",
                "\t".join(TEXT_FEATURES),
                "\t".join(f"in.{x}" for x in LEVEL_TYPES),
                "\t".join(FEATURES),
            )
        )
        chunkSize = 10000
        i = 0
        s = 0
        NA = [""]
        CHAPTER = "chapter"
        CHUNK = "chunk"

        for n in N.walk():
            textValues = [str(Fs(f).v(n) or "") for f in TEXT_FEATURES]
            levelValues = [(L.u(n, otype=level) or NA)[0] for level in LEVEL_TYPES]
            nodeValues = [
                (
                    F.chapter.v(L.u(n, otype="chapter")[0])
                    if f == CHAPTER and F.otype.v(n) == CHUNK
                    else str(Fs(f).v(n) or "")
                )
                for f in FEATURES
            ]
            hr.write(
                "{}\t{}\t{}\t{}\t{}\n".format(
                    n,
                    F.otype.v(n),
                    ("\t".join(textValues)).replace("\n", "\\n"),
                    ("\t".join(str(x) for x in levelValues)),
                    ("\t".join(nodeValues)),
                )
            )
            i += 1
            s += 1
            if s == chunkSize:
                s = 0
                A.info("{:>7} nodes written".format(i))

    A.info("{:>7} nodes written and done".format(i))

    with open(TABLE_FILE, "r") as hr:
        for (i, line) in enumerate(hr):
            if i > 10:
                break
            print(line)

    A.info("Importing into Pandas ...")

    dataFrame = pd.read_table(
        TABLE_FILE,
        delimiter="\t",
        low_memory=False,
        encoding="utf8",
        keep_default_na=False,
        na_values=naValues,
        dtype=dtype,
        #    index_col='n',
    )
    A.info("Done. Size = {}".format(dataFrame.size))
    A.info("Saving as Parquet file ...")
    dataFrame.to_parquet(TABLE_FILE_PD, engine="pyarrow")
    A.info("Done")


if __name__ == "__main__":
    makeTable()
