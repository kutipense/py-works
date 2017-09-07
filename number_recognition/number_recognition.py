#!/usr/bin/python3
#py3.5.2
import os
import re


class Arama():
    def __init__(self, harfler='58829'):
        self.harfler = harfler
        self.numlist = [sayi for sayi in self.harfler]
        self.words = ''
        self.lu = len(self.numlist)
        self.p = 0
        self.dic = {'0': '',
                    '1': ' ',
                    '2': '[abc]',
                    '3': '[def]',
                    '4': '[ghi]',
                    '5': '[jkl]',
                    '6': '[mno]',
                    '7': '[pqrsş]',
                    '8': '[tuv]',
                    '9': '[wxyz]'}

    def bul(self):
        with open('data.txt', 'r') as dosya:
            self.kars = [i[:self.lu] for i in dosya.readlines() if len(i) - 1 == self.lu]
            for word in self.kars:
                for num in self.numlist:
                    self.icomp = re.compile(self.dic.get(num), re.IGNORECASE)
                    try:
                        self.sonuc = self.icomp.search(word[self.p])
                        self.p += 1
                        self.words = self.words + self.sonuc.group()
                    except:
                        break
                self.p = 0
                self.words = self.words + ' '
            self.yaz()

    def sayac(self):
        for i in self.miniliste:
            if len(i) != self.lu:
                yield i

    @property
    def duzenle(self):
        self.miniliste = self.words.split(' ')
        while True:
            try:
                self.miniliste.remove('')
            except:
                break
        for i in tuple(self.sayac()):
            del self.miniliste[self.miniliste.index(i)]
        return self.miniliste, len(self.miniliste)

    def yaz(self):
        x, y = self.duzenle
        if y and x:
            print('\n{} results has been found!\n'.format(y), '\rResults are:', ', '.join(x), '\b!')
        elif y == 1:
            print('Result is: {}'.format(', '.join(x)))
        else:
            print('Nothing to find!')


if __name__ == '__main__':
    while True:
        os.system('clear')
        girdi = input(('Give me some numbers: '))
        if girdi:
            a = Arama(girdi)
        else:
            a = Arama()
        a.bul()
        input('\nPlay again? [enter]')
        os.system('clear')
