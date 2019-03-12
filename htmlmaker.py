import os
from datetime import datetime


class HtmlMaker:
    def contact_list(self, contacts):
        """ generates the contact list """

        html = "<ul>"

        for c in contacts:
            html += (
                '<li><a href="'
                + c[0]
                + '.html">'
                + c[0]
                + " - "
                + str(c[1])
                + " "
                + str(c[2])
                + "</a></li>\n"
            )

        html += "</ul>"

        self.write_html_file(html, "contacts.html")

    def contact_messages(self, contact, messages):
        """ writes the messages for a contact """

        html = ""

        html += (
            """
        <h1>"""
            + str(contact[1])
            + " "
            + str(contact[2])
            + """</h1>
        """
        )

        html += "<ul>"

        for m in messages:

            dt = datetime.fromtimestamp(m[1] / 1000)
            tstr = dt.isoformat(timespec="minutes")

            html += "<li><b>" + tstr + ": </b>" + str(m[0]) + "</li>"

        html += "</ul>"

        self.write_html_file(html, str(contact[0]) + ".html")

    def group_list(self, contacts):
        """ generates the contact list """

        html = "<ul>"

        for c in contacts:
            html += (
                '<li><a href="group_'
                + str(c[2])
                + '.html">'
                + str(c[1])
                + "</a></li>\n"
            )

        html += "</ul>"

        self.write_html_file(html, "groups.html")

    def group_messages(self, group, messages):
        """ writes the messages for a group """

        html = ""

        html += (
            """
        <h1>"""
            + str(group[1])
            + """</h1>
        """
        )

        html += "<ul>"

        for m in messages:

            dt = datetime.fromtimestamp(m[1] / 1000)
            tstr = dt.isoformat(timespec="minutes")

            html += "<li><b>" + tstr + ": </b>" + str(m[0]) + " " + str(m[2]) + "</li>"

        html += "</ul>"

        self.write_html_file(html, "group_" + str(group[2]) + ".html")

    def write_html_file(self, html, filename):

        pre = """
        <html>
        <head>
        <title>Threema to HTML</title>
        <meta charset="UTF-8"> 
        <style type="text/css">
            body, html { font-family: sans-serif; }
        </style>
        </head>
        <body>
        """
        post = "</body></html>"

        out = pre + html + post
        outfile = os.path.join("html", filename)

        f = open(outfile, "w")
        f.write(out)
        f.close()
