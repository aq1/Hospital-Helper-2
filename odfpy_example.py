#!/usr/bin/env python
# -*- coding: utf-8 -*-

from odf.opendocument import OpenDocumentText
from odf.style import (Style, TextProperties, ParagraphProperties,
                       ListLevelProperties, TabStop, TabStops)
from odf.text import (H, P, List, ListItem, ListStyle, ListLevelStyleNumber,
                      ListLevelStyleBullet)
from odf import teletype

textdoc = OpenDocumentText()

# Creating different style used in the document
s = textdoc.styles

# For Level-1 Headings that are centerd
h1style = Style(name="CenterHeading 1", family="paragraph")
h1style.addElement(ParagraphProperties(attributes={"textalign": "center"}))
h1style.addElement(TextProperties(
    attributes={"fontsize": "18pt", "fontweight": "bold"}))

# For Level-2 Headings that are centered
h2style = Style(name="CenterHeading 2", family="paragraph")
h2style.addElement(ParagraphProperties(attributes={"textalign": "center"}))
h2style.addElement(TextProperties(
    attributes={"fontsize": "15pt", "fontweight": "bold"}))

# For bold text
boldstyle = Style(name="Bold", family="text")
boldstyle.addElement(TextProperties(attributes={"fontweight": "bold"}))

# For numbered list
numberedliststyle = ListStyle(name="NumberedList")
level = 1
numberedlistproperty = ListLevelStyleNumber(
    level=str(level), numsuffix=".", startvalue=1)
numberedlistproperty.setAttribute('numsuffix', ".")
numberedlistproperty.addElement(ListLevelProperties(
    minlabelwidth="%fcm" % (level - .2)))
numberedliststyle.addElement(numberedlistproperty)

# For Bulleted list
bulletedliststyle = ListStyle(name="BulletList")
level = 1
bulletlistproperty = ListLevelStyleBullet(level=str(level), bulletchar=u"•")
bulletlistproperty.addElement(ListLevelProperties(
    minlabelwidth="%fcm" % level))
bulletedliststyle.addElement(bulletlistproperty)


# Justified style
justifystyle = Style(name="justified", family="paragraph")
justifystyle.addElement(ParagraphProperties(
    attributes={"textalign": "justify"}))

# Creating a tabstop at 10cm
tabstops_style = TabStops()
tabstop_style = TabStop(position="10cm")
tabstops_style.addElement(tabstop_style)
tabstoppar = ParagraphProperties()
tabstoppar.addElement(tabstops_style)
tabparagraphstyle = Style(name="Question", family="paragraph")
tabparagraphstyle.addElement(tabstoppar)
s.addElement(tabparagraphstyle)


# Register created styles to styleset
s.addElement(h1style)
s.addElement(h2style)
s.addElement(boldstyle)
s.addElement(numberedliststyle)
s.addElement(bulletedliststyle)
s.addElement(justifystyle)
s.addElement(tabparagraphstyle)

# Adding main heading
mymainheading_element = H(outlinelevel=1, stylename=h1style)
mymainheading_text = "This is my main heading"
teletype.addTextToElement(mymainheading_element, mymainheading_text)
textdoc.text.addElement(mymainheading_element)

# Adding second heading
mysecondheading_element = H(outlinelevel=1, stylename=h2style)
mysecondheading_text = "This is my subheading"
teletype.addTextToElement(mysecondheading_element, mysecondheading_text)
textdoc.text.addElement(mysecondheading_element)

# Adding a paragraph
paragraph_element = P(stylename=justifystyle)
paragraph_text = """
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\n"""
teletype.addTextToElement(paragraph_element, paragraph_text)
textdoc.text.addElement(paragraph_element, paragraph_text)


# Adding bulleted list
bulletlist = List(stylename=bulletedliststyle)
listitemelement1 = ListItem()
listitemelement1_paragraph = P()
listitemelement1_content = "My first item"
teletype.addTextToElement(listitemelement1_paragraph, listitemelement1_content)
listitemelement1.addElement(listitemelement1_paragraph)
bulletlist.addElement(listitemelement1)
listitemelement2 = ListItem()
listitemelement2_paragraph = P()
listitemelement2_content = "My second item"
teletype.addTextToElement(listitemelement2_paragraph, listitemelement2_content)
listitemelement2.addElement(listitemelement2_paragraph)
bulletlist.addElement(listitemelement2)

textdoc.text.addElement(bulletlist)

# Adding numbered list
numberlist = List(stylename=numberedliststyle)
listitemelement1 = ListItem()
listitemelement1_paragraph = P()
listitemelement1_content = "My first item"
teletype.addTextToElement(listitemelement1_paragraph, listitemelement1_content)
listitemelement1.addElement(listitemelement1_paragraph)
numberlist.addElement(listitemelement1)
listitemelement2 = ListItem()
listitemelement2_paragraph = P()
listitemelement2_content = "My second item"
teletype.addTextToElement(listitemelement2_paragraph, listitemelement2_content)
listitemelement2.addElement(listitemelement2_paragraph)
numberlist.addElement(listitemelement2)

textdoc.text.addElement(numberlist)


# Adding a tabbed sentence to check tabstop
newtext = "Testing\tTabstops"
tabp = P(stylename=tabparagraphstyle)
teletype.addTextToElement(tabp, newtext)
textdoc.text.addElement(tabp)

textdoc.save(u"myfirstdocument.odt")