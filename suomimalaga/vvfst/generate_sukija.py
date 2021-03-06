# -*- coding: utf-8 -*-

# Copyright 2013 Hannu Väisänen (Hannu.Vaisanen@uef.fi)
# Program to generate old spellings and common spelling mistakes for Voikko lexicon.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


# This program generates old spellings (e.g. symbooli) and
# common spelling errors (e.g. kirjottaa) from file "all.lexc".
#
# An example: from line
# [Ln][Xp]symboli[X]symbol@P.INEN_SALLITTU.ON@:symbol@P.INEN_SALLITTU.ON@ NimisanaPaperi_a ;
#
# generate line
# [Ln][Xp]symboli[X]symbool@P.INEN_SALLITTU.ON@:symbool@P.INEN_SALLITTU.ON@ NimisanaPaperi_a 
#
# Shoud I generate these lines also?
# [Ln][Xp]symbooli[X]symbol@P.INEN_SALLITTU.ON@:symbol@P.INEN_SALLITTU.ON@ NimisanaPaperi_a ;
# [Ln][Xp]symbooli[X]symbool@P.INEN_SALLITTU.ON@:symbool@P.INEN_SALLITTU.ON@ NimisanaPaperi_a 
#
# This automatic generation will generate some old
# spellings and spelling errors that do not exist in real life.

# Compiling (in directory suomimalaga):
# make vvfst-sukija

# Testing:
# foma -e "read att all-sukija.att" -e "save stack sukija.fst" -e "quit"
# date; cat ~/Lataukset/koesanat?.txt | flookup -i sukija.fst | gawk 'length($0) > 0' |sort >test.out; date
# diff test.out ~/Lataukset/vvfst-sukija-testi.out | grep '<.*[+][?]' | less

# Style- ja usage-lippujen arvot suoraan Joukahaisesta:
# grep -A1 '<style>' ../vocabulary/joukahainen.xml|grep flag|sort -u|gawk '{printf "%s,", substr($1,7,length($1)-13)}'
# grep -A1 '<usage>' ../vocabulary/joukahainen.xml|grep flag|sort -u|gawk '{printf "%s,", substr($1,7,length($1)-13)}'

# Tiedostossa taivutuskaavat.lexc.in vanhat taivutukset on lisätty näihin taivutuksiin:
# Hame, Kalleus, Kansi, Koira, Lohi, Lovi, Lumi, Meri, Nainen, Onneton, Paperi,
# Pieni, Risti, Sisar, Tosi, Uistin, Veli.
# 17.6.2013: Kalleus, Kansi, Lohi, Lumi, Meri, Pieni, Tosi.

import codecs
import getopt
import re
import sys
from types import *
sys.path.append("common")
import generate_lex_common

OPTIONS = generate_lex_common.get_options()

infile = codecs.open (OPTIONS["destdir"] + u"/all.lexc", "r", "UTF-8")
outfile = codecs.open (OPTIONS["destdir"] + u"/all-sukija.lexc", 'w', 'UTF-8')

C = u"[qwrtpsšdfghjklzžxcvbnm]"  # Consonants.
V = u"[aeiouüyåäö]"              # Vovels.


def makeRePattern (wordClass, word):
    u = u"^\\[%s\\]\\[Xp\\].*%s\\[X\\]" % (wordClass, word)
    u = u.replace ('C', C)
    u = u.replace ('V', V)
    return u


def makeRe (wordClass, word):
    return re.compile (makeRePattern (wordClass, word), re.UNICODE)


def replace (s, old, new):
    u = s.replace (old + u":", new + u":")
    u = u.replace (old + u" ", new + u" ")
    u = u.replace (old + u"\t", new + u"\t")
    u = u.replace (old + u"@", new + u"@")
    return u


def replace_and_write (line, string1, string2):
    s = replace (line, string1, string2)
    outfile.write (s)


re_adi = makeRe (u"Ln", u".Cadi")
re_odi = makeRe (u"Ln", u".Codi")
re_ofi = makeRe (u"Ln", u".Cofi")
re_ogi = makeRe (u"Ln", u".Cogi")
re_oli = makeRe (u"Ln", u".Coli")
re_omi = makeRe (u"Ln", u".Comi")
re_oni = makeRe (u"Ln", u".Coni")
re_ori = makeRe (u"Ln", u".Cori")

re_adinen = makeRe (u"Ln", u".Cadinen")
re_odinen = makeRe (u"Ln", u".Codinen")
re_ofinen = makeRe (u"Ln", u".Cofinen")
re_oginen = makeRe (u"Ln", u".Coginen")
re_olinen = makeRe (u"Ln", u".Colinen")
re_ominen = makeRe (u"Ln", u".Cominen")
re_oninen = makeRe (u"Ln", u".Coninen")
re_orinen = makeRe (u"Ll", u".Corinen")

re_grafia   = makeRe (u"Ln", u"grafia")
re_grafinen = makeRe (u"Ll", u"grafinen")
re_logia    = makeRe (u"Ln", u"logia")
re_loginen  = makeRe (u"Ll", u"loginen")

re_oittaa1 = makeRe (u"Lt", u".Coittaa")
re_oittaa2 = makeRe (u"Lt", u".Cöittää")

re_ottaa1 = makeRe (u"Lt", u".Cottaa")
re_ottaa2 = makeRe (u"Lt", u".Cöttää")

re_oitin = makeRe (u"Ln", u".Coitin")
re_aatio = makeRe (u"Ln", u".Caatio")
re_uutio = makeRe (u"Ln", u".Cuutio")
re_uusio = makeRe (u"Ln", u".Cuusio")
re_tio   = makeRe (u"Ln", u"[ik]tio") # Traditio, funktio.

re_nuolaista = re.compile (u"\\[Lt\\].* Nuolaista_");
re_rangaista = re.compile (u"\\[Lt\\].* Rangaista_");


# Words to be excluded.
#
re_adi_x = re.compile (u"\\A\[Ln\]\[Xp\](dekadi|faradi|pikofaradi|stadi)\[X\]")
re_ogi_x = re.compile (u"\\A\[Ln\]\[Xp\](blogi|grogi|judogi)\[X\]")
re_omi_x = re.compile (u"\\A\[Ln\]\[Xp\](binomi|bromi|dibromi|genomi|kromi|trinomi)\[X\]")
re_oni_x = re.compile (u"\\A\[Ln\]\[Xp\](ikoni)\[X\]")
re_ori_x = re.compile (u"\\A\[Ln\]\[Xp\](hevosori|jalostusori|reettori|siitosori)\[X\]")

re_logia_x = re.compile (u"\\A\[Ln\]\[Xp\](genealogia|trilogia)\[X\]")
re_uusio_x = re.compile (u"\\A\[Ln\]\[Xp\](diffuusio)\[X\]")
re_tio_x   = re.compile (u"\\A\[Ln\]\[Xp\](aitio)\[X\]")

re_A = re.compile (u"[aou]")


spelling_pattern_list = [
  (re_adi, u"ad", u"aad", re_adi_x),  # Serenadi  => senenaadi.
  (re_odi, u"od", u"ood"),            # Aplodi    => aploodi.
  (re_ofi, u"of", u"oof"),            # Filosofi  => filosoofi.
  (re_ogi, u"og", u"oog", re_ogi_x),  # Arkeologi => arkeoloogi.
  (re_oli, u"ol", u"ool"),            # Symboli   => symbooli.
  (re_omi, u"om", u"oom", re_omi_x),  # Atomi     => atoomi.
  (re_oni, u"on", u"oon", re_oni_x),  # Telefoni  => telefooni.
  (re_ori, u"or", u"oor", re_ori_x),  # Pehtori   => pehtoori.

  (re_adinen,   u"adi",    u"aadi"),
  (re_odinen,   u"odi",    u"oodi"),
  (re_ofinen,   u"ofi",    u"oofi"),
  (re_oginen,   u"ogi",    u"oogi"),
  (re_olinen,   u"oli",    u"ooli"),
  (re_ominen,   u"omi",    u"oomi"),
  (re_oninen,   u"oni",    u"ooni"),
  (re_orinen,   u"ori",    u"oori"),

  (re_grafia,   u"grafi",  u"graafi"),
  (re_grafinen, u"grafi",  u"graafi"),
  (re_logia,    u"logi",   u"loogi", re_logia_x),
  (re_loginen,  u"logi",   u"loogi"),

  (re_oitin, u"oit", u"ot"),  # Kirjoitin => kirjotin (esim. kirjo(i)ttimen).
  (re_aatio, u"aatio", u"atsion", u"atsioon", u"NimisanaAutio_a", u"NimisanaPaperi_a"),
  (re_uutio, u"uutio", u"utsion", u"utsioon", u"NimisanaAutio_a", u"NimisanaPaperi_a"),
  (re_uusio, u"uusio", u"usion",  u"usioon",  u"NimisanaAutio_a", u"NimisanaPaperi_a", re_uusio_x),
  (re_tio,   u"tio",   u"tsion",  u"tsioon",  u"NimisanaAutio_a", u"NimisanaPaperi_a", re_tio_x),
  (re_oittaa1, u"o",   u"ot",  u"Kirjoittaa", u"Alittaa"),
  (re_oittaa2, u"ö",   u"öt",  u"Kirjoittaa", u"Alittaa"),
  (re_oittaa1, u"oit", u"ot",  u"Alittaa",    u"Alittaa"),
  (re_oittaa2, u"öit", u"öt",  u"Alittaa",    u"Alittaa"),
  (re_ottaa1,  u"ot",  u"oit", u"Alittaa",    u"Alittaa"),
  (re_ottaa2,  u"öt",  u"öit", u"Alittaa",    u"Alittaa"),
  (re_ottaa1,  u"o",   u"oi",  u"Ammottaa",   u"Ammottaa"),
  (re_ottaa2,  u"ö",   u"öi",  u"Ammottaa",   u"Ammottaa"),
  (re_nuolaista, u"Nuolaista_"),
  (re_rangaista, u"Rangaista_"),
]



lexicon_kaunis = [
    u"LEXICON <WC>SukijaKaunis_<A>",
    u"[Sg][Nm]eid:eid	<WC>MonikonGenetiiviEnJatko_<A>	;",
    u"[Sg][Nm]eitt:eitt	<WC>MonikonGenetiiviEnJatko_<A>	;",
    u"[Sg][Nm]ehitt:ehitt	<WC>MonikonGenetiiviEnJatko_<A>	;",
    u"[Sg][Nm]ehi:ehi   <WC>MonikonGenetiiviEnJatko_<A>	;",
    u"[Sp][Nm]eit<A>:eit<A>	<WC>LiOlV_<A>	;",
    u"[Sp][Nm]ehi<A>:ehi<A>	<WC>LiOlV_<A>	;",
    u"[Sill][Nm]eisii:eisii	<WC>LiOlN_<A>	;",
    u"[Sill][Nm]ehisi:ehisi	<WC>LiOlN_<A>	;",
    u"ehi:ehi   Kerronto_sti_<A> ;",
    u"e:e	<WC>YhteisetMonikonPaikallissijat_<A>	;",
    u"e:e	<WC>YhteisetMonikonSijat2_<A>	      ;",
    u"eh:eh	<WC>YhteisetMonikonPaikallissijat_<A>	;",
    u"eh:eh	<WC>YhteisetMonikonSijat2_<A>	      ;",
    u"?Laatusana	ehi:ehi	Voittoaste_<A>	;",
    u"?Laatusana	eh:eh   Yliaste_<A>	;",
]

lexicon_altis = [
    u"LEXICON <WC>SukijaAltis_<A>",
    u"[Sg][Nm]teid:teid	<WC>MonikonGenetiiviEnJatko_<A>	;",
    u"[Sg][Nm]teitt:teitt	<WC>MonikonGenetiiviEnJatko_<A>	;",
    u"[Sg][Nm]tehitt:tehitt	<WC>MonikonGenetiiviEnJatko_<A>	;",
    u"[Sg][Nm]tehi:tehi   <WC>MonikonGenetiiviEnJatko_<A>	;",
    u"[Sp][Nm]teit<A>:teit<A>	<WC>LiOlV_<A>	;",
    u"[Sp][Nm]tehi<A>:tehi<A>	<WC>LiOlV_<A>	;",
    u"[Sill][Nm]teisii:teisii	<WC>LiOlN_<A>	;",
    u"[Sill][Nm]tehisi:tehisi	<WC>LiOlN_<A>	;",
    u"tehi:tehi   Kerronto_sti_<A> ;",
    u"te:te	<WC>YhteisetMonikonPaikallissijat_<A>	;",
    u"te:te	<WC>YhteisetMonikonSijat2_<A>	      ;",
    u"teh:teh	<WC>YhteisetMonikonPaikallissijat_<A>	;",
    u"teh:teh	<WC>YhteisetMonikonSijat2_<A>	      ;",
    u"?Laatusana	tehi:tehi	Voittoaste_<A>	;",
    u"?Laatusana	eh:eh   Yliaste_<A>	;",
#    u"t:t <WC>SukijaKaunis_<A>",
]


def generate (lexicon, word_class, a):
    p = []
    for i in lexicon:
        p.append (i.replace(u"<WC>", word_class).replace(u"<A>", a))
    return p


def write_word (p):
    prefix = p[1][0:p[1].find (u"[X]")+3]
    outfile.write (u"%s%s:%s Sukija%s ;\n" % (prefix, p[0][0:len(p[0])-1], p[0][0:len(p[0])-1], p[2]))



def word_class (line):
    L = dict ([(u"[Ll]",  u"Laatusana"),
               (u"[Ln]",  u"Nimisana"),
               (u"[Lnl]", u"NimiLaatusana")])
    return L[line[0:line.find("]")+1]]


# Sanoja, joilla on vain muutama vanha taivutusmuoto. Generoidaan ne erikseen,
# mutta vain sanoille, jotka ovat Joukahaisessa. Sanat ovat Nykysuomen
# sanakirjan taivutuskaavojen numeroiden mukaisessa järjestyksessä.
#
# Tuomo Tuomi: Suomen kielen käänteissanakirja, 2. painos.
# Suomalaisen Kirjallisuuden Seura 1980.


def write_ahven (line, word):
    prefix = line[0:line.find (u"[X]")+3]
    A = u"a" if re_A.search(word) else u"ä"
    outfile.write (u"%s%s[Ses][Ny]n%s:%sn%s NimisanaLiOlV_%s ;\n" % (prefix, word, A, word, A, A))


def write_kaunis (line, word):
    prefix = line[0:line.find (u" ")]
    A = u"a" if re_A.search(word) else u"ä"
    outfile.write (u"%s %sSukijaKaunis_%s ;\n" % (prefix, word_class(line), A))


def write_altis (line, word):
    prefix = line[0:line.find (u" ")]
    A = u"a" if re_A.search(word) else u"ä"
    outfile.write (u"%s %sSukijaAltis_%s ;\n" % (prefix, word_class(line), A))


def generate_from_pattern (line, pattern_list):
    for x in pattern_list:
        if x[0].match(line):
            if (len(x) == 2):
                outfile.write (line.replace (x[1], u"Sukija" + x[1]))
            elif (len(x) == 3) or (len(x) == 4 and not x[3].match(line)):
                replace_and_write (line, x[1], x[2])
            elif (len(x) == 5) and (line.find (x[3]) >= 0):
                replace_and_write (line.replace(x[3], x[4]), x[1], x[2])
            elif (len(x) == 6) or (len(x) == 7 and not x[6].match(line)):
                s = line.replace (x[4], x[5])
                outfile.write (replace (s, x[1], x[2]))
                outfile.write (replace (s, x[1], x[3]))


# Old spellings and common spelling errors of words
# that do not conform to any pattern.
#
#    (u"", (u"", u"")),
#
word_list = [
    (u"aarteisto",        (u"aarteisto",     u"aartehisto")),
    (u"aggressiivinen",   (u"aggressiivi",   u"akressiivi")),
    (u"aikainen",         (u"aikai",         u"aikahi")),
    (u"ainainen",         (u"ainai",         u"ainahi")),
    (u"aineisto",         (u"aineisto",      u"ainehisto")),
    (u"alkovi",           (u"alkov",         u"alkoov")),
    (u"ameba",            (u"ameb",          u"ameeb")),
    (u"arsenikki",        (u"arsenik",       u"arseniik")),
    (u"assistentti",      (u"assistent",     u"asistent")),
    (u"barbaari",         (u"barbaar",       u"barbar")),
    (u"beduiini",         (u"beduiin",       u"beduin")),
    (u"biljoona",         (u"biljoon",       u"biljon")),
    (u"emali",            (u"emal",          u"emalj")),
    (u"eteinen",          (u"etei",          u"etehi")),
    (u"evankelinen",      (u"evankeli",      u"evankeeli")),
    (u"hevonen",          (u"hevo",          u"hevoi")),
    (u"humaaninen",       (u"humaani",       u"humani")),
    (u"husaari",          (u"husaar",        u"husar")),
    (u"huumori",          (u"huumor",        u"humor")),
    (u"invalidi",         (u"invalid",       u"invaliid")),
    (u"juridinen",        (u"juridi",        u"juriidi")),
    (u"kahdeksainen",        (u"kahdeksai",         u"kaheksai")),
    (u"kahdeksan",           (u"kahdeks",           u"kaheks")),
    (u"kahdeksankymppinen",  (u"kahdeksankymppi",   u"kaheksankymppi")),
    (u"kahdeksankertaistaa", (u"kahdeksankertaist", u"kaheksankertaist")),
    (u"kahdeksankymmen",     (u"kahdeksankymmen",   u"kaheksankymmen")),
    (u"kahdeksanlainen",     (u"kahdeksanlai",      u"kaheksanlai")),
    (u"kahdeksannes",        (u"kahdeksanne",       u"kaheksanne")),
    (u"kahdeksas",           (u"kahdeksa",          u"kaheksa")),
    (u"kaleeri",        (u"kaleer",      u"kaler")),
    (u"kamari",         (u"kamar",       u"kammar")),
    (u"kameli",         (u"kamel",       u"kameel")),
    (u"kampanja",       (u"kampanj",     u"kamppanj")),
    (u"kaneli",         (u"kanel",       u"kaneel")),
    (u"kaoottinen",     (u"kaootti",     u"kaaootti", u"kaaotti", u"kaotti")),
    (u"kavaljeeri",     (u"kavaljeer",   u"kavalier", u"kavaljier")),
    (u"kirjoitelma",    (u"kirjoitelm",  u"kirjotelm")),
    (u"koneisto",       (u"koneisto",    u"konehisto")),
    (u"konossementti",  (u"konossement", u"konnossement")),
    (u"kortteeri",      (u"kortteer",    u"kortier")),
    (u"kraatteri",      (u"kraatter",    u"kraater")),
    (u"kulttuuri",      (u"kulttuur",    u"kultuur", "kulttur")),
    (u"kuriiri",        (u"kuriir",      u"kurier")),
    (u"leegio",         (u"leegio",      u"legio")),
    (u"legioona",       (u"legioon",     u"legion")),
    (u"legioonalainen", (u"legioonalai", u"legionalai")),
    (u"liipaisin",      (u"liipaisi",    u"liipasi")),
    (u"lordi",          (u"lord",        u"loord")),
    (u"majoneesi",      (u"majonees",    u"majonnees")),
    (u"matrikkeli",     (u"matrikkel",   u"matrikel")),
    (u"mieluinen",      (u"mielui",      u"mieluhi")),
    (u"miljoona",       (u"miljoon",     u"miljon")),
    (u"modeemi",        (u"modeem",      u"modem")),
    (u"mosaiikki",      (u"mosaiik",     u"mosaik")),
    (u"paneeli",        (u"paneel",      u"panel")),
    (u"paronitar",      (u"paronit",     u"paroonit")),
    (u"pataljoona",     (u"pataljoon",   u"pataljon")),
    (u"patriisi",       (u"patriis",     u"patris")),
    (u"patruuna",       (u"patruun",     u"patrun")),
    (u"persoona",       (u"persoon",     u"person")),
    (u"pioneeri",       (u"pioneer",     u"pioner")),
    (u"pioni",          (u"pion",        u"pioon")),
    (u"plutoona",       (u"plutoon",     u"pluton")),
    (u"poliisi",        (u"poliis",      u"polis")),
    (u"poliitikko",     (u"poliitik",    u"politik", u"poliitiik")),
    (u"poliittinen",    (u"poliitti",    u"politti", u"poliittii")),
    (u"politiikka",     (u"politiik",    u"politik", u"poliitiik")),
    (u"posliini",       (u"posliin",     u"poslin"   u"porsliin", u"porslin")),
    (u"preettori",      (u"preettor",    u"preetor")),
    (u"pyramidi",       (u"pyramid",     u"pyramiid")),
    (u"reettori",       (u"reettor",     u"reetor")),
    (u"sampanja",       (u"sampanj",     u"samppanj")),
    (u"sapeli",         (u"sapel",       u"sapeel")),
    (u"senaatti",       ((u"senaat",     u"senaat", u"NimisanaTatti_a", u"NimisanaRisti_a"),
                         (u"senaat",     u"senat",  u"NimisanaTatti_a", u"NimisanaRisti_a"))),
    (u"senaattori",     (u"senaattor",   u"senaator")),
    (u"serafi",         (u"seraf",       u"seraaf")),
    (u"shampanja",      (u"shampanj",    u"shamppanj")),
    (u"sihteeri",       (u"sihteer",     u"sihtier")),
    (u"sitruuna",       (u"sitruun",     u"sitrun", u"sitroon", u"sitron")),
    (u"soolo",          (u"soolo",       u"solo")),
    (u"soopeli",        (u"soopel",      u"sopel")),
    (u"synagoga",       (u"synagog",     u"synagoog")),
    (u"teatteri",       (u"teatter",     u"teaater", u"teaatter", u"teater")),
    (u"temperamentti",  (u"temperament", u"tempperament")),
    (u"tooga",          (u"toog",        u"tog")),
    (u"Toscana",        (u"toscan",      u"toskan")),
    (u"tällainen",      ((u"tällai",     u"tälläi", u"NimiLaatusanaNainen_a", u"NimiLaatusanaNainen_ä"), )),
    (u"upseeri",        (u"upseer",      u"upser", u"upsier")),
    (u"upseeristo",     (u"upseeristo",  u"upsieristo")),
    (u"yhdeksäinen",        (u"yhdeksäi",         u"yheksäi")),
    (u"yhdeksän",           (u"yhdeks",           u"yheks")),
    (u"yhdeksänkymppinen",  (u"yhdeksänkymppi",   u"yheksänkymppi")),
    (u"yhdeksänkertaistaa", (u"yhdeksänkertaist", u"yheksänkertaist")),
    (u"yhdeksänkymmen",     (u"yhdeksänkymmen",   u"yheksänkymmen")),
    (u"yhdeksänlainen",     (u"yhdeksänlai",      u"yheksänlai")),
    (u"yhdeksännes",        (u"yhdeksänne",       u"yheksänne")),
    (u"yhdeksäs",           (u"yhdeksä",          u"yheksä")),

    (u"ien",     [u"[Ln][Xp]ien[X]iken[Sn][Ny]e:ikene Loppu ;"]),
    (u"kappale", [u"[Ln][Xp]kappale[X]kappal[Sg][Nm]ten:kappalten # ;"]),
    (u"maailma", [u"[Ln][Xp]maailma[X]maailmoitse:maailmoitse # ;"]),
    (u"mies",    [u"[Ln][Xp]mies[X]mies[Ses][Ny]nä:miesnä NimisanaLiOlV_ä ;",
                  u"[Ln][Xp]mies[X]mies[Ses][Ny]sä:miessä NimisanaLiOlV_ä ;"]),
    (u"pieni",   [u"[Ll][Xp]pieni[X]pien[Ses][Ny]nä:piennä NimisanaLiOlV_ä ;"]),
    (u"sankari", [u"[Ln][Xp]sankari[X]sankar[Sg][Nm]ten:sankarten # ;"]),
    (u"tuta",    [u"[Lt][Xp]tuta[X]tu:tu SukijaTuta ;"]),
    (u"venäjä",  [u"[Ln][Xp]venäjä[X]venä[Sp][Ny]ttä:venättä NimisanaLiOlV_ä ;"]),

    # 39 nuori (3, 3). Tuomi, s. 182, 184.
    #
    (u"juuri",   [u"[Ln][Xp]juuri[X]juur[Ses][Ny]na:juurna NimisanaLiOlV_a ;",
                  u"[Ln][Xp]juuri[X]juur[Ses][Ny]ra:juurra NimisanaLiOlV_a ;"]),
    (u"nuori",   [u"[Lnl][Xp]nuori[X]nuor[Ses][Ny]na:nuorna NimisanaLiOlV_a ;",
                  u"[Lnl][Xp]nuori[X]nuor[Ses][Ny]ra:nuorra NimisanaLiOlV_a ;"]),
    (u"suuri",   [u"[Lnl][Xp]suuri[X]suur[Ses][Ny]na:suurna NimisanaLiOlV_a ;",
                  u"[Lnl][Xp]suuri[X]suur[Ses][Ny]ra:suurra NimisanaLiOlV_a ;"]),

    # 46 hapsi (1, 1). Tuomi, s. 190. -- Vvfst tunnistaa muodot "hasten" ja "hapsien".
    # hasna, hassa, hasten, hapsien   -- Nämä ovat niin harvinaisia, että tarvitseeko näitä indeksoinnissa?
    #
#    (u"hapsi", [u"[Ln][Xp]hapsi[X]has[Ses][Ny]na:hasna NimisanaLiOlV_a ;",
#                u"[Ln][Xp]hapsi[X]has[Ses][Ny]sa:hassa NimisanaLiOlV_a ;"]),

    # 78 hame
    #
    (u"hame",  [u"[Ln][Xp]hame[X]hame[Sp][Ny]hta:hamehta NimisanaLiOlV_a ;"]),

    # 79 terve (4, 4). Tuomi s. 142, 143, 146.
    #
    (u"tuore", [u"[Ll][Xp]tuore[X]tuore[Ses][Ny]nna:tuorenna NimisanaLiOlV_a ;"]),
    (u"vetre", [u"[Ll][Xp]vetre[X]vetre[Ses][Ny]nnä:vetrennä NimisanaLiOlV_ä ;"]),
    (u"päre",  [u"[Ln][Xp]päre[X]päre[Ses][Ny]nnä:pärennä NimisanaLiOlV_ä ;"]),
    (u"terve", [u"[Lnl][Xp]terve[X]terve[Ses][Ny]nnä:tervennä NimisanaLiOlV_ä ;"]),
]


function_list = [
    # Herttua-tyyppisillä sanoilla on monikkomuodot, joissa ei ole o:ta (herttuilla, jne).
    #
    # 20 herttua (10, 10). Tuomi, s. 114, 116, 121, 124, 125.
    #
    (lambda line, word: outfile.write (u"[Ln][Xp]%s[X]%s:%s SukijaHerttua ;\n" %
                                       (word, word[0:len(word)-1], word[0:len(word)-1])),
     (u"aurtua",
      u"herttua",
      u"hierua",
      u"juolua",
      u"lastua",
      u"liettua",
      u"luusua",
      u"porstua",
      u"saarua",
      u"tanhua")),

    # 33 lohi (2, 2). Tuomi, s. 151.
    # lohten, uuhten
    #
    (lambda line, word: outfile.write (u"[Ln][Xp]%s[X]%s:%s SukijaLohi ;\n" %
                                       (word, word[0:len(word)-1], word[0:len(word)-1])),
     (u"lohi",
      u"uuhi")),

    # Ahven taipuu kuten sisar, paitsi että yksikön olento on myös ahvenna.
    #
    # 55 ahven (22, 23). Tuomi, s. 246, 247, 301, 302.
    #
    (write_ahven,
     (u"aamen",
      u"ahven",
      u"haiven",
      u"huomen",
      u"häiven",
      u"höyhen",
      u"ien",
      u"iljen",
      u"joutsen",
      u"jäsen",
      u"kymmen",
      u"kämmen",
      u"liemen",
      u"paimen",
      u"siemen",
      u"ruumen",
      u"terhen",
      u"taimen",
      u"tuumen",
      u"tyven",
      u"tyyven",
      u"uumen",
      u"vuomen")),

    # 69 kaunis (7, 6). Tuomi, s. 358.
    #
    (write_kaunis,
     (u"kallis",
      u"aulis",
      u"valmis",
      u"kaunis",
#      u"altis",
      u"tiivis")),

     (write_altis, (u"altis", )),
]

def convert_to_dictionary (word_list):
    l0 = map (lambda x : x[0], word_list)
    l1 = map (lambda x : x[1], word_list)
    return dict (zip (l0, l1))

sukija_dictionary = convert_to_dictionary (word_list)


def error (line):
    sys.stderr.write (line)
    sys.stderr.write ("Wrong format in sukija_dictionary.\n")
    sys.exit (1)


def write_list (line, key, data):
    for x in data:
        if type(x) == UnicodeType:
            outfile.write (x + u"\n")
        else:
            error (line)


def write_tuple (line, key, g):
     if type(g[0]) == UnicodeType:
         for i in range (1, len(g)):
             replace_and_write (line, g[0], g[i])
     elif type(g[0]) == TupleType:
         for i in range (0, len(g)):
             s = line.replace (g[i][2], g[i][3])
             outfile.write (replace (s, g[i][0], g[i][1]))
     else:
         error (line)


# Extract base form from a line.
#
base_form_re = re.compile (u"\\[Xp\\]([^[]+)\\[X\\]", re.UNICODE)

def generate_word (line, sukija_dictionary):
    r = base_form_re.search (line)
    if r:
        try:
            g = sukija_dictionary[r.group(1)]
	    if type(g) == ListType:
                write_list (line, r.group(1), g)
	    elif type(g) == TupleType:
                write_tuple (line, r.group(1), g)
	    else:
		error (line)
        except KeyError:  # It is not an error if a word is not in sukija_dictionary.
            pass


def generate_from_function (line, function_list):
    r = base_form_re.search (line)
    if r:
        for x in function_list:
            if r.group(1) in x[1]:
                x[0] (line, r.group(1))



# Copy Voikko vocabulary and insert forms that Sukija needs.
#
while True:
    line = infile.readline()
    if line == u"":
        break;
    outfile.write (line)
    if line == u"LEXICON Sanasto\n":
        outfile.write (u"Sukija ;\n")
    generate_from_pattern (line, spelling_pattern_list)
    generate_word (line, sukija_dictionary)
    generate_from_function (line, function_list)
infile.close()


outfile.write (u"\n\n\n")

OUTPUT = [
u"LEXICON SukijaNuolaista_a",
u"s:s   Nuolaista_w_a ;",
u"s:s   Nuolaista_s_a ;",
u"s:s   Johdin_U_arvelu_a ;",
u"LEXICON SukijaNuolaista_ä",
u"s:s   Nuolaista_w_ä ;",
u"s:s   Nuolaista_s_ä ;",
u"s:s   Johdin_U_arvelu_ä ;",
u"LEXICON SukijaNuolaista_aä",
u"s:s   Nuolaista_w_a ;",
u"s:s   Nuolaista_w_ä ;",
u"s:s   Nuolaista_s_a ;",
u"s:s   Nuolaista_s_ä ;",
u"s:s   Johdin_U_arvelu_a ;",
u"s:s   Johdin_U_arvelu_ä ;",
u"LEXICON SukijaRangaista_a",
u"gas:gas Nuolaista_w_a ;",
u"kas:kas Nuolaista_s_a ;",
u"kas:kas Johdin_U_arvelu_a ;",
u"LEXICON SukijaHerttua",
u"NimisanaApila_m_a ;",
u"LEXICON SukijaLohi",
u"[Sg][Nm]t:t NimisanaMonikonGenetiiviEnJatko_a ;",
u"LEXICON SukijaOmistusliite_a_in",
u"Omistusliite_a ;",
u"[O1y]in:in Liitesana_a ;",
u"LEXICON SukijaTuta",
u"[Tn1p]takse:takse SukijaOmistusliite_a_in ;",
u"[Tn2]ten:ten Liitesana_a ;",

u"LEXICON Sukija",
u"[Ln][Xp]aatelisneiti[X][Xr]ppppppp=[X]aatelisnei[Sg][Ny]den:aatelisneiden Loppu ;",
u"[Ln][Xp]herrasneiti[X][Xr]pppppp=[X]herrasnei[Sg][Ny]den:herrasneiden Loppu ;",
u"[Ln][Xp]hovineiti[X][Xr]pppp=[X]hovinei[Sg][Ny]den:hovineiden Loppu ;",
u"[Ln][Xp]neiti[X]nei[Sg][Ny]den:neiden Loppu ;",
u"[Ln][Xp]nuorimies[X]nuornamiesnä:nuornamiesnä NimisanaLiOlV_ä ;",
]

OUTPUT.extend (generate (lexicon_kaunis, u"Laatusana", u"a"))
OUTPUT.extend (generate (lexicon_kaunis, u"Laatusana", u"ä"))
OUTPUT.extend (generate (lexicon_kaunis, u"NimiLaatusana", u"a"))
OUTPUT.extend (generate (lexicon_altis,  u"NimiLaatusana", u"a"))

for x in OUTPUT:
    outfile.write (x + u"\n")
