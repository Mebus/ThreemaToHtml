#!/usr/bin/python3

import argparse
import json
import os
import sqlite3
import subprocess
import sys

from htmlmaker import HtmlMaker


class Threema2HTML:

    key = "x'abcdefgh...'"
    input_file = "threema.db"
    plaindb_file = "data/plaintext.db"

    def __init__(self):
        self.html = HtmlMaker()

    def parse_args(self):

        self.parser = argparse.ArgumentParser(prog="PROG")
        self.parser.add_argument(
            "inputfile", help="the encrypted threema.db file from Threema"
        )
        self.args = self.parser.parse_args()
        self.input_file = str(self.args.inputfile)

    def config(self):
        """ load the configuration """

        with open("config.json") as json_data_file:
            data = json.load(json_data_file)
            self.key = data["key"]

    def decrypt(self):

        print("Opening: " + self.input_file)
        print("Will rite to: " + self.plaindb_file)

        # Cleanup
        if os.path.exists(self.plaindb_file):
            os.remove(self.plaindb_file)

        p = subprocess.Popen(
            ["sqlcipher", self.input_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        s = (
            """
        PRAGMA cipher_default_kdf_iter = 4000;PRAGMA key = '"""
            + self.key
            + """'; 
        ATTACH DATABASE '"""
            + self.plaindb_file
            + """' AS plaintext KEY '';  -- empty key will disable encryption
        SELECT sqlcipher_export('plaintext');
        DETACH DATABASE plaintext;
        """
        )
        out, _ = p.communicate(s.encode())
        print(out.decode())

        if os.path.exists(self.plaindb_file):
            print("Decrypted the database!")
            return True
        else:
            return False

    def load_plain(self):
        print("Loading the plain database...")

        self.conn = sqlite3.connect(self.plaindb_file)
        self.c = self.conn.cursor()

        self.convert_contacts()
        self.convert_groups()

    def convert_contacts(self):
        """ converts all contacts """

        contacts = self.c.execute(
            "SELECT identity, firstName, lastName FROM contacts ORDER BY lastName;"
        )

        a = contacts.fetchall()

        self.html.contact_list(a)

        for k in a:
            self.convert_contact(k)

    def convert_contact(self, contact):
        """ converts the messages for a single contact """

        messages = self.c.execute(
            'SELECT body, postedAtUTC FROM message WHERE identity = "'
            + str(contact[0])
            + '" ORDER BY postedAtUTC;'
        )
        self.html.contact_messages(contact, messages)

    def convert_groups(self):
        """ converts all groups """

        contacts = self.c.execute(
            "SELECT apiGroupId, name, id FROM m_group ORDER BY name;"
        )

        a = contacts.fetchall()
        self.html.group_list(a)

        for k in a:
            self.convert_group(k)

    def convert_group(self, group):
        """ extracts the messages from a group """

        messages = self.c.execute(
            'SELECT identity, postedAtUTC, body FROM m_group_message WHERE groupId = "'
            + str(group[2])
            + '" ORDER BY postedAtUTC;'
        )

        print(group[2])

        self.html.group_messages(group, messages)

    def convert_all(self):
        self.config()
        self.parse_args()
        if self.decrypt():
            self.load_plain()


if __name__ == "__main__":

    t2html = Threema2HTML()
    t2html.convert_all()
