#!/usr/bin/env python3
"""
Convert the test stock list to a comprehensive database matching TASI's 259 stocks
"""

import json

def parse_test_file_to_database():
    """Parse the test file and create a comprehensive stock database"""
    
    # Read the test file content (259 stocks)
    test_data = """1	2030	SARCO	56.95	-	-
2	2222	SAUDI ARAMCO	24.05	-	-
3	2380	PETRO RABIGH	7.04	-	-
4	2381	ARABIAN DRILLING	74.05	-	-
5	2382	ADES	14.9	-	-
6	4030	BAHRI	21.98	-	-
7	4200	ALDREES	121.8	-	-
8	1201	TAKWEEN	7.43	-	-
9	1202	MEPCO	27.82	-	-
10	1210	BCI	26.5	-	-
11	1211	MAADEN	52.95	-	-
12	1301	ASLAK	22.2	-	-
13	1304	ALYAMAMAH STEEL	33	-	-
14	1320	SSP	50.95	-	-
15	1321	EAST PIPES	105.7	-	-
16	1322	AMAK	64.5	-	-
17	1323	UCIC	29.78	-	-
18	2001	CHEMANOL	9.7	-	-
19	2010	SABIC	57.4	-	-
20	2020	SABIC AGRI-NUTRIENTS	118.5	-	-
21	2060	TASNEE	9.75	-	-
22	2090	NGC	19.56	-	-
23	2150	ZOUJAJ	41.24	-	-
24	2170	ALUJAIN	36.1	-	-
25	2180	FIPCO	31.54	-	-
26	2200	APC	5.54	-	-
27	2210	NAMA CHEMICALS	25.36	-	-
28	2220	MAADANIYAH	15.88	-	-
29	2223	LUBEREF	86.4	-	-
30	2240	ZAMIL INDUST	38.08	-	-
31	2250	SIIG	17.55	-	-
32	2290	YANSAB	31.42	-	-
33	2300	SPM	55.95	-	-
34	2310	SIPCHEM	17.7	-	-
35	2330	ADVANCED	32.44	-	-
36	2350	SAUDI KAYAN	4.66	-	-
37	2360	SVCP	26.82	-	-
38	3002	NAJRAN CEMENT	7.99	-	-
39	3003	CITY CEMENT	16.09	-	-
40	3004	NORTHERN CEMENT	7.79	-	-
41	3005	UACC	15.03	-	-
42	3007	OASIS	24.9	-	-
43	3008	ALKATHIRI	2.19	-	-
44	3010	ACC	21.64	-	-
45	3020	YC	32.9	-	-
46	3030	SAUDI CEMENT	38.8	-	-
47	3040	QACCO	42.7	-	-
48	3050	SPCC	25.84	-	-
49	3060	YCC	16.12	-	-
50	3080	EPCCO	26.94	-	-
51	3090	TCC	10.43	-	-
52	3091	JOUF CEMENT	6.54	-	-
53	3092	RIYADH CEMENT	29.72	-	-
54	1212	ASTRA INDUSTRIAL	149.2	-	-
55	1214	SHAKER	27.4	-	-
56	1302	BAWAN	58.9	-	-
57	1303	EIC	9.28	-	-
58	2040	SAUDI CERAMICS	30.4	-	-
59	2110	SAUDI CABLE	151.4	-	-
60	2160	AMIANTIT	20.16	-	-
61	2320	ALBABTAIN	57.95	-	-
62	2370	MESC	33.28	-	-
63	4110	BATIC	2.22	-	-
64	4140	SIECO	2.1	-	-
65	4141	ALOMRAN	26.52	-	-
66	4142	RIYADH CABLES	136.9	-	-
67	4143	TALCO	41.32	-	-
68	4144	RAOOM	57.05	-	-
69	4145	OBEIKAN GLASS	30.84	-	-
70	1831	MAHARAH	4.73	-	-
71	1832	SADR	2.86	-	-
72	1833	ALMAWARID	131.5	-	-
73	1834	SMASCO	5.83	-	-
74	1835	TAMKEEN	56.35	-	-
75	4270	SPPC	11.96	-	-
76	6004	CATRION	107.8	-	-
77	2190	SISCO HOLDING	35.7	-	-
78	4031	SGS	46.78	-	-
79	4040	SAPTCO	13.44	-	-
80	4260	BUDGET SAUDI	71.4	-	-
81	4261	THEEB	64.3	-	-
82	4262	LUMI	58.25	-	-
83	4263	SAL	172	-	-
84	4264	FLYNAS	77.5	-	-
85	1213	NASEEJ	102.7	-	-
86	2130	SIDC	30.12	-	-
87	2340	ARTEX	12.22	-	-
88	4011	LAZURDE	12.45	-	-
89	4012	ALASEEL	3.7	-	-
90	4180	FITAIHI GROUP	3.17	-	-
91	1810	SEERA	25.74	-	-
92	1820	BAAN	2.26	-	-
93	1830	LEEJAM SPORTS	147.4	-	-
94	4170	TECO	0.96	-	-
95	4290	ALKHALEEJ TRNG	22.18	-	-
96	4291	NCLE	158.5	-	-
97	4292	ATAA	62.6	-	-
98	6002	HERFY FOODS	22.43	-	-
99	6012	RAYDAN	13.18	-	-
100	6013	DWF	101	-	-
101	6014	ALAMAR	50.65	-	-
102	6015	AMERICANA	2.1	-	-
103	6016	BURGERIZZR	16.05	-	-
104	6017	JAHEZ	23.45	-	-
105	6018	SPORT CLUBS	11.57	-	-
106	4070	TAPRCO	15.79	-	-
107	4071	ALARABIA	87	-	-
108	4072	MBC GROUP	29.4	-	-
109	4210	SRMG	175	-	-
110	4003	EXTRA	88.35	-	-
111	4008	SACO	28.74	-	-
112	4050	SASCO	52.4	-	-
113	4051	BAAZEEM	5.67	-	-
114	4190	JARIR	12.54	-	-
115	4191	ABO MOATI	39	-	-
116	4192	ALSAIF GALLERY	7	-	-
117	4193	NICE ONE	24.78	-	-
118	4240	CENOMI RETAIL	25.64	-	-
119	4001	A.OTHAIM MARKET	7.3	-	-
120	4006	FARM SUPERSTORES	15.89	-	-
121	4061	ANAAM HOLDING	15.5	-	-
122	4160	THIMAR	36.4	-	-
123	4161	BINDAWOOD	5.7	-	-
124	4162	ALMUNAJEM	58	-	-
125	4163	ALDAWAA	65.75	-	-
126	4164	NAHDI	114.9	-	-
127	2050	SAVOLA GROUP	23.89	-	-
128	2100	WAFRAH	25.74	-	-
129	2270	SADAFCO	270	-	-
130	2280	ALMARAI	46.28	-	-
131	2281	TANMIAH	81.45	-	-
132	2282	NAQI	51	-	-
133	2283	FIRST MILLS	52.4	-	-
134	2284	MODERN MILLS	31.04	-	-
135	2285	ARABIAN MILLS	42.1	-	-
136	2286	FOURTH MILLING	4.02	-	-
137	2287	ENTAJ	40.48	-	-
138	4080	SINAD HOLDING	10.11	-	-
139	6001	HB	43.42	-	-
140	6010	NADEC	21.1	-	-
141	6020	GACO	15.53	-	-
142	6040	TADCO	9.95	-	-
143	6050	SFICO	85.5	-	-
144	6060	SHARQIYAH DEV	16.2	-	-
145	6070	ALJOUF	43.56	-	-
146	6090	JAZADCO	10.91	-	-
147	4165	ALMAJED OUD	123.4	-	-
148	2140	AYYAN	12.37	-	-
149	2230	CHEMICAL	7.05	-	-
150	4002	MOUWASAT	74.75	-	-
151	4004	DALLAH HEALTH	133.5	-	-
152	4005	CARE	174.7	-	-
153	4007	ALHAMMADI	33.44	-	-
154	4009	SAUDI GERMAN HEALTH	57.15	-	-
155	4013	SULAIMAN ALHABIB	253.2	-	-
156	4014	EQUIPMENT HOUSE	35.44	-	-
157	4017	FAKEEH CARE	39.1	-	-
158	4018	ALMOOSA	173.7	-	-
159	4019	SMC HEALTHCARE	20	-	-
160	2070	SPIMACO	26.08	-	-
161	4015	JAMJOOM PHARMA	161.1	-	-
162	4016	AVALON PHARMA	121.6	-	-
163	1010	RIBL	26.4	-	-
164	1020	BJAZ	12.26	-	-
165	1030	SAIB	13.69	-	-
166	1050	BSF	16.7	-	-
167	1060	SAB	31.82	-	-
168	1080	ANB	21.56	-	-
169	1120	ALRAJHI	93.2	-	-
170	1140	ALBILAD	25.22	-	-
171	1150	ALINMA	25.42	-	-
172	1180	SNB	35.48	-	-
173	1111	TADAWUL GROUP	165.9	-	-
174	1182	AMLAK	12.62	-	-
175	1183	SHL	22	-	-
176	2120	SAIC	23.55	-	-
177	4081	NAYIFAT	12.6	-	-
178	4082	MRNA	11.06	-	-
179	4083	TASHEEL	152.7	-	-
180	4084	DERAYAH	25.36	-	-
181	4130	SAUDI DARB	3.11	-	-
182	4280	KINGDOM	7.86	-	-
183	8010	TAWUNIYA	125.5	-	-
184	8012	JAZIRA TAKAFUL	12.35	-	-
185	8020	MALATH INSURANCE	13.09	-	-
186	8030	MEDGULF	16.77	-	-
187	8040	MUTAKAMELA	14.66	-	-
188	8050	SALAMA	12.4	-	-
189	8060	WALAA	12.31	-	-
190	8070	ARABIAN SHIELD	13.56	-	-
191	8100	SAICO	14.1	-	-
192	8120	GULF UNION ALAHLIA	12.4	-	-
193	8150	ACIG	11	-	-
194	8160	AICC	10.78	-	-
195	8170	ALETIHAD	10.97	-	-
196	8180	ALSAGR INSURANCE	14.21	-	-
197	8190	UCA	5.28	-	-
198	8200	SAUDI RE	47.96	-	-
199	8210	BUPA ARABIA	155.3	-	-
200	8230	ALRAJHI TAKAFUL	118.8	-	-
201	8240	CHUBB	32.6	-	-
202	8250	GIG	23.77	-	-
203	8260	GULF GENERAL	4.9	-	-
204	8270	BURUJ	16.65	-	-
205	8280	LIVA	13.29	-	-
206	8300	WATANIYA	14.94	-	-
207	8310	AMANA INSURANCE	7.86	-	-
208	8311	ENAYA	9.3	-	-
209	8313	RASAN	94	-	-
210	7200	MIS	130	-	-
211	7201	ARAB SEA	5.17	-	-
212	7202	SOLUTIONS	244.4	-	-
213	7203	ELM	912	-	-
214	7204	2P	10.42	-	-
215	7211	AZM	26.4	-	-
216	7010	STC	42.4	-	-
217	7020	ETIHAD ETISALAT	64.55	-	-
218	7030	ZAIN KSA	10.67	-	-
219	7040	GO TELECOM	103.9	-	-
220	2080	GASCO	74.75	-	-
221	2081	AWPT	126.7	-	-
222	2082	ACWA POWER	227.8	-	-
223	2083	MARAFIQ	40	-	-
224	2084	MIAHONA	25.18	-	-
225	5110	SAUDI ELECTRICITY	14.44	-	-
226	4330	RIYAD REIT	5.19	-	-
227	4331	ALJAZIRA REIT	13.37	-	-
228	4332	JADWA REIT ALHARAMAIN	5.16	-	-
229	4333	TALEEM REIT	9.6	-	-
230	4334	AL MAATHER REIT	9.4	-	-
231	4335	MUSHARAKA REIT	4.18	-	-
232	4336	MULKIA REIT	4.63	-	-
233	4337	SICO SAUDI REIT	4.26	-	-
234	4338	ALAHLI REIT 1	6.88	-	-
235	4339	DERAYAH REIT	5.49	-	-
236	4340	Al RAJHI REIT	8.16	-	-
237	4342	JADWA REIT SAUDI	10.23	-	-
238	4344	SEDCO CAPITAL REIT	6.64	-	-
239	4345	ALINMA RETAIL REIT	4.51	-	-
240	4346	MEFIC REIT	3.67	-	-
241	4347	BONYAN REIT	9.14	-	-
242	4348	ALKHABEER REIT	5.64	-	-
243	4349	ALINMA HOSPITALITY REIT	8.11	-	-
244	4350	ALISTITHMAR REIT	7.73	-	-
245	4020	ALAKARIA	17.96	-	-
246	4090	TAIBA	37	-	-
247	4100	MCDC	76.05	-	-
248	4150	ARDCO	32.04	-	-
249	4220	EMAAR EC	12.01	-	-
250	4230	RED SEA	46.4	-	-
251	4250	JABAL OMAR	18.17	-	-
252	4300	DAR ALARKAN	18.04	-	-
253	4310	KEC	12.45	-	-
254	4320	ALANDALUS	18.16	-	-
255	4321	CENOMI CENTERS	20.3	-	-
256	4322	RETAL	12.99	-	-
257	4323	SUMOU	38.32	-	-
258	4324	BANAN	4.77	-	-
259	4325	MASAR	22.74	-	-"""

    # Parse the data
    lines = test_data.strip().split('\n')
    stocks_db = {}
    
    # Name mappings for common companies
    name_mappings = {
        'SARCO': 'Saudi Arabian Oil Company',
        'SAUDI ARAMCO': 'Saudi Arabian Oil Company', 
        'SABIC': 'Saudi Basic Industries Corporation',
        'ALRAJHI': 'Al Rajhi Bank',
        'STC': 'Saudi Telecom Company',
        'BAHRI': 'National Shipping Company of Saudi Arabia',
        'ALMARAI': 'Almarai Company',
        'SNB': 'Saudi National Bank',
        'TADAWUL GROUP': 'Tadawul Group Holding Company',
        'ACWA POWER': 'ACWA Power International',
        'BUPA ARABIA': 'Bupa Arabia for Cooperative Insurance'
    }
    
    # Sector mappings based on symbol ranges
    def get_sector(symbol):
        symbol_int = int(symbol)
        if 1000 <= symbol_int <= 1999:
            return "Financial Services"
        elif 2000 <= symbol_int <= 2999:
            return "Materials & Energy"  
        elif 3000 <= symbol_int <= 3999:
            return "Materials"
        elif 4000 <= symbol_int <= 4999:
            return "Consumer & Healthcare"
        elif 5000 <= symbol_int <= 5999:
            return "Utilities"
        elif 6000 <= symbol_int <= 6999:
            return "Food & Agriculture"
        elif 7000 <= symbol_int <= 7999:
            return "Technology & Telecom"
        elif 8000 <= symbol_int <= 8999:
            return "Insurance"
        else:
            return "Other"
    
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) >= 4:
            row_num = parts[0]
            symbol = parts[1]
            short_name = parts[2]
            price = parts[3]
            
            # Get full name from mapping or use short name
            full_name = name_mappings.get(short_name, short_name.title())
            
            stocks_db[symbol] = {
                "symbol": symbol,
                "name_en": full_name,
                "name_ar": f"اسم {full_name}",  # Placeholder Arabic
                "sector": get_sector(symbol),
                "current_price": float(price) if price.replace('.', '').isdigit() else 0.0
            }
    
    return stocks_db

if __name__ == "__main__":
    db = parse_test_file_to_database()
    print(f"Generated database with {len(db)} stocks")
    
    # Save to file
    with open('saudi_stocks_database_complete.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print("Saved to saudi_stocks_database_complete.json")
