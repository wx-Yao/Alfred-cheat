#!/usr/bin/python
import os
from workflow import MATCH_ALL, MATCH_ALLCHARS

class Parser:
    def __init__(self,path):
        self._path=path
        self._available=os.listdir(self._path)
        return None

    def availableSheets(self):
        return self._available

    def list(self, sheetName):
        return [] if sheetName not in self._available else self.__parseSheet(sheetName) # return value: [{}, {}, {}, ...]

    def searchAcrossAll(self, keyword, workflow):
        ret=[]
        for sheet in self._available:
            ret.extend(self.__parseSheet(sheet))
        return self.filter(ret, keyword, workflow) # [{}, {}, {}...]

    def searchInSheet(self, keyword, sheetName, workflow):
        return self.filter(self.__parseSheet(sheetName), keyword, workflow)

    def __parseSheet(self, filename):
        with open(os.path.join(self._path,filename), 'r') as f:
            content=f.read().decode('utf-8',"replace").strip()
        # Tokenize to get each "item" by spliting the "\n\n". This rule must be repspected
        content=[item.strip() for item in content.split("\n\n")]
        # ASSUME the item pattern is "comment, comment, comment ..., command"
        # An item doesn't have to contain comments but must have a command
        items=[]
        for item in content:
            try:
                comment, command=item.rsplit("\n",1)
            except ValueError:
                continue
            # Or you wanna see which line doesn't comform to the format
            #   comment=""
            #   command="Fail to parse: {}".format(item)
            # cleanup "#" and \n
            comment=comment.replace("#","").replace("\n",". ").strip()
            command=command.strip()
            items.append((comment, command))
        return [dict(comment=comment, command=command) for comment,command in items] # [{}, {}, {}...]

    def filter(self, content, keyword, workflow):
        def searchIndex(item):
            return u" ".join([item["comment"],item["command"]])
        return workflow.filter(keyword, content,key=searchIndex, match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=50)
