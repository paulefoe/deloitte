import re
from pdfminer.layout import LAParams
from pdfminer.converter import  PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal
import os

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
import bisect
from .models import Book



class FindBook:
    def __init__(self, search_text, path_to_books=None):
        """if specified path_to_books should be a list of actual books like [/path/to/book.pdf]"""
        self.search_text = search_text
        self.path_to_books = path_to_books
        self.titles = []
        self.destination = []
        if not self.path_to_books:
            self.path_to_books = [a.book for a in Book.query.all()]

    def search_books(self):
        res = []

        for book_name in self.path_to_books:
            name = os.path.split(book_name)[1]
            if book_name.split('.')[-1] == 'pdf':
                temp = self.__search_pdf(book_name)
                if temp[name]:
                    res.append(temp)
        return res

    def __get_outlines_pdf(self, book_name):
        """Get the titles and pages that this titles link to. If there's no destination (link to text from title
        it'll not be possible to find out the title of the page)"""

        fp = open(book_name, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)

        try:
            outlines = document.get_outlines()
            for (level, title, dest, a, se) in outlines:
                if not dest:
                    break
                self.destination.append(dest[0].objid)
                self.titles.append(title)
        except (PDFNoOutlines, TypeError):
            pass
        fp.close()

    def __search_pdf(self, book_name):
        self.__get_outlines_pdf(book_name)
        document = open(book_name, 'rb')
        word = self.search_text.split()
        # Create resource manager
        rsrcmgr = PDFResourceManager()
        # Set parameters for analysis.
        laparams = LAParams()
        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        counter = 0
        finded = {}
        name = os.path.split(book_name)[1]
        finded[name] = {}
        for page in PDFPage.get_pages(document):
            counter += 1
            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text()
                    res = re.search('.'.join(word), text)
                    if res:
                        # finded_pages.append(page)
                        if self.destination:
                            if isinstance(page.attrs['Contents'], list):
                                page.attrs['Contents'] = page.attrs['Contents'][0]

                            if page.attrs['Contents'].objid in self.destination:

                                # finded[book_name] = {}
                                finded[name][counter] = self.titles[bisect.bisect_left(self.destination,
                                                                                       page.attrs['Contents'].objid)]
                            else:

                                finded[name][counter] = self.titles[bisect.bisect(self.destination,
                                                                            page.attrs['Contents'].objid) - 1]
                        else:
                            finded[name][counter] = 'No title were found'

        document.close()
        return finded


