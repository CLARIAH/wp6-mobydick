
# Corpus CLARIAH - wp6-mobydick

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
    [Text-Fabric datamodel](https://annotation.github.io/text-fabric/tf/about/datamodel.html).

In this dataset, **words** fullfill the role of slots.

## How TEI maps to TF

*   Text-Fabric word nodes correspond to **words** in TEI element content;
*   Text-Fabric node types correspond to TEI element names (tags);
*   Text-Fabric non-word nodes correspond to TEI elements in the source;
*   Text-Fabric *features* correspond to TEI *attributes*;
*   Here are the [TEI elements and attributes](elements.md) used in this corpus.

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



### node type `word`

*Individual words, without punctuation.*


**Slot type.**


**Features**

feature | description
--- | ---
`str` | the characters of the word, without soft hyphens.
`after` | the non-word characters after the word, up till the next word.
`is_meta` | whether a word is in the teiHeader element
`is_note` | whether a word is in a note element
`rend_`*r* | whether a word is under the influence of a `rend="`*r*`"` attribute.



### Additional features

Empty words may have been inserted to mark the place of empty elements.
Or empty elements may have left features on preceding words.

feature | description
--- | ---
`empty` | whether a word has been inserted in an empty element
`empty_`*element* | whether there is a following empty *element*
`empty_`*element*`_`*attribute* | the value of *attribute* of the following empty *element*


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





### Model II: single file and divs.

This model assumes that the source is a single TEI file.

There are two section levels: 

*   *chapter* Top-level division, roughly corresponding to top-level `<div>` elements;
    heading: a sequence number and a tag name, or the contents of an heading-bearing element;
*   *chunk* division withint the chapters, roughly corresponding to `<p>` elements.
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

1.  The heading of a chapter is either the text in a heading-bearing element,
    or, if no such element is found, a sequence number and the tag name.
1.  Extra parameters specify how to find the head-bearing element for a chapter.
    This corpus is parametrized with

    ```
    {'element': 'head', 'attributes': {}}
    ```

    meaning:
    
    *   heads occur in `<head>` elements that follow the chapter-starting element;
        but only those ones that satisfy the following attribute criteria, if any:

    	*	*no attribute criteria*


1.  Additional remarks about heading bearing elements:
    1.  their original occurrences in the text are preserved and treated in the same
        way as all other elements;
    1.  only the plain text content of the headings are used for the chapter headings,
        markup inside headings is ignored for this purpose.



## Word detection

Words will be detected. They are maximally long sequences of alphanumeric characters
and hyphens.

1.  What is alphanumeric is determined by the unicode class of the character,
    see the Python documentation of the function
    [`isalnum()`](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)
1.  Hyphens are Unicode characters 002D (ascii hyphen) and 2010 (unicode hyphen).
1.  Words get the following features:
    *   `str`: the alphanumeric string that is the word;
    *   `after`: the non-alphanumeric string after the word unti the following word.

## Words

Whether characters of words are taken as the basic unit (*slot*) is decided
by the parameter `wordAsSlot`, passed to the conversion
(for this corpus the slot type is **word**).

### Words and empty elements

When empty elements occur, something must be done to anchor them to the text stream.

*   *accidentally empty*:
    When the element is empty, but could have had content, we add an empty word, with
    features derived from the attributes of the element.
    This empty word also gets the ZERO-WIDTH-SPACE (Unicode 200B) as character value.
*   *necessarily empty*:
    When the element can never have content (as defined by the TEI guidelines), we add
    its attributes as features to the previous word (if there is no such word,
    we make an empty word).
    We also add a feature `empty_`*tag*`=1` on that word; *tag* is the name of the
    empty element. All attributes of such an element go into features
    `empty_`*tag*`_`*att*`=`*value* on the same word.

### Words in general

1.  Spaces are stripped when they are between elements whose parent does not allow
    mixed content; other whitespace is reduced to a single space.
1.  All words inside the teiHeader will get the feature `is_meta` set to 1;
    for words inside the body, `is_meta` has no value.





## More about words

The basic unit is the word, as detected by the rules above.

1.  *word* nodes get these defining features:
    *   `str`: the string of the word
    *   `after`: interword material after the word

1. Nodes that contain only part of the characters of a word, will contain the whole
   word.
1. Features that have different values for different characters in the word,
   will have the last value encountered for the whole word.
1. Formatting attributes, such as `rend=italic` (see below) will give rise
   to features `r_italic`. If a word is embedded in severel elements with
   `rend` attributes and different values for them, the word will get
   features `r_`*value* for all those values. But if different parts of the
   word are in the scope of different `rend` values, that information will be lost,
   the `r_`*value* features all apply the whole word.



## Text kinds and styled formatting

We record in additional features whether text occurs in metadata elements and
in note elements and what formatting specifiers influence the text.
These features are provided for `word` nodes, and have only one value: 1.
The absence of values means that the corresponding property does not hold.

The following features are added:

*   `is_meta`: 1 if the word occurs in inside the `<teiHeader>`, no value otherwise.
*   `is_note`: 1 if the word occurs in inside the `<note>`, no value otherwise.
*   `rend_`*r*: for any *r* that is the value of a `rend` attribute.

All these features are defined for `word` nodes.
For word nodes, the value of these features is set equal to what these features
are for their first character.

Special formatting for the `rend_`*r* features is supported for some values of *r*.
The conversion supports these out-of-the-box:

value | description
--- | ---
`above` | above the line
`b` | bold font weight
`below` | below the line
`bold` | bold font weight
`center` | horizontally centered text
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

The `text` formats do not apply any kind of special formating, the `layout` formats
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

1.  Processing instructions (`<!proc a="b">`) are ignored.
1.  Comments (`<!-- this is a comment -->`) are ignored.
1.  Declarations (`<?xml ...>` `<?xml-model ...>` `<?xml-stylesheet ...>`) are
    read by the parser, but do not leave traces in the TF output.
1.  The atrributes of the root-element (`<TEI>`) are ignored.
1.  Namespaces (`xmlns="http://www.tei-c.org/ns/1.0"`) are read by the parser,
    but only the unqualified names are distinguishable in the output as feature names.
    So if the input has elements `tei:abb` and `ns:abb`, we'll see just the node
    type `abb` in the output.

### Validation

We have used [lxml](https://lxml.de) for XML parsing. During `convert` it is not used
in validating mode, but we can trigger a validation step during `check`.

However, some information about the elements, in particular whether they allow
mixed content or not, has been gleaned from the schemas, and has been used
during conversion.

Care has been taken that the names of these extra nodes and features do not collide
with element/attribute names of the TEI.


## See also

*   [about](about.md)
