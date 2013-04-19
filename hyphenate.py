# -*- encoding: utf-8 -*-

""" Hyphenation, using Frank Liang's algorithm.

	This module provides a single function to hyphenate words.  hyphenate_word takes 
	a string (the word), and returns a list of parts that can be separated by hyphens.
	
	>>> hyphenate_word("hyphenation")
	['hy', 'phen', 'ation']
	>>> hyphenate_word("supercalifragilisticexpialidocious")
	['su', 'per', 'cal', 'ifrag', 'ilis', 'tic', 'ex', 'pi', 'ali', 'do', 'cious']
	>>> hyphenate_word("project")
	['project']
	
	Ned Batchelder, July 2007.
	This Python code is in the public domain.

	Modified to work with Spanish using Office Libre Patterns
"""

import re

__version__ = '1.0.20070709'

class Hyphenator:
	def __init__(self, patterns, exceptions=''):
		self.tree = {}
		for pattern in patterns.split():
			self._insert_pattern(pattern)
	
		self.exceptions = {}
		for ex in exceptions.split():
			# Convert the hyphenated pattern into a point array for use later.
			self.exceptions[ex.replace('-', '')] = [0] + [ int(h == '-') for h in re.split(r"[a-z]", ex) ]
				
	def _insert_pattern(self, pattern):
		# Convert the a pattern like 'a1bc3d4' into a string of chars 'abcd'
		# and a list of points [ 1, 0, 3, 4 ].
		chars = re.sub(u'[0-9]', '', pattern)
		points = [ int(d or 0) for d in re.split("[^0-9]", pattern) ]

		
		# Insert the pattern into the tree.  Each character finds a dict
		# another level down in the tree, and leaf nodes have the list of
		# points.
		t = self.tree
		for c in chars:
			if c not in t:
				t[c] = {}
			t = t[c]
		t[None] = points
		
	def hyphenate_word(self, word):
		""" Given a word, returns a list of pieces, broken at the possible
			hyphenation points.
		"""
		# Short words aren't hyphenated.
		if len(word) <= 2:
			return [word]
		# If the word is an exception, get the stored points.
		if word.lower() in self.exceptions:
			points = self.exceptions[word.lower()]
		else:
			work = '.' + word.lower() + '.'
			points = [0] * (len(work)+1)
			for i in range(len(work)):
				t = self.tree
				for c in work[i:]:
					if c in t:
						t = t[c]
						if None in t:
							p = t[None]
							for j in range(len(p)):
								points[i+j] = max(points[i+j], p[j])
					else:
						break
			# No hyphens in the first two chars or the last two.
			points[1] = points[2] = points[-2] = points[-3] = 0

		# Examine the points to build the pieces list.
		pieces = ['']
		for c, p in zip(word, points[2:]):
			pieces[-1] += c
			if p % 2:
				pieces.append('')
		return pieces

patterns = (  ##Libre Office Spanish Patterns Line 184 added .ex5a
u'''.1d2 .des1a2 .s2a5b2 .s1a2 
.s1e3d2 .s2e3l a1a2 2a3b2 4a5bor2i ab2o1 abo1r 3a4bri1g2 ab4r abr2i
3a4br\xc3\xad1g2 ab3r\xc3\xad 3a4br2o1 3a4br\xc3\xb31 a2c2a1c2 a1c2
ac4a 2acr4a a3c1r a4cre a3cu1l ac2u 2a1d2 4ad. 4a3da 3a2d3j 4a3d2o1 
3adyuv2an a2d3y ad2y2u adyu1v 2ae a1e2l a1e1m a2e2r a1es 2a3fia a1f4
af2i 2a3fi\xc3\xa1 2a3fie 2a3fi\xc3\xa9 2a3fi\xc3\xb31 2a3f\xc3\xad
3a4f\xc3\xad1l 3a4f\xc3\xad1n 2ah2u 3ahu1m 2a2i 2a\xc3\xad 3a\xc3\xads
2a3la a1l 4a5laban. al2a3b2 alab2an 3ala1g2 2a3l\xc3\xa1 2a2l1d2
2a3le. a3l2e1g2 2a3le1m 2a3l2en. 2a3le1s 2a3l\xc3\xa9 3ali1g2 al2i
a3li1z 2a3l2l 2a3lo. al2o1 a3lo1b2 a3los 2a3l\xc3\xb3. al\xc3\xb31
a3lu1b2 al2u 2a3me a1m 2an a3na a3ne 3a2no1c2 a1n2o1 an2te1m a2n1t4
an2ti1n ant2i 2a3\xc3\xb1 a3o2f4 a2o1 a3o1r 2aos a1\xc3\xb31 2a3q 2a1r
4ar. 4a3r4a 4a3r\xc3\xa1 4a2r1c2 4a3re 4a3r\xc3\xa9 4a3r\xc3\xad
4a2r1l 4a2r1n 4a3r2o1 4a3r\xc3\xb31 4a3rro1l a1r4r arr2o1
4a3rr\xc3\xb31l arr\xc3\xb31 4a2r1s2 4a2r1z 2a1s 6as. as2a2 asa3t4
4a3s2e 5a4s2e1g2 3a2s1n 6a2s3t4 7ast\xc3\xad a3tis a1t4 at2i a3ti1v
a4tro1d2 a3tr2o1 at1r a4y2u a3y 2a1z 3a4zo1g2 a3z2o1 3a4z\xc3\xb31g2
a3z\xc3\xb31 \xc3\xa12d2 1\xc3\xa12l1m \xc3\xa11l \xc3\xa11s
\xc3\xa1s2a2 1\xc3\xa12s1n \xc3\xa12te \xc3\xa11t4 1b2 b3c2 2b3d2 be1
5bes bes2a2 bie2n1 b2i 2b3j 5bor2i b2o1 bo1r b4r 4bri1g2 br2i
4br\xc3\xad1g2 b3r\xc3\xad 2bs b3s1a2 b3se b3s2i b3s2o1 2b3t4 bue3 b2u
2b3v 2b3y 1c2 c4a 3c2a5b2 c4ac4a4 ca1c2 3c2a1r ca3te ca1t4 3c\xc3\xa1
2c3c2 ce1s ces2a2 3ch 2c3n 3co. c2o1 co3ha co2h 3c1r 2c3t4 3cu1d2 c2u
1d2 3da de2h 1d2es5a1d2 des1a2 des5a1s 2dh 2d3j 2d3l 2d3m 2d3n 3d2o1
4dor\xc3\xa1 do1r 4dor\xc3\xa9 4do2r1m 4do2r1n d4r d3s 3du1m d2u 3du1r
d3v 2d3y 2e2a ea5j e3a4y 2e2\xc3\xa1 2e1c2 e2di1f4 e1d2 ed2i 2ee ee3d2
2e\xc3\xa9 2e1g2 e1ha e1h2i e2his e1h2o1 e1hu1m eh2u 2e2i1 e3i2g2
2e3me e1m 2em2o1 2empe3\xc3\xb1 e2m1p2 2emp\xc3\xa9 3emp\xc3\xa91g2
2en. e3n2i e4n3i1n e2n3t4 2e2o1 e3o4j 2e3q 2e1r e3r\xc3\xa1
e3r\xc3\xa9 2es. es3a1d2 es1a2 e2s3a4l2a3b2 e1s2a3la esa1l
es3a3\xc3\xb1 es3a1r es3a1s es1e e3t4 et2a1s4 e1\xc3\xba e2x e3x2i
\xc3\xa9e1 \xc3\xa92p2 \xc3\xa92r2c2 \xc3\xa91r \xc3\xa91s2 1f4 fe1s
fes6a2 3fia f2i 3fi\xc3\xa1 3fie 3fi\xc3\xa9 fi3n2o1 fi1n 3fi\xc3\xb31
3f\xc3\xad 4f\xc3\xad1l 4f\xc3\xad1n 1g2 g4a 2g3m 2g3n 2gs 2g3z 2ha1l
2ha1m 2ha1r4r h2a1r 2hen he1s 2hi1g2 h2i hue1 h2u 2hus h\xc3\xba1 2i
i1a\xc3\xa9 i1a2u i3cua i1c2 ic2u ie2n2o1 ie3no. ie1s i1e2s1p2 2i1h2i
i1h2o1 2i3i ija2m i3j i5la i1l illa3n2o1 i3l2l ill2an i1n in2h i3o2x
i2o1 i5re i1r i1s2a2 isa3g2 i1se i2x 2i3x2i \xc3\xadge2 \xc3\xad1g2
\xc3\xad1n \xc3\xad3n2o1 \xc3\xad2n3t4 \xc3\xad2r \xc3\xad3r4a
\xc3\xad1se 3j je1s 4jus j2u 4j\xc3\xba 1l 4labe1 l2a3b2 4lag\xc3\xa1
la1g2 4lag2o1 4lag\xc3\xb31 2l1b2 2l1c2 2l1d2 le1s les2a2 2l1f4 2l1g2
2lh li2c2u l2i li1c2 2lig2u li1g2 3li1v l\xc3\xad2c2u l\xc3\xad1c2
3l2l 2l1m 2l1n 2l1p2 2l3q 2l1s2 2l1t4 2l1v 2l1z 1m 3m2an ma3n2o1 2m1b2
3me me1s mes6a2 3mie m2i 2m1n 3mos m2o1 2m1p2 3mue1l m2u 1na n2a1l
3nal. n3an3da n2an na2n1d2 3n2a1r n4a5re na2ven na1v 3n\xc3\xa1 2n1c2
2n1d2 nde1s ndes6a2 1ne 3n\xc3\xa9 2n1f4 2n1g2 n1h2e1c2 n1h2i 1n2i
1n\xc3\xad 2n3j 2n1l 2n1m 2n1n 1n2o1 2no. n3o2l2i no1l 1n\xc3\xb31
2n3q 2n1r 2n1s ns2a2 nsa3g2 2n1t4 n2te1b2 n2t2e2i1 n2te1s1a2 n2ti1b2
nt2i n2tic2o1 nti1c2 n2ti1d2 n2tie1s n2ti1m n2ti2o1 n2tip4a2r1l nti1p2
ntip4a ntip2a1r n2ti3q n2ti1r n2tita nti1t4 n3tra1c2 nt1r ntr4a
n3tra1v 1n2u 1n\xc3\xba 2n1v 2n3y 2n1z 3\xc3\xb1 \xc3\xb1e1s
4\xc3\xb1u1d2 \xc3\xb12u 2o1 o2a o3a4c2 o2a2d2 o3ad2u o3a2li1g2 oa1l
oal2i o3a2u o3a2x o2\xc3\xa1 o2e o3e2f4 o3e4x o2h o3h2e1r o3ho1ne
oh2o1 o3i1n o2i ol2te o1l o2l1t4 on2t1r o2n1t4 2o2o2 o3o1p2 o3orde
oo1r oo2r1d2 4opera3t4 o1p2 op2e1r oper4a 5operativa opera3ti1v
operat2i o3p1l os2a2 os2e \xc3\xb31 1\xc3\xb32x 1p2 p4a 2p3c2 pe1s1a2
pla3n2o1 p1l pl2an 2p3n 3pon p2o1 2p3s2 2p3t4 3q 1r r4a ra1en r2ae
ra1h ra3i1n r2a2i ra3t4 r\xc3\xa13t4 2r1b2 2r1c2 2r1d2 re1he 4re1na
4re3n\xc3\xa1 re1s4a2 re1s2e 2r1f4 2r1g2 2rh 3r\xc3\xad 2r3j 2r1l 2r1m
2r1n 2r1p2 2r3q 1r4r 3rria rr2i 3rro1l rr2o1 3rr\xc3\xb31l rr\xc3\xb31
2r1s2 2r1t4 2r1v 2r1z r3z2o3 s1a2 1sa. s3a4b2a1r s2a3b2 s3a4b6a2s3t4
sab2a1s s3a4be1 s3a4b2o1 1s4a5bor2i sabo1r 1sab4r 2s3a4bri1g2 sabr2i
2s3a4br\xc3\xad1g2 sab3r\xc3\xad 2s3a4br2o1 2s3a4br\xc3\xb31 2s3a4b2u
1s2acr4a sa1c2 sa3c1r s4ad2u s2a1d2 1s2a3fia sa1f4 saf2i
1s2a3fi\xc3\xa1 1s2a3fie 1s2a3fi\xc3\xa9 1s2a3fi\xc3\xb31
1s2a3f\xc3\xad 2s3a4f\xc3\xad1l 2s3a4f\xc3\xad1n 1s2ah2u 2s3ahu1m
1s2a2i 2s3ais 1s2a\xc3\xad 2s3a\xc3\xads 1s2a3la sa1l 2s3al2a3b2
3s4a5laban. salab2an 2s3a4la1g2 1s2a3l\xc3\xa1 1s2a3le. 1s2a3le1m
1s2a3l2en. 1s2a3le1s 1s2a3l\xc3\xa9 1s2a3lo. sal2o1 1s2a3l\xc3\xb3.
sal\xc3\xb31 s3a2n1c2 s2an s3an3da sa2n1d2 s3and\xc3\xa1 s3and2u
1sa2n1g2 2s3ange s3a1n2i s3a1n2u s5aren s2a1r s4a3re 1s4a3rro1l sa1r4r
sarr2o1 1s4a3rr\xc3\xb31l sarr\xc3\xb31 1s4a2r1z sa4s2e2a s2a1s
s4a3s2e sa4s2e2\xc3\xa1 s7ast2i s6a2s3t4 1sast1r 1s2a1z sa3z2o3
2s3a4zo1g2 2s3a4z\xc3\xb31g2 sa3z\xc3\xb31 1s\xc3\xa1 2s1\xc3\xa12l1m
s\xc3\xa11l s\xc3\xa12n 2s1\xc3\xa11n2i 2s1\xc3\xa12s1n s\xc3\xa11s
2s1\xc3\xa12t4 2s1b2 4s1c2 2s1d2 1se. 1s2e2a 1s2e2\xc3\xa1 1s2e1c2
s1e1d2 se2d2u 1s2ee 1s2e\xc3\xa9 1s2e1g2 s2e1l s3e2le 1se3l2l 1s2e3me
se1m 1s2empe3\xc3\xb1 se2m1p2 1s2emp\xc3\xa9 2s3emp\xc3\xa91g2 se2n
1s2e2o1 1s2e3q 2s3e4qu2i seq2u 1s2e1r 1s2es. se1s2a2 se1s1e 1s\xc3\xa9
2s1f4 2s1g2 2s1h 1s2i 2s3j 2s1l 2s1m 2s1n 1s2o1 2s3o4j 1s\xc3\xb31
2s1p2 2s3q 2s3t4 3s2u 2s1v 1t4 3te. 2te3a1l t2e2a 2tea1n2o1 te2an
2te3a4y 2teca1m t2e1c2 tec4a 2tec\xc3\xa11m te3c\xc3\xa1 2tec2o1
3te3co. 3tecos 2te3c1r 2te1d2 2te1f4 3tefe 2teg2u t2e1g2 2tej2u te3j
2tema te1m 2tem2u 2te1n2o1 2te3o4j t2e2o1 2te1p2 te1s1a2 te1s1e 2tete
1t4e3t4 2te1v 2ti. t2i 2ti1a\xc3\xa9 tia3n2o1 ti2an 2ti1a2u 2tica1r4r
ti1c2 tic4a ti3c2a1r 2ti1c2i1c2 tic2i 2ticle tic1l 2t2icr2i ti3c1r
3ti3d2o1 ti1d2 2tifa ti1f4 2tigr4a ti1g2 tig1r 2tigu1b2 tig2u 2ti1h
2t2i3i 3timon ti1m tim2o1 4tim2o1n2o1 3ti1n2o1 ti1n 2ti1p2a1p2 ti1p2
tip4a 2t2ipara1s2i tip2a1r tip4a3r4a tipar2a1s 2t2ip2i 3t2ip2ir2i
tipi1r 2tip\xc3\xba 2tise1m ti1se 2ti1s\xc3\xa9 2t2i1s2i 2ti1s2o1
2tit2o1 1t4i1t4 2titu1b2 tit2u 2tivi1r ti1v tiv2i 2t\xc3\xad1g2
2t4\xc3\xad1t4 2t5m 3trae. t1r tr4a tr2ae 3trae1d2 3tra\xc3\xa9
3trai1g2 tr2a2i 3tr2a\xc3\xad 3tra1l 3trap2e2a tra1p2 3t1r2a1r
4t1ra1r4r 3t4ra3t4 3tra3y 3tr\xc3\xa1 3tr2i 3tr2o1 2t\xc3\xba 2u
u2ba1l u1b2 ue1n4a uena3v ue1s2a2 ui3n2o1 u2i ui1n u1s2a2 usa3t4 u1se
2u3u \xc3\xba2l \xc3\xba1n 1v 3v2a1r ve1s v\xc3\xa93a vo3h v2o1 1x 3xa .ex5a
3x2u 3y ye1s 2y2u 1z z4a5re z2a1r 2z1c2 2z1g2 2z1m 2z1n 3z2o1 4zo1g2
z2o4o2 3z\xc3\xb31 4z\xc3\xb31g2 2z1t4''')

exceptions = ("""
u-na u-no 
""")




