RAW_NAMES = [
'SPV Inc., DBA: Super Company',
'Michael Forsky LLC d.b.a F/B Burgers .',
'*** Youthful You Aesthetics ***',
'Aruna Indika (dba. NGXess)',
'Diot SA, - D. B. A. *Diot-Technologies*',
'PERFECT PRIVACY, LLC, d-b-a Perfection,',
'PostgreSQL DB Analytics',
'/JAYE INC/',
' ETABLISSEMENTS SCHEPENS /D.B.A./ ETS_SCHEPENS',
'DUIKERSTRAINING OOSTENDE | D.B.A.: D.T.O. '
]

import re

def clean_names(RAW_NAMES):
   Names= [i.replace('_',' ') for i in RAW_NAMES]
   name_pairs = []
   for n in Names:
      name_pairs.append(re.split('[^a-zA-Z0-9]+[dD][^a-zA-Z0-9]*[bB][^a-zA-Z0-9]*[aA][^a-zA-Z0-9]+',n))

   clean_name_pairs = []
   for name_pair in name_pairs:
      clean_pair = []
      for part in name_pair:
         clean_pair.append(re.sub(r'^[^a-zA-Z0-9]*|[^a-zA-Z0-9]*$','',part))
         clean_tuple=(clean_pair[0],None) if len(clean_pair) ==1 else tuple(clean_pair)
      clean_name_pairs.append(clean_tuple)
   return clean_name_pairs

CLEANED_NAME_PAIRS=[
('SPV Inc', 'Super Company'),
('Michael Forsky LLC', 'F/B Burgers'),
('Youthful You Aesthetics', None),
('Aruna Indika', 'NGXess'),
('Diot SA', 'Diot-Technologies'),
('PERFECT PRIVACY, LLC', 'Perfection'),
('PostgreSQL DB Analytics', None),
('JAYE INC', None),
('ETABLISSEMENTS SCHEPENS', 'ETS SCHEPENS'),
('DUIKERSTRAINING OOSTENDE', 'D.T.O'),
]

#print(clean_names(RAW_NAMES))

assert clean_names(RAW_NAMES) == CLEANED_NAME_PAIRS