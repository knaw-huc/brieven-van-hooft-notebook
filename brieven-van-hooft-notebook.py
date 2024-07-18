import marimo

__generated_with = "0.7.7"
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
        You can also inspect the full [pipeline that produced this
        model](https://github.com/knaw-huc/brieven-van-hooft-pipeline).

        This notebook provides search and visualisation functionality on this STAM
        model. We will guide you through several examples. All code in this notebook
        can be executed, and if needed, modified to your liking.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(f"""### Obtaining the data

    We first obtain the data by downloading the original texts of the three books
    from DBNL, and by downloading the STAM model from Zenodo. Then will will load the data into memory. All this may take a
    while. Please wait until both these tasks are marked as done below:
    """)
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

    mo.md(f"* Data download ready? {data_downloaded}")
    return data_downloaded, mo, natsorted, os, polars, stam, urlretrieve


@app.cell
def __(data_downloaded, mo, stam):
    if data_downloaded:
        #load the STAM model (AnnotationStore) into the variable `store`
        store = stam.AnnotationStore(file="hoof001hwva.output.store.stam.json")
        data_loaded = "✅"

    mo.md(f"* Data loaded? {data_loaded}")
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
        | `gustave-pos` | `class` | The Part-of-Speech tag, manually assigned by the annotator, according to the CGN tagset and an extension thereof. This contains the full tag along with all its features. If you only want the tag head, use key `head` instead. If you want a specific feature use the key pertaining to the feature (e.g. `gender` or `number`) |
        | `gustave-lemma` |	`class` | The lemma, manually assigned by the annotator |
        | `http://ilk.uvt.nl/folia/sets/frog-mbpos-cgn`	| `class` | The Part-of-Speech tag, automatically annotated by Frog, according to the CGN tagset |
        | `http://ilk.uvt.nl/folia/sets/frog-mblem-nl` | `class` | The lemma, automatically annotated by Frog |
        | `https://w3id.org/folia/v2/` | `confidence` | The confidence value that was assigned to the annotation (a value between 0 and 1, occurs with automatic annotations by Frog) | 
        | `brieven-van-hooft-metadata` |  `dbnl_id` | The full letter identifier as assigned by the DBNL. It is the primary means of identifying a particular letter. You will find this key and others in this set on annotations of letters as a whole. |
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

    You can explore the keys and values in a vocabulary. If you select any values here, they will be used to constrain the letters shown in the next section.

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
    key_dbnl_id = dataset_metadata.key("dbnl_id")
    return dataset_metadata, key_dbnl_id


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
    key_dbnl_id,
    mo,
    polars,
    store,
    vocab_selection,
):
    #constrain letters given selected data

    data_values = "|".join([str(x[0]) for x in vocab_selection.value.select(polars.selectors.first()).iter_rows()])
    data_query = f"""SELECT ANNOTATION ?a WHERE DATA "{chosen_dataset.value}" "{chosen_key.value}" = "{data_values}";"""
    matching_letters = []
    for _annotation in store.query(data_query):
        if _annotation["a"].test_data(key_dbnl_id):
            matching_letters.append(next(_annotation["a"].data(key_dbnl_id)))
        #else:
        #    for _letter in _annotation["a"].related_text(stam.TextSelectionOperator.embedded(), limit=5).annotations(key_dbnl_id):
        #        _dbnl_id = next(_letter.data(key_dbnl_id))
        #        if _dbnl_id not in matching_letters:
        #            matching_letters.append(_dbnl_id)

    if matching_letters:
        _md = mo.md(f"{len(matching_letters)} matching letters were found (query was: ``{data_query}``), the selection below is constrained accordingly:" )
    else:
        _md = mo.md(f"No matching letters found (query was ``{data_query}``)")
    _md
    return data_query, data_values, matching_letters


@app.cell
def __(key_dbnl_id, matching_letters, mo, natsorted, polars):
    #this cell presents a form to view letters and annotations

    if matching_letters:
        available_letters = polars.DataFrame(
            data=natsorted((str(x) for x in matching_letters)),
            schema=["dbnl_id"],
            orient="row"
        )
        letter_note = "*(this selection is constrained by your data query above!)*"
    else:
        available_letters = polars.DataFrame(
            data=natsorted(str(x) for x in key_dbnl_id.data()),
            schema=["dbnl_id"],
            orient="row"
        )
        letter_note = ""
    chosen_letters = mo.ui.table(available_letters,selection="multi")
    show_pos_annotations = mo.ui.checkbox()
    show_lemma_annotations = mo.ui.checkbox()
    show_part_annotations = mo.ui.checkbox()
    show_structure_annotations = mo.ui.checkbox()


    mo.md(f"""
    ## Visualisation of Letters and Annotations

    * Select one or more letters to visualise: {letter_note} {chosen_letters}
    * Show part-of-speech annotations? {show_pos_annotations}
    * Show lemma annotations? {show_lemma_annotations}
    * Show part annotations? {show_part_annotations}
    * Show structure annotations from FoLiA? {show_structure_annotations}

    """)
    return (
        available_letters,
        chosen_letters,
        letter_note,
        show_lemma_annotations,
        show_part_annotations,
        show_pos_annotations,
        show_structure_annotations,
    )


@app.cell
def __(
    chosen_letters,
    mo,
    polars,
    show_lemma_annotations,
    show_part_annotations,
    show_pos_annotations,
    show_structure_annotations,
    store,
):
    #this cell forms and runs query for letter visualisation and display the results
    if not chosen_letters.value.is_empty():
        _chosen_letters = "|".join(chosen_letters.value.to_series())
        query = f"""SELECT ANNOTATION ?letter WHERE DATA "brieven-van-hooft-metadata" "dbnl_id" = "{_chosen_letters}";"""
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
        for _letter in store.query(query):
            letter_metadata = polars.DataFrame(((x.dataset().id(), x.key().id(), str(x)) for x in _letter["letter"].data()), schema=["Dataset","Key", "Value"],orient="row")
            break
    else:
        _html = "(no letters selected)"
        query = "(no query provided)"
        letter_metadata = polars.DataFrame()
        highlights_md = ""
    mo.Html(_html)
    return highlights_md, letter_metadata, query


@app.cell
def __(highlights_md, mo, query):
    mo.md(f"""

        The following selection query and (optionally) highlight queries were used to render the above visualisation:

        * ``{query}``
        {highlights_md}

        The table below shows all the metadata that was associated with the first selected letter:   
    """)
    return


@app.cell
def __(letter_metadata):
    letter_metadata
    return


@app.cell
def __(mo):
    #this cell produces the custom query form

    queryform = mo.ui.text_area(label="Enter a selection query and zero or more highlight queries, each separated by an empty line. Use STAMQL syntax:",full_width=True, rows=25).form()

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
            _html = "(custom query did no produce any results)"
    else:
        _html = "(no custom query submitted)"
    mo.Html(_html)
    return custom_queries,


@app.cell
def __(custom_queries, mo):
    _custom_queries_md = "\n".join((f"* `{q}`" for q in custom_queries))
    mo.md(f"""
    The following custom selection query and (optionally) highlight queries were used to render the above visualisation:

    {_custom_queries_md}
    """)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Custom Query Examples

        You can copy these example queries to the custom query input and run them:

        ### Metadata search

        Show all letters to recipients born prior to 1600:

        ```
        SELECT ANNOTATION ?letter WHERE
            DATA "brieven-van-hooft-metadata" "dbnl_id";
            DATA "brieven-van-hooft-metadata" "birthyear" < 1600;
        ```

        ### Display a specific letter and highlight specific Part-of-Speech tags

        ```
        SELECT ANNOTATION ?letter WHERE
            DATA "brieven-van-hooft-metadata" "dbnl_id" = "hoof001hwva02_01_0032";

        SELECT ANNOTATION ?adj WHERE
            RELATION ?letter EMBEDS;
            DATA "gustave-pos" "head" = "ADJ";

        SELECT ANNOTATION ?adv WHERE
            RELATION ?letter EMBEDS;
            DATA "gustave-pos" "head" = "BIJW";   

        ```


        ### Search for words with a specific text and part-of-Speech tag

        In letters, search for words with a specific text that also have a specific PoS tag:

        ```
        SELECT ANNOTATION ?letter WHERE
            DATA "brieven-van-hooft-metadata" "dbnl_id";
        {
          SELECT ANNOTATION ?w WHERE
            RELATION ?letter EMBEDS;
            DATA "https://w3id.org/folia/v2/" "elementtype" = "w";
            TEXT "Naerden";
          {
            SELECT ANNOTATION ?pos WHERE
                RELATION ?w EQUALS;
                DATA "gustave-pos" "head" = "N";
           }  
        }
        ```

        Alternative (TODO: DEBUG!):

        ```
        SELECT ANNOTATION ?letter WHERE
            DATA "brieven-van-hooft-metadata" "dbnl_id";
        {
          SELECT TEXT ?w WHERE
            RELATION ?letter EMBEDS;
            TEXT "Naerden";
            DATA "https://w3id.org/folia/v2/" "elementtype" = "w";
            DATA "gustave-pos" "head" = "N";      
        }
        ```
        """
    )
    return


if __name__ == "__main__":
    app.run()
