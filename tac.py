from node import Node


class GeneratorTac:
    def __init__(self):
        self.var = -1
        self.label = -1
        self.tac_str = ""
        self.line = 0
        self.label_stack = []

    def get_var(self):
        self.var += 1
        return 'r' + str(self.var)


    def escribirLinea(self, *argv):
        for arg in argv:
            self.tac_str += (arg + ' ')
        self.tac_str = self.tac_str[:-1]
        self.tac_str += '\n'
        self.line += 1

    def tacGenerator(self, node):
        if not isinstance(node, Node):
            return node
        c = node.children

        if node.type == 'bloque':
            self.tacGenerator(c[0])
            if len(c) == 2:
                self.tacGenerator(c[1])
        if node.type == 'declaracion':
            pass
        if node.type == 'delcaracionAsignada':
            self.escribirLinea(c[1], '=', self.tacGenerator(c[2]))
        if node.type == 'bool':
            return self.tacGenerator(c[0])
        if node.type == 'boolop':
            v = self.get_var()
            self.escribirLinea(v, '=', self.tacGenerator(
                c[0]), c[1], self.tacGenerator(c[2]))
            return v
        if node.type == 'numcomp':
            v = self.get_var()
            self.escribirLinea(v, '=', self.tacGenerator(
                c[0]), c[1], self.tacGenerator(c[2]))
            return v
        if node.type == 'num':
            return self.tacGenerator(c)
        if node.type == 'numop':
            v = self.get_var()
            self.escribirLinea(v, '=', self.tacGenerator(
                c[0]), c[1], self.tacGenerator(c[2]))
            return v
        if node.type == 'concat':
            v = self.get_var()
            self.escribirLinea(v, '=', self.tacGenerator(
                c[0]), '+', self.tacGenerator(c[1]))
            return v
        if node.type == 'strcast':
            v = self.get_var()
            self.escribirLinea(v, '=', 'num2str(', self.tacGenerator(c[0]), ')')
            return v
        if node.type == 'str':
            return self.tacGenerator(c[0])
        if node.type == 'assign':
            self.escribirLinea(c[0], '=', self.tacGenerator(c[1]))
        if node.type == 'if':
            if len(c) == 4:
                label1 = self.get_label()
                label2 = self.get_label()
                self.label_stack.append(label2)

                self.escribirLinea(
                    'if', 'false', self.tacGenerator(c[0]), 'goto', label1)
                self.tacGenerator(c[1])
                self.escribirLinea('goto', label2)
                self.escribirLinea(label1)
                self.tacGenerator(c[2])
                self.tacGenerator(c[3])
                self.escribirLinea(self.label_stack.pop())
            elif len(c) == 3:
                label1 = self.get_label()
                label2 = self.get_label()
                self.label_stack.append(label2)

                self.escribirLinea(
                    'if', 'false', self.tacGenerator(c[0]), 'goto', label1)
                self.tacGenerator(c[1])
                self.escribirLinea('goto', label2)
                self.escribirLinea(label1)
                self.tacGenerator(c[2])
                self.escribirLinea(self.label_stack.pop())
            else:
                label = self.get_label()
                self.escribirLinea(
                    'if', 'false', self.tacGenerator(c[0]), 'goto', label)
                self.tacGenerator(c[1])
                self.escribirLinea(label)
        if node.type == 'elif':
            if len(c) == 3:
                label = self.get_label()
                self.escribirLinea(
                    'if', 'false', self.tacGenerator(c[0]), 'goto', label)
                self.tacGenerator(c[1])
                self.escribirLinea('goto', self.label_stack[-1])
                self.escribirLinea(label)
                self.tacGenerator(c[2])
            else:
                label = self.get_label()
                self.escribirLinea(
                    'if', 'false', self.tacGenerator(c[0]), 'goto', label)
                self.tacGenerator(c[1])
                self.escribirLinea('goto', self.label_stack[-1])
                self.escribirLinea(self.label)
        if node.type == 'else':
            self.tacGenerator(c[0])
        if node.type == 'while':
            label1 = self.get_label()
            label2 = self.get_label()

            self.escribirLinea(label1)
            self.escribirLinea('if', 'false', self.tacGenerator(c[0]), 'goto', label2)
            self.tacGenerator(c[1])
            self.escribirLinea('goto', label1)
            self.escribirLinea(label2)

    def numeroLinea(self, my_str):
        arr = my_str.split('\n')
        for i in range(len(arr)):
            arr[i] = str(i) + '. ' + arr[i]
        return '\n'.join(arr)

    def get_label(self):
        self.label += 1
        return 'L' + str(self.label)