
# Corpus annotation - mobydick

## How a TF dataset represents a corpus

A TF dataset contains: 

*   textual objects as a set of nodes;
*   textual positions as a range of slots, which are also nodes;
*   nodes are represented as numbers;
*   nodes are divided in types, which have a name;
*   non-slot nodes are linked to slots;
*   all data about textual positions and objects are in features,
    which map nodes to values;
*   features have a name, and each feature is stored in a separate file with that name;
*   in particular, the text itself is stored in one or more features;
*   there are a few standard features that are present in every TF dataset;
*   See the
    [Text-Fabric data model](https://annotation.github.io/text-fabric/tf/about/datamodel.html).

In this dataset, **tokens** fulfill the role of slots.

## How TEI maps to TF

*   Text-Fabric *token nodes* correspond to **tokens** in TEI element content;
*   Text-Fabric *node types* correspond to TEI *element names (tags)*;
*   Text-Fabric *non-token nodes* correspond to TEI *elements in the source*;
*   Text-Fabric *features* correspond to TEI *attributes*;
*   Text-Fabric *edges* correspond to *relationships* between TEI elements;


*   Here are the [TEI elements and attributes](elements.md) used in this corpus.

*   Text-Fabric *node types* that start with a `?` correspond to TEI processing 
    instruction with that node type as target. The attributes of the processing
    instruction translate to TF features. As to the link to slots: it is
    treated as if it were an empty element.


*   Processing instructions in the TEI are ignored and do not leave any trace in the
    TF data.



The conversion may invoke custom code which may generate extra features.
For these features, metadata may have been declared, and it will show in the
generated documentation.


Tokens and sentence boundaries have been generated by a Natural Language
Pipeline, such as Spacy.


The TEI to TF conversion is an almost literal and very faithful transformation from
the TEI source files to a Text-Fabric data set.

## TF nodes and features overview

(only in as far they are not in 1-1 correspondence with TEI elements and attributes)





### node type `chapter`

*The type of chapters in a TEI document.*

**Section level 1**

**Features**

feature | description
--- | ---
`chapter` | heading of the chapter



### node type `chunk`




*paragraph-like division.*


**Section level 2**

**Features**





feature | description
--- | ---
`chunk` | sequence number of the chunk within the chapter, positive for `<p>` chunks, negative for other chunks.




### node type `sentence`

*Sentences, i.e. material between full stops and several other punctuation marks*.

feature | description
--- | ---
`nsent` | the sequence number of the sentence within the corpus



### node type `token`

*Individual tokens, without space or punctuation.*



**Slot type.**


**Features**

feature | description
--- | ---
`str` | the characters of the token, without soft hyphens.
`after` | the space after the word, if present, otherwise the empty string.
`is_meta` | whether a token is in the `teiHeader` element
`is_note` | whether a token is in a note element
`rend_r` | whether a token is under the influence of a `rend="r"` attribute.



## Edge features

feature | description
--- | ---

Note that edges can be traversed in both directions, see the
[docs](https://annotation.github.io/text-fabric/tf/core/edgefeature.html).





## Extra features





The conversion has not generated extra features by means of custom code.


## Sectioning

The material is divided into 2 levels of sections, mainly for the purposes
of text display.

But how these levels relate to the source material is a different matter.

The conversion supports a few sectioning models that specify this.
This aspect is *work-in-progress*, because TEI sources differ wildly in how they
are sectioned.
The sectioning models that are currently supported correspond to cases we have
encountered, we have not done exhaustive research into TEI sectioning in practice.

This corpus is converted with section **Model II**.





### Model II: single file and `div` elements.

This model assumes that the source is a single TEI file.

There are two section levels: 

*   *chapter* Top-level division, roughly corresponding to top-level `<div>` elements;
    heading: a sequence number and a tag name, or the contents of an heading-bearing element;
*   *chunk* division within the chapters, roughly corresponding to `<p>` elements.
    heading: sequence number of the chunk within a chapter; chunks that are `<p>` elements
    are numbered with positive numbers; other chunks are numbered separately with negative numbers.

All section headings are stored in a feature with the same name as the type of section:
*chapter*, *chunk*.

#### Details

1.  *chapter* nodes have been made as follows:

    *   `<teiHeader>` is a chapter;
    *   immediate children of `<text>` are chapters,
        except the *text structure* elements
        `<front>`, `<body>`, `<back>` and `<group>`;
    *   immediate children of the text structure elements are chapters;

1.  *chunk* nodes have been made as follows:

    *   the `<teiHeader>` is a chunk;
    *   immediate children of `<text>` are chunks,
        except the *text structure* elements
        `<front>`, `<body>`, `<back>` and `<group>`;
    *   immediate children of the text structure elements are chunks,
    *   but not necessarily empty elements such as `<lb/>` and `<pb/>`.

1.  the slots generated for empty elements are linked to the current chapter and chunk
    if there they exist; otherwise they will be linked to the upcoming chapter
    and chunk.
1.  The heading of a chapter is either the text in a heading-bearing element,
    or, if no such element is found, a sequence number and the tag name.
1.  Extra parameters specify how to find the head-bearing element for a chapter.
    This corpus is parametrized with

    ```
    {'element': 'head', 'levels': ['chapter', 'chunk'], 'attributes': {}}
    ```

    meaning:
    
    *   heads occur in `<head>` elements that follow the chapter-starting element;
        but only those ones that satisfy the following attribute properties, if any:

    	*	*no attribute properties*


1.  Additional remarks about heading bearing elements:
    1.  their original occurrences in the text are preserved and treated in the same
        way as all other elements;
    1.  only the plain text content of the headings are used for the chapter headings,
        markup inside headings is ignored for this purpose.






## Token detection

Tokens have been detected by an NLP pipeline.
The values of tokens are either words or non-word characters.
White space is not part of the token.
Whether a token is followed by a space or not is in the feature `after`.

## Sentence detection
Sentences have been detected by an NLP pipeline.
They form a new node type, `sentence`, with just a sequence number as feature (`nsent`).


## Tokens

Whether characters of words  or tokens are taken as the basic unit (*slot*) is decided
by the parameter `wordAsSlot`, passed to the conversion, and whether tokens have been
provided later on.
(for this corpus the slot type is **token**).

### Tokens and empty elements

When empty elements occur, something must be done to anchor them to the text stream.

To such elements we add an empty token with the ZERO-WIDTH-SPACE (Unicode 200B) as
character/string value.

Such slots get the feature `empty` assigned with value 1.

### Tokens in general

1.  Spaces are stripped when they are between elements whose parent does not allow
    mixed content; other white-space is reduced to a single space.
1.  However, after direct child elements of pure elements we add a single space
    or newline: if there is an ancestor with mixed content, we add a space;
    if the whole ancestry consists of pure elements (typically in the TEI header),
    we add a newline.
    
    
1.  All tokens inside the `teiHeader` will get the feature `is_meta` set to 1;
    for tokens inside the body, `is_meta` has no value.






## Text kinds and styled formatting

We record in additional features whether text occurs in metadata elements and
in note elements and what formatting specifiers influence the text.
These features are provided for `token` nodes, and have only one value: 1.
The absence of values means that the corresponding property does not hold.

The following features are added:

*   `is_meta`: 1 if the token occurs in inside the `<teiHeader>`, no
    value otherwise.
*   `is_note`: 1 if the token occurs in inside the `<note>`, no value otherwise.
*   `rend_r`: for any `r` that is the value of a `rend` attribute.

All these features are defined for `token` nodes.
For token nodes, the value of these features is set equal to what these features
are for their first character.

Special formatting for the `rend_r` features is supported for some values of `r`.
The conversion supports these out-of-the-box:

value | description
--- | ---
`above` | above the line
`b` | bold font weight
`below` | below the line
`bold` | bold font weight
`center` | horizontally centred text
`h1` | heading of level 1
`h2` | heading of level 2
`h3` | heading of level 3
`h4` | heading of level 4
`h5` | heading of level 5
`h6` | heading of level 6
`i` | cursive font style
`italic` | cursive font style
`italics` | cursive font style
`large` | large font size
`margin` | in the margin
`sc` | small-caps font variation
`small_caps` | small-caps font variation
`smallcaps` | small-caps font variation
`spaced` | widely spaced between characters
`spat` | widely spaced between characters
`sub` | as subscript
`sup` | as superscript
`super` | as superscript
`ul` | underlined text
`underline` | underlined text

It is possible for the corpus designer to add more formatting on a per-corpus
basis by adding it to the `display.css` in the app directory of the corpus.
Unsupported values get a generic kind of special format: an orange-like color.

Special formatting becomes visible when material is rendered in a `layout` text
format.

## Text formats

Text-formats regulate how text is displayed, and they can also determine
what text is displayed.

There are two kind of text-formats: those that start with the word `layout` and
those that start with `text`.

The `text` formats do not apply any kind of special formatting, the `layout` formats
do.

We have the following formats:

*   `text-orig-full`: all text
*   `layout-orig-full`: all text, formatted in HTML

## Boundary conditions

XML is complicated, the TEI guidelines use that complexity to the full.
In particular, it is difficult to determine what the set of TEI elements is
and what their properties are, just by looking at the schemas, because they are full
of macros, indirections, and abstractions, which can be overridden in any particular
TEI application.

On the other hand, the resulting TF should consist of clearly demarcated node types
and a simple list of features. In order to make that happen, we simplify matters
a bit.


1.  Processing instructions (`<?proc a="b">`) are treated as empty elements with as tag
    the *target* with preceding `?` and as attributes its pseudo attributes.


1.  Processing instructions (`<?proc a="b">`) are ignored.
1.  Comments (`<!-- this is a comment -->`) are ignored.
1.  Declarations (`<?xml ...>` `<?xml-model ...>` `<?xml-stylesheet ...>`) are
    read by the parser, but do not leave traces in the TF output.
1.  The attributes of the root-element (`<TEI>`) are ignored.
1.  Namespaces (`xmlns="http://www.tei-c.org/ns/1.0"`) are read by the parser,
    but only the unqualified names are distinguishable in the output as feature names.
    So if the input has elements `tei:abb` and `ns:abb`, we'll see just the node
    type `abb` in the output.

### Validation

We have used [LXML](https://lxml.de) for XML parsing. During `convert` it is not used
in validating mode, but we can trigger a validation step during `check`.

However, some information about the elements, in particular whether they allow
mixed content or not, has been gleaned from the schemas, and has been used
during conversion.

Care has been taken that the names of these extra nodes and features do not collide
with element/attribute names of the TEI.


## See also

*   [about](about.md)



