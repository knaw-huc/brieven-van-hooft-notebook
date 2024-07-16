import marimo

__generated_with = "0.7.5"
app = marimo.App(width="medium", app_title="Brieven van Hooft - Notebook")


@app.cell
def __(mo):
    mo.md(
        """
        # Brieven van Hooft - Notebook

        ## Introduction

        This notebook provides access to the linguistic and socio-linguistic
        annotations that were added to the letters by P.C van Hooft in an annotation
        project in 2017 by Marjo van Koppen and Marijn Schraagen.

        The letters come from *"De briefwisseling van Pieter Corneliszoon Hooft, edited
        by H.W van Tricht e.a.,"*, as published by the DBNL in the following three
        parts:

        * [Part 1](https://www.dbnl.org/tekst/hoof001hwva02_01/)
        * [Part 2](https://www.dbnl.org/tekst/hoof001hwva03_01/)
        * [Part 3](https://www.dbnl.org/tekst/hoof001hwva04_01/)

        License information for these works can be found in
        [here](https://www.dbnl.org/titels/gebruiksvoorwaarden.php?id=hoof001hwva03).
        We did not receive the rights to publish the editorial parts of the texts that
        are not from the 17th century. They will still be available in this notebook as
        they can be downloaded from DBNL directly, but republishing them is not
        permitted unfortunately.

        The annotations were initially published in a combination of FoLiA XML and
        other stand-off formats. In 2024, they have been re-aligned with the original
        DBNL sources and published as a [STAM](https://annotation.github.io/stam) model.

        This notebook provides search and visualisation functionality on this STAM
        model. We will guide you through several examples. All code in this notebook
        can be executed, and if needed, modified to your liking.
        """
    )
    return


@app.cell
def __(mo):
    import os.path
    from urllib.request import urlretrieve

    if not os.path.exists("hoof001hwva02.txt"):
        urlretrieve("https://www.dbnl.org/nieuws/text.php?id=hoof001hwva02","hoof001hwva02.txt")
    if not os.path.exists("hoof001hwva03.txt"):
        urlretrieve("https://www.dbnl.org/nieuws/text.php?id=hoof001hwva03","hoof001hwva03.txt")
    if not os.path.exists("hoof001hwva04.txt"):
        urlretrieve("https://www.dbnl.org/nieuws/text.php?id=hoof001hwva04","hoof001hwva04.txt")
    if not os.path.exists("hoof001hwva.output.store.stam.json"):
        #TODO: adapt link to Zenodo before final publication
        urlretrieve("https://download.anaproy.nl/hoof001hwva.output.store.stam.json","hoof001hwva.output.store.stam.json")
    data_downloaded = "✅"

    mo.md(f"""### Obtaining the data

    We first obtain the data by downloading the original texts of the three books
    from DBNL, and by downloading the STAM model from Zenodo. The latter may take a
    while, please wait until it reports being done:

    * Data download ready? {data_downloaded}
    """)
    return data_downloaded, os, urlretrieve


@app.cell
def __(data_downloaded, mo, stam):
    if data_downloaded:
        #load the STAM model (AnnotationStore) into the variable `store`
        store = stam.AnnotationStore(file="hoof001hwva.output.store.stam.json")
        data_loaded = "✅"

    mo.md(f"""
    Next we load the data into memory, this too may take a while:

    * Data loaded? {data_loaded}""")
    return data_loaded, store


@app.cell
def __(mo):
    mo.md(
        """
        ## Data exploration

        ### Vocabularies

        Before we get to the actual texts and annotations, we first want to give some
        insight into the vocabularies that are used in this project. Understanding and
        exploring the vocabularies is important to be able to make sensible queries
        later on.

        Vocabularies used by the annotations are grouped into so-called **annotation data
        sets**, within these sets, **keys** are defined. Notable keys in this project are the following:

        | Set | Key	| Explanation |
        | --- | --- | ----------- |
        | `https://w3id.org/folia/v2/` | `elementtype` | Indicates the type of FoLiA element of this annotation (e.g. `s` (sentence), `w`(word), `pos`, `lemma`) | 
        | `gustave-pos` | `class` | The Part-of-Speech tag, manually assigned by the annotator, according to the CGN tagset and an extension thereof |
        | `gustave-lemma` |	`class` | The lemma, manually assigned by the annotator |
        | `http://ilk.uvt.nl/folia/sets/frog-mbpos-cgn`	| `class` | The Part-of-Speech tag, automatically annotated by Frog, according to the CGN tagset |
        | `http://ilk.uvt.nl/folia/sets/frog-mblem-nl` | `class` | The lemma, automatically annotated by Frog |
        | `https://w3id.org/folia/v2/` | `confidence` | The confidence value that was assigned to the annotation (a value between 0 and 1, occurs with automatic annotations by Frog) | 
        | `brieven-van-hooft-metadata` |  `dbnl_id` | The full letter identifier as assigned by the DBNL. You will find this key and others in this set on annotations of letters as a whole. |
        | `brieven-van-hooft-metadata` |  `dated` | The date of a letter |
        | `brieven-van-hooft-metadata` |  `recipient` | The name of the recipient of a letter |
        | `brieven-van-hooft-metadata` |  `letter_id` | The letter sequence number (not necessarily entirely numerical) |
        | `brieven-van-hooft-metadata` |  `invididual` | `True` if the recipient is an individual, `False` if it's an organization or group  |
        | `brieven-van-hooft-metadata` |  `gender` | The gender of the recipient: `male` or `female` (not much space for gender fluidity in the 17th century) |
        | `brieven-van-hooft-metadata` |  `function` | Occupation of the recipient, type of organisation of the recipient or type of personal relation to the recipient. Free value. |
        | `brieven-van-hooft-metadata` |  `literary` | `True` if the recipient is a literary author, `False` otherwise |
        | `brieven-van-hooft-categories` |  `function` | Function of the letter (closed vocabulary). You will find this key and others in this set on annotations of letters as a whole. |
        | `brieven-van-hooft-categories` |  `topic` | Topic of the letter (closed vocabulary) |
        | `brieven-van-hooft-categories` |  `business` | `True` if it's a business letter, `False` if it's a personal letter |
        | `brieven-van-hooft-categories` |  `accompanying` | `True` if it's an accompanying letter, `False` if it's an independent letter |
        | `brieven-van-hooft-categories` |  `part` | This key is found on annotations that identifies *parts* of letters, values are a closed vocabulary containing `greeting`, `opening`, `narratio`, `closing`, `finalgreeting` |
        """
    )
    return


@app.cell
def __(mo, store):
    available_datasets = [ x.id() for x in store.datasets() ]
    chosen_dataset = mo.ui.dropdown(options=sorted(available_datasets), value="brieven-van-hooft-metadata", label="Annotation Dataset:")

    mo.md(f"""
    ### Exploring vocabularies

    You can choose an annotation dataset to explore possible keys and values therein: 

    * {chosen_dataset}
    """)
    return available_datasets, chosen_dataset


@app.cell
def __(chosen_dataset, mo, store):
    dataset = store.dataset(chosen_dataset.value)
    available_keys = [x.id() for x in dataset.keys() ]
    chosen_key = mo.ui.dropdown(options=sorted(available_keys),label="Datakey:",value=available_keys[0])

    mo.md(f"""
    * {chosen_key}
    """)
    return available_keys, chosen_key, dataset


@app.cell
def __(chosen_key, dataset, natsorted, polars):
    key = dataset.key(chosen_key.value)
    vocab_dataframe = polars.DataFrame(
        data=natsorted((str(x), x.annotations_len()) for x in key.data()),
        schema=["Value","Occurrences"],
        orient="row"
    )
    vocab_dataframe
    return key, vocab_dataframe


@app.cell
def __(mo, natsorted, store):
    dataset_metadata = store.dataset("brieven-van-hooft-metadata")
    key_letter_id = dataset_metadata.key("letter_id")
    available_letters = natsorted(str(x) for x in key_letter_id.data())
    chosen_letter = mo.ui.dropdown(options=available_letters)
    show_pos_annotations = mo.ui.checkbox()
    show_lemma_annotations = mo.ui.checkbox()
    show_part_annotations = mo.ui.checkbox()


    mo.md(f"""
    ### Visualising Letters

    * Select a letter to visualise: {chosen_letter}
    * Show part-of-speech annotations? {show_pos_annotations}
    * Show lemma annotations? {show_lemma_annotations}
    * Show part annotations? {show_part_annotations}

    """)
    return (
        available_letters,
        chosen_letter,
        dataset_metadata,
        key_letter_id,
        show_lemma_annotations,
        show_part_annotations,
        show_pos_annotations,
    )


@app.cell
def __(
    chosen_letter,
    mo,
    show_lemma_annotations,
    show_part_annotations,
    show_pos_annotations,
    store,
):
    _query = f"""SELECT ANNOTATION ?letter WHERE DATA "brieven-van-hooft-metadata" "letter_id" = "{chosen_letter.value}";"""
    _highlights = []
    if show_pos_annotations.value:
        _highlights.append("""@VALUETAG SELECT ANNOTATION ?pos WHERE RELATION ?letter EMBEDS; DATA "gustave-pos" "class";""")
    if show_lemma_annotations.value:
        _highlights.append("""@VALUETAG SELECT ANNOTATION ?lemma WHERE RELATION ?letter EMBEDS; DATA "gustave-lem" "class";""")
    if show_part_annotations.value:
        _highlights.append("""@VALUETAG SELECT ANNOTATION ?part WHERE RELATION ?letter EMBEDS; DATA "brieven-van-hooft-categories" "part";""")
    _html = store.view(_query, *_highlights)
    mo.Html(_html)
    return


@app.cell
def __():
    #these are the main imports
    import marimo as mo
    import polars
    from natsort import natsorted
    import stam
    return mo, natsorted, polars, stam


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
