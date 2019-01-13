import json
import random


class Node:
    def __init__(self, father, children, name):
        self.father = father
        if children is None:
            self.children = []
        else:
            self.children = children
        self.name = name

    def __str__(self):
        return self.name


class SE:
    def __init__(self, json_file):
        file = open(json_file, encoding='utf-8').read()
        datas = json.loads(file)
        self.country = datas['country']
        self.title = datas['title']
        self.start = datas['start']
        self.end = datas['end']
        self.candidates = datas['authors']
        self.current_president = datas['currentBoss']
        self.organism = 'ORGANISM'
        self.registered = datas['voters registered by BV']
        self.list_nodes = []
        self.root = Node(None, [], self.country)
        self.profondeur = 0
        self.build_tree(self.root, datas['sections'])

    """def build_tree(self, current_section, content_node):
        for elt in content_node:
            node = None
            if content_node[elt]['type'] == 'BV':
                node = BV(section=current_section, name=elt, voters_num=content_node[elt]['nombre_votants'])
                self.list_nodes.append(node)
            else:
                node = Section(father=current_section, name=elt)
                self.build_tree(current_section=node, content_node=content_node[elt]['sections'])
            current_section.children.append(node)
        self.list_nodes.append(current_section)"""

    def build_tree(self, current_section, content_node):
        for elt in content_node:
            if 'sections' not in elt:
                node = BV(section=current_section, name=elt['name'],
                          voters_num=int((0.3 * random.random() + 0.7) * self.registered), register_num=self.registered)
                self.list_nodes.append(node)
            else:
                node = Section(father=current_section, name=elt['name'])
                self.build_tree(current_section=node, content_node=elt['sections'])
            current_section.children.append(node)
        self.list_nodes.append(current_section)


class PV:
    def __init__(self, owner, bv, result):
        self.owner = owner
        self.bv = bv
        self.result = result

    def __str__(self):
        return "PV de {} dans le bureau de vote {} avec pour resultat {}".format(self.owner, self.bv.name, self.result)


class Section(Node):
    def __init__(self, name, father=None, children=None):
        Node.__init__(self, father, children, name)

    def __str__(self):
        return "Section : {}".format(self.name)


class BV(Node):
    def __init__(self, name, voters_num, register_num, pvs=None, section=None):
        Node.__init__(self, section, None, name)
        if pvs is None:
            self.pVs = []
        self.voters_num = voters_num
        self.register_num = register_num

    def __str__(self):
        return "Bureau de Vote : {}, avec {} votants et {} inscrits".format(self.name, self.voters_num,
                                                                            self.register_num)
