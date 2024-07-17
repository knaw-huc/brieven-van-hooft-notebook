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
def __():
    #these are the main imports
    import marimo as mo
    import polars
    from natsort import natsorted
    import stam

    import os.path
    from urllib.request import urlretrieve

    #download the data
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
    return data_downloaded, mo, natsorted, os, polars, stam, urlretrieve


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
    # present a form to explore vocabularies

    available_datasets = [ x.id() for x in store.datasets() ]
    chosen_dataset = mo.ui.dropdown(options=sorted(available_datasets), value="brieven-van-hooft-metadata", label="Annotation Dataset:")

    mo.md(f"""
    ### Exploring vocabularies

    Explore keys and values in a vocabulary:

    * {chosen_dataset}
    """)
    return available_datasets, chosen_dataset


@app.cell
def __(chosen_dataset, mo, store):
    # present datakeys based on selected dataset

    dataset = store.dataset(chosen_dataset.value)
    available_keys = [x.id() for x in dataset.keys() ]
    chosen_key = mo.ui.dropdown(options=sorted(available_keys),label="Datakey:",value=available_keys[0])

    mo.md(f"""
    * {chosen_key}
    """)
    return available_keys, chosen_key, dataset


@app.cell
def __(store):
    # initialize some data we need later
    dataset_metadata = store.dataset("brieven-van-hooft-metadata")
    key_letter_id = dataset_metadata.key("letter_id")
    return dataset_metadata, key_letter_id


@app.cell
def __(chosen_key, dataset, mo, natsorted, polars):
    # show the data for the selected data key
    key = dataset.key(chosen_key.value)
    vocab_dataframe = polars.DataFrame(
        data=natsorted((str(x), x.annotations_len()) for x in key.data()),
        schema=["Value","Occurrences"],
        orient="row"
    )
    vocab_selection = mo.ui.table(vocab_dataframe, selection="multi")
    vocab_selection
    return key, vocab_dataframe, vocab_selection


@app.cell
def __(
    chosen_dataset,
    chosen_key,
    key_letter_id,
    mo,
    natsorted,
    polars,
    store,
    vocab_selection,
):
    #Find letters given selected data

    data_values = "|".join([f"\"{str(x[0])}\"" for x in vocab_selection.value.select(polars.selectors.first()).iter_rows()])
    data_query = f"""SELECT ANNOTATION ?a WHERE DATA "{chosen_dataset.value}" "{chosen_key.value}" = {data_values};"""
    matching_letters = []
    for result in store.query(data_query):
        if result["a"].test_data(key_letter_id):
            matching_letters.append(next(result["a"].data(key_letter_id)))

    if matching_letters:
        matching_letters_md = "\n".join(natsorted(f"* ``{str(x)}``" for x in matching_letters))
        _r = mo.md(f"""The following letters match your query (``{data_query}``): 

    {matching_letters_md}
    """)
    elif data_query and data_values:
        _r = mo.md(f"""There were no letters matching your query (``{data_query}``)""")
    else:
        _r = mo.md(f"""(no data query done)""")
    _r        
    return (
        data_query,
        data_values,
        matching_letters,
        matching_letters_md,
        result,
    )


@app.cell
def __(key_letter_id, mo, natsorted):
    #this cell presents a form to view letters and annotations

    available_letters = natsorted(str(x) for x in key_letter_id.data())
    chosen_letter = mo.ui.dropdown(options=available_letters)
    show_pos_annotations = mo.ui.checkbox()
    show_lemma_annotations = mo.ui.checkbox()
    show_part_annotations = mo.ui.checkbox()
    show_structure_annotations = mo.ui.checkbox()


    mo.md(f"""
    ## Visualisation of Letters and Annotations

    * Select a letter to visualise: {chosen_letter}
    * Show part-of-speech annotations? {show_pos_annotations}
    * Show lemma annotations? {show_lemma_annotations}
    * Show part annotations? {show_part_annotations}
    * Show structure annotations from FoLiA? {show_structure_annotations}

    """)
    return (
        available_letters,
        chosen_letter,
        show_lemma_annotations,
        show_part_annotations,
        show_pos_annotations,
        show_structure_annotations,
    )


@app.cell
def __(
    chosen_letter,
    mo,
    show_lemma_annotations,
    show_part_annotations,
    show_pos_annotations,
    show_structure_annotations,
    store,
):
    #this cell forms and runs query for letter visualisation and display the results

    query = f"""SELECT ANNOTATION ?letter WHERE DATA "brieven-van-hooft-metadata" "letter_id" = "{chosen_letter.value}";"""
    _highlights = []
    if show_pos_annotations.value:
        _highlights.append("""@VALUETAG SELECT ANNOTATION ?pos WHERE RELATION ?letter EMBEDS; DATA "gustave-pos" "class";""")
    if show_lemma_annotations.value:
        _highlights.append("""@VALUETAG SELECT ANNOTATION ?lemma WHERE RELATION ?letter EMBEDS; DATA "gustave-lem" "class";""")
    if show_part_annotations.value:
        _highlights.append("""@VALUETAG SELECT ANNOTATION ?part WHERE RELATION ?letter EMBEDS; DATA "brieven-van-hooft-categories" "part";""")
    if show_structure_annotations.value:
        _highlights.append("""@VALUETAG SELECT ANNOTATION ?w WHERE RELATION ?letter EMBEDS; DATA "https://w3id.org/folia/v2/" "elementtype" = "w";""")
        _highlights.append("""@VALUETAG SELECT ANNOTATION ?p WHERE RELATION ?letter EMBEDS; DATA "https://w3id.org/folia/v2/" "elementtype" = "p";""")
        _highlights.append("""@VALUETAG SELECT ANNOTATION ?s WHERE RELATION ?letter EMBEDS; DATA "https://w3id.org/folia/v2/" "elementtype" = "s";""")    

    _html = store.view(query, *_highlights)
    highlights_md = "".join(f"* ``{hq}``\n" for hq in _highlights)
    mo.Html(_html)
    return highlights_md, query


@app.cell
def __(highlights_md, mo, query):
    mo.md(f"""

        The following selection query and (optionally) highlight queries were used to render the above visualisation:
        
        * ``{query}``
        {highlights_md}
    """)
    return


@app.cell
def __(mo):
    #this cell produces the custom query form

    queryform = mo.ui.text_area(label="Enter a selection query and zero or more highlight queries, each separated by an empty line. Use STAMQL syntax:",full_width=True).form()

    mo.md(f"""
    ## Custom Queries

    {queryform}
    """)

    return queryform,


@app.cell
def __(mo, queryform, store):
    #this cell runs the custom query and presents the results

    if queryform.value:
        custom_queries = [ x for x in queryform.value.split("\n\n") if x.strip() ]
        _html = store.view(custom_queries[0], *custom_queries[1:])
        if _html.find("<h2>") == -1:
            _html = "(query did no produce any results)"
    else:
        _html = "(no query submitted)"
    mo.Html(_html)
    return custom_queries,


if __name__ == "__main__":
    app.run()
