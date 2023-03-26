import requests, json, re
from datetime import datetime

def main(pubid=5243):
    #make req for every pubid req
    url = f'https://static.wsstack.nn4maws.net/content/v5/menus/{pubid}.json'

    response = requests.get(url)

    #has portions
    wantedcats=["Lager, beer, craft and cider | Draught",
                "Real ale",            
                "Hard Seltzers ",
                "Gin",
                "Vodka",
                "Rum",
                "Whisky",
                "Liqueur and brandy",]

    bottles=["World beers and craft | Bottles & cans",
            "Cider | Bottles",]

    wine =["Wine, prosecco & sparkling"]
    bas = ["Bombs and shots"]

    othercats=[
                "2 for £5.50",
                "3 for £5.50",
                "4 for £5.50"]

    '''
    drinks data

    Name | Size | Price | ABV | Category

    '''
    drinkstable=[]

    pattern = r'(\d+(\.\d+)?)(%| ABV)'

    if response.status_code == 200:
        data = response.json()
        for element in data['menus']:
            if element['name'] == "Drinks":
                for item in element['subMenu']:
                    #item is one of the non deals alcoholic drinks
                    if item["headerText"] in wantedcats:
                        for product in item["productGroups"]:
                            for drink in product['products']:
                                matches = re.findall(pattern, drink["description"])
                                if matches:
                                    # Extract the first match and convert it to a float
                                    abv = float(matches[0][0])
                                    if drink["portions"] is not None:
                                        for eachitem in drink["portions"]:                                        
                                            drinkstable.append([drink["displayName"],eachitem["name"],eachitem["price"],abv,product["groupHeader"]])

                    #bottles            
                    if item["headerText"] in bottles:
                        for product in item["productGroups"]:
                            for drink in product['products']:
                                # need to regex for abv, and size
                                # can then do price normally
                                pattern_ml = r'[0-9]+ml'
                                matches_abv = re.findall(pattern, drink["description"])
                                abv = float(matches_abv[0][0])                            
                                matches_ml = re.findall(pattern_ml, drink["description"])
                                ml = float(matches_ml[0][:3])
                                drinkstable.append([drink["displayName"],ml,drink["priceValue"],abv,product["groupHeader"]])

                    if item["headerText"] in wine:
                        for drinkgroup in item['productGroups']:
                            for drink in drinkgroup["products"]:
                                matches = re.findall(r'[0-9]+ml', drink["description"].replace('\\', ''))
                                if matches:
                                    abv = matches[0][0]
                                    if drink["portions"] is not None:
                                            for eachitem in drink["portions"]:                                        
                                                drinkstable.append([drink["displayName"],eachitem["name"],eachitem["price"],abv,product["groupHeader"]])


                    #implement these
                
                    #bombs and shots            
                    if item["headerText"] in bas:
                        for product in item["productGroups"]:
                            for drink in product['products']:
                                if drink["description"]:
                                    # need to regex for abv, and size
                                    # can then do price normally
                                    pattern_ml = r'[0-9]+ml'
                                    matches_abv = re.findall(pattern, drink["description"])
                                    abv = float(matches_abv[0][0])                            
                                    matches_ml = re.findall(pattern_ml, drink["description"])
                                    if matches_ml:
                                        ml = float(matches_ml[0][:-2])
                                        drinkstable.append([drink["displayName"],ml,drink["priceValue"],abv,product["groupHeader"]])

                    
                    #item is alcoholic deals
                    if item["headerText"] in othercats:
                        if item["headerText"] == "2 for £5.50":
                            deal=2
                        if item["headerText"] == "3 for £5.50":
                            deal=3
                        if item["headerText"] == "4 for £5.50":
                            deal=4
                        for productgroup in item["productGroups"]:
                            for product in productgroup["products"]:
                                pattern_ml = r'[0-9]+ml'
                                matches_abv = re.findall(pattern, product["description"])
                                abv = float(matches_abv[0][0])                            
                                matches_ml = re.findall(pattern_ml, product["description"])
                                new_name = str(product["displayName"])+" on "+str(deal)+" for £5.50"
                                if matches_ml:
                                    ml = float(matches_ml[0][:-2])
                                    drinkstable.append([new_name,ml*deal,5.50,abv,productgroup["groupHeader"]])
                                else:
                                    drinkstable.append([new_name,25.0*deal,5.50,abv,productgroup["groupHeader"]])

    conversionlist=["Single","Double","Third","Half","Pint","Half pint","Half Pint"]
    '''
    Go through and change "double" "single" etc to ml
    '''
    for drink in drinkstable:
        if drink[1] in conversionlist:
            if drink[1] == "Single":
                drink[1] = 25
            if drink[1] == "Double":
                drink[1] = 50
            if drink[1] == "Third":
                drink[1] = 75
            if drink[1] == "Half Pint":
                drink[1] = 284
            if drink[1] == "Half pint":
                drink[1] = 284
            if drink[1] == "Half":
                drink[1] = 284
            if drink[1] == "Pint":
                drink[1] = 568


    '''
    Name | Size | Price | ABV | Category

    Add units column
    Add £/unit column

    '''

    for drink in drinkstable:
        units=float((drink[1]*drink[3])/1000)
        drink.append(units)
        drink.append(float(drink[2]/units))

    '''
    Name | Size | Price | ABV | Category | Units | £/unit
    '''
    sorted_main = sorted(drinkstable, key=lambda x: x[-1])
    return(sorted_main)

#list of pubs
pubslist=[
    ['5243', 'Abraham Darby'],
['6694', 'St. Matthews Hall'],
['5834', 'The Arthur Robertson'],
['5397', 'The Atrium'],
['6882', 'The Avion'],
['1406', 'The Bellwether'],
['592', 'The Billiard Hall'],
['297', 'The Bishop Vesey'],
['6234', 'The Black Horse'],
['6875', 'The Bloxwich Showman'],
['1251', 'The Bottle of Sack'],
['791', 'The Briar Rose'],
['1656', 'The Britannia'],
['1355', 'The Charlie Hall'],
['6422', 'The Chequers Inn'],
['1823', 'The City Arms'],
['663', 'The Clifton'],
['6596', 'The Court of Requests'],
['7226', 'The Cross Inn'],
['5609', 'The Dragon Inn'],
['2192', 'The Earl of Mercia'],
['1320', 'The Elizabeth of York'],
['295', 'The Figure of Eight'],
['163', 'The Flying Standard'],
['189', 'The Full Moon'],
['1670', 'The Hornet'],
['798', 'The Malthouse'],
['6387', 'The Mare Pool'],
['495', 'The Moon Under Water'],
['184', 'The Moon Under Water'],
['7528', 'The Navigation Inn '],
['7178', 'The Pump House'],
['626', 'The Royal Tiger'],
['1470', 'The Sir Henry Newbolt'],
['4124', 'The Soloman Cutler'],
['6400', 'The Spon Gate'],
['398', 'The Spread Eagle'],
['82', 'The Square Peg'],
['1227', 'The Waterfront Inn'],
['5178', 'The White Swan'],
['494', 'The William Shenstone'],
['6299', 'The William Tyler'],
['6137', 'Airport Wetherspoons'],
['5505', 'NEC Wetherspoons'],
['185', 'Baxters Court'],
['91', 'Goldengrove'],
['2173', 'Goodmans Field'],
['42', 'Hamilton Hall'],
['27', 'J.J. Moons'],
['20', 'J.J. Moons'],
['39', 'J.J. Moons'],
['5', 'J.J. Moons'],
['4063', 'Oyster Rooms'],
['506', 'Penderels Oak'],
['239', "Shakespeare's Head"],
['390', 'Spouters Corner'],
['2466', 'The Alfred Herring'],
['783', 'The Angel'],
['635', 'The Asparagus'],
['87', 'The Bankers Draft'],
['7498', 'The Barrel Vault'],
['35', 'The Beaten Docket'],
['51', 'The Beehive'],
['884', 'The Botwell Inn'],
['1006', 'The Brockley Barge'],
['1686', 'The Capitol'],
['4030', 'The Central Bar'],
['453', 'The Coronation Hall'],
['279', 'The Coronet'],
['364', 'The Crosse Keys'],
['1019', 'The Edmund Halley'],
['134', 'The Fox on the Hill'],
['109', 'The Foxley Hatch'],
['2862', 'The Furze Wren'],
['585', 'The Gate Clock'],
['50', 'The George'],
['46', 'The George'],
['112', 'The Good Yarn'],
['1139', 'The Great Harry'],
['7337', 'The Greenwood Hotel'],
['6364', 'The Greyhound'],
['590', 'The Half Moon'],
['133', 'The Harvest Moon'],
['469', 'The Holland Tringham'],
['703', 'The Hudson Bay'],
['2450', 'The Ice Wharf'],
['638', 'The Kentish Drovers'],
['214', 'The Kings Ford'],
['266', 'The Kings Tun'],
['538', 'The Knights Templar'],
['1637', 'The Ledger Building'],
['550', 'The Liberty Bounds'],
['1408', 'The London & Rye'],
['7249', 'The London and South Western'],
['195', 'The Masque Haunt'],
['1106', 'The Metropolitan Bar'],
['2757', 'The Milan Bar'],
['62', 'The Millers Well'],
['188', 'The Montagu Pyke'],
['71', 'The Moon & Stars'],
['37', 'The Moon and Sixpence'],
['79', 'The Moon and Stars'],
['38', 'The Moon on the Hill'],
['106', 'The Moon on the Hill'],
['227', 'The Moon on the Square'],
['30', 'The Moon Under Water'],
['33', 'The Moon Under Water'],
['81', 'The Moon Under Water'],
['70', 'The Moon Under Water'],
['6524', 'The Mossy Well'],
['728', 'The New Cross Turnpike'],
['101', 'The New Crown'],
['4', 'The New Moon'],
['154', 'The Nonsuch Inn'],
['2175', 'The Plough & Harrow'],
['487', 'The Pommelers Rest'],
['9', 'The Railway Bell'],
['59', 'The Red Lion & Pineapple'],
['704', 'The Richmal Crompton'],
['3', 'The Rochester Castle'],
['6283', 'The Rocket'],
['1260', 'The Rockingham Arms'],
['7077', 'The Sir John Hawkshaw'],
['430', 'The Sir John Oldcastle'],
['1249', 'The Sir Julian Huxley'],
['6014', 'The Sir Michael Balcon'],
['337', 'The Skylark'],
['140', 'The Sovereign of the Seas'],
['467', 'The Surrey Docks'],
['6151', 'The Tailors Chalk'],
['707', 'The Tichenham Inn'],
['18', 'The Toll Gate'],
['53', 'The Village Inn'],
['433', 'The Walnut Tree'],
['254', 'The Watch House'],
['5447', 'The Watchman'],
['55', 'The Whispering Moon'],
['1732', 'The White Swan'],
['221', 'The Wibbas Down Inn'],
['166', 'The William Morris'],
['2650', 'The William Webb Ellis'],
['1169', 'The Willow Walk'],
['6017', 'The Worlds Inn'],
['100', 'The WrongUn'],
['64', 'Wetherspoons'],
['246', "Beckett's Bank"],
['7517', 'Stick or Twist '],
['446', 'The Barum Top Inn'],
['7104', 'The Blue Bell'],
['5523', 'The Bowling Green'],
['7283', 'The Briggate'],
['7402', 'Charles Henry Roe'],
['1536', 'The Cherry Tree'],
['7153', 'The Clothiers Arms'],
['6976', 'The Commercial Inn'],
['6633', 'The Crossed Shuttle'],
['5482', 'The Cuthbert Brodrick'],
['855', 'The Glass Blower'],
['5713', 'The Golden Beam '],
['6206', 'The Hedley Verity'],
['6693', 'The Lister Arms'],
['4432', 'The Livery Rooms - opens in March '],
['2314', 'The Lord Wilson'],
['1739', 'The Myrtle Grove'],
['1904', 'The Obediah Brooke'],
['7207', 'The Old Unicorn'],
['6399', 'The Percy Shaw'],
['5771', 'The Picture House'],
['937', 'The Richard Oastler'],
['2554', 'The Sir Norman Rae'],
['451', 'The Six Chimneys'],
['546', 'The Three Hulats'],
['4219', 'The Turls Green'],
['2080', 'The Union Rooms'],
['6767', 'The White Hart'],
['2779', 'The Winter Seam'],
['643', 'Wetherspoons'],
['6255', 'Cabot Court Hotel'],
['7060', 'The Iron Duke'],
['6817', 'Palladium Electric'],
['2346', 'The Carnival Inn'], ['2337', 'The Cerdic'],
['2580', 'The Coal Orchard'],
['5501', 'The Duke of Wellington'],
['6229', 'The Glassmaker'],
['2609', 'The King of Wessex'],
['1790', 'The Lantokay'],
['234', 'The Perkin Warbeck'], ['7098', 'The Posset Cup'],
['6507', 'The Quarter Jack'],
['4439', 'The Reeds Arms'],
['677', 'The William Dampier'],
['6027', 'The Bell'],
['167', 'The Falcon'],
['7097', 'The Hope & Champion'],
['1195', 'The Moon Under Water'],
['6402', 'The White Hart'],
['152', 'Wetherspoons'],
['5647', 'Castle in the Air'],
['6520', 'The Mardi Gras'],
['312', 'The Eccles Cross'],
['835', 'The Edwin Waugh'],
['5613', 'The Ford Madox Brown'],
['2809', 'The Great Central'],
['315', 'The Harbord Harbord'],
['511', 'The J. P. Joule'],
['193', 'The Moon Under Water'],
['1015', 'The Paramount'],
['305', 'The Robert Peel'],
['1090', 'The Sedge Lynn'],
['2099', 'The Seven Stars'],
['1103', 'The Tim Bobbin'],
['2103', 'The Waterhouse'],
['192', 'Wetherspoons'],
['5498', 'Chapel an Gansblydhen'],
['7323', 'The Coinage Hall'],
['6383', 'The Green Parrot'],
['5958', 'The Hain Line'],
['6006', 'The John Francis Basset'],
['6981', 'The King Doniert'],
['1033', 'The Packet Station'],
['5441', 'The Rann Wartha'],
['1856', 'The Towan Blystra'],
['1099', 'The Tremenheere'],
['5376', 'Try Dowr'],
['1977', 'City and County'],
['7609', 'Sanctuary Bar - Opens 31 Jan'],
['1699', 'The Admiral of the Humber'],
['6203', 'The Benjamin Fawcett'],
['6803', 'The Cross Keys'],
['1002', 'The Prior John'],
['1417', 'The Three John Scotts'],
['2156', 'Colombia Press'],
['5480', 'Harpsfield Hall'],
['566', 'The Admiral Byng'], ['6427', 'The Angel Vaults Inn'], ['473', 'The Crown'], ['269', 'The Full House'], ['120', 'The Hart & Spool'], ['6849', 'The Manor House'], ['569', 'The Moon and Cross'], ['95', 'The Moon Under Water'], ['177', 'The Pennsylvanian'], ['6391', 'The Port Jackson'], ['1641', 'The Six Templars'], ['1031', 'The Standing Order'], ['7244', 'The Star'], ['289', 'The Three Magnets'], ['5152', 'Waterend Barn'], ['280', 'Cornfield Garage'], ['896', 'The Bright Helm'], ['218', 'The Cliftonville Inn'], ['7264', 'The Crowborough Cross'], ['6284', 'The George Hotel'], ['1806', 'The John Logie Baird'], ['6189', 'The London & County'], ['7139', 'The Picture Playhouse'], ['6221', 'The Post & Telegraph'], ['5340', 'The West Quay'], ['5504', 'George Hotel'], ['176', 'Golden Cross Hotel'], ['4086', 'The Crown'], ['5562', 'The Foley Arms Hotel'], ['953', 'The Old Swanne Inne'], ['293', 'The Postal Order'], ['407', 'The Rising Sun'], ['6404', 'The Royal Enfield'], ['1040', 'Georges Meeting House'], ['5556', 'The Admiral Collingwood'], ['1171', 'The Britannia Inn'], ['6217', 'The Chevalier Inn'], ['2925', 'The General Sir Redvers Buller'], ['2661', 'The Gog and Magog'], ['6011', 'The Green Ginger'], ['253', 'The Imperial'], ['7309', 'The Jolie Brise'], ['2365', 'The Mannamead'], ['2365', 'the-mannamead-plymouth'], ['1155', 'The Panniers'], ['259', 'The Powder Monkey'], ['7251', "The Queen's Head Hotel"], ['2700', 'The Richard Hopkins'], ['6449', 'The Rose Salterne'], ['6035', 'The Sawyers Arms'], ['6850', 'The Stannary Court'], ['6790', 'The Star Inn'], ['5879', 'The Talk of the Town'], ['662', 'The Union Rooms'], ['688', 'The Vigilance'], ['5978', 'The Water Gate'], ['2999', 'The White Ball Inn'], ['7280', 'The White Hart Hotel'], ['2520', 'Globe Hotel'], ['136', 'The Bell Hotel'], ['664', 'The Glass House'], ['6970', 'The Limes'], ['1719', 'The Queen of Iceni'], ['6620', 'The Red Lion'], ['5937', 'The Romany Rye'], ['210', 'The Troll Cart'], ['7320', 'The Whalebone'], ['915', 'The Whiffler'], ['7294', 'The William Adams'], ['5285', 'Grover & Allen'], ['6382', 'The Corn Exchange'], ['288', 'The Cricketers'], ['1058', 'The Drabbet Smock'], ['1311', 'The Golden Lion'], ['6251', 'The Joseph Conrad'], ['6377', 'The Kings Head Hotel'], ['5478', 'The Willow Tree'], ['7136', 'The Hedgeford Lodge'], ['441', 'The Acorn Inn'], ['1964', 'The Arnold Machin'], ['1898', 'The Bradley Green'], ['6808', 'The Butlers Bell'], ['7029', 'The Green Dragon'], ['1328', 'The Linford Arms'], ['412', 'The Lord Burton'], ['5367', 'The Old Swan'], ['257', 'The Picture House'], ['671', 'The Plaza'], ['2060', 'The Poste of Stone'], ['199', 'The Reginald Mitchell'], ['6226', 'The Wheatsheaf'], ['755', 'The Wheatsheaf'], ['541', 'Hoylake Lights'], ['6535', 'The Barkers Brewery'], ['2071', 'The Brass Balance'], ['6826', 'The Captain Alexander'], ['6235', 'The Childwall Fiveways Hotel'], ['4259', 'The Clairville'], ['2375', 'The Dee Hotel'], ['2517', 'The Fall Well'], ['6910', 'The Frank Hornby'], ['2026', 'The Glass House'], ['5531', 'The John Masefield'], ['7216', 'The Lifeboat'], ['2011', 'The Lime Kiln'], ['6641', 'The Master Mariner'], ['1200', 'The Mockbeggar Hall'], ['2936', 'The Navigator'], ['7293', 'The Nine Arches'], ['6486', 'The North Western'], ['6068', 'The Queens Picture House'], ['403', 'The Raven'], ['198', 'The Richard John Blackler'], ['203', 'The Sir Henry Segrave'], ['2372', 'The Thomas Frost'], ['6103', 'The Watch Maker'], ['2572', 'The Welkin'], ['414', 'The Wild Rose'], ['4113', 'The Willow Grove'], ['2092', 'Jewel of the Severn'], ['6041', 'Montgomerys Tower'], ['5534', 'The Hippodrome'], ['777', 'The Shrewsbury Hotel'], ['5325', 'The Thomas Botfield'], ['2773', 'The Wilfred Owen'], ['6444', 'The William Withering'], ['89', 'J.J. Moons'], ['438', 'Moon and Starfish'], ['7152', 'Parsons Barn'], ['7286', 'Rose & Crown'], ['117', 'The Barking Dog'], ['2495', 'The Battesford Court'], ['1379', 'The Blue Boar'], ['7386', 'The Bottle Kiln'], ['614', 'The Colley Rowe Inn'], ['7111', 'The Dairyman'], ['143', 'The Elms'], ['562', 'The Eva Hart'], ['90', 'The Great Spoon of Ilford'], ['4055', 'The Ivory Peg'], ['60', 'The Last Post'], ['148', 'The Last Post'], ['158', 'The Moon on the Square'], ['43', 'The New Fairlop Oak'], ['698', 'The Picture Palace'], ['137', 'The Playhouse'], ['1902', 'The Roebuck'], ['736', 'The Temeraire'], ['2861', 'The William Aylmer'], ['7262', 'The Windmill'], ['5309', 'Wetherspoon Express'], ['7087', 'John The Clerk of Cramlington'], ['6500', 'The Electrical Wizard'], ['834', 'The Forum'], ['6389', 'The Red Lion'], ['548', 'The Rohan Kanhai'], ['5516', 'The Wallaw'], ['2194', 'Lloyds No.1 Bar'], ['5467', 'The Admiral Sir John Borlase Warren'], ['6487', 'The Butter Cross'], ['2211', 'The Company Inn'], ['5436', 'The Dominie Cross'], ['1168', 'The Ernehale'], ['5837', 'The Free Man'], ['6728', 'The Gooseberry Bush'], ['1554', 'The Joseph Else'], ['7091', 'The Lady Chatterley'], ['758', 'The Last Post'], ['2155', 'The Liquorice Gardens'], ['1367', 'The Picture House'], ['810', 'The Pilgrim Oak'], ['6527', 'The Regent'], ['1154', 'The Roebuck Inn'], ['6326', 'The Samuel Hall'], ['369', 'The Sir John Arderne'], ['6423', 'The Stag & Pheasant'], ['5479', 'The William Peverel'], ['5571', 'The Woodthorpe Top'], ['229', 'Opera House'], ['7185', 'The Belle and Lion'], ['530', 'The County Hotel'], ['397', 'The Eight Bells'], ['6149', 'The Flying Boat'], ['7343', 'The Golden Hope'], ['738', 'The Golden Lion'], ['428', 'The Humphrey Bean'], ['498', 'The Leading Light'], ['1685', 'The Mechanical Elephant'], ['172', 'The Muggleton Inn'], ['6102', 'The Peter Cushing'], ['7404', 'The Railway'], ['316', 'The Robert Pocock'], ['5994', 'Royal Victoria Pavilion'], ['213', 'The Samuel Peto'], ['2957', 'The Saxon Shore'], ['360', 'The Sennockian'], ['6436', 'The Sir Norman Wisdom'], ['2505', 'The Society Rooms'], ['291', 'The Thomas Ingoldsby'], ['6549', 'The Thomas Waghorn'], ['673', 'The West Gate Inn'], ['7243', 'The Crown Hotel'], ['5639', 'The Gary Cooper'], ['474', 'The Pilgrims Progress'], ['5805', 'The Swan Hotel'], ['168', 'The White House'], ['651', 'Ritz'], ['928', 'The Blue Bell Inn'], ['7190', 'The Coliseum Picture Theatre'], ['2493', 'The Ivy Wall'], ['6662', 'The Joseph Morton'], ['606', 'The Moon Under Water'], ['2880', 'The Packhorse Inn'], ['405', 'The Red Lion'], ['2795', 'The Square Sail'], ['6911', 'The Stamford Post'], ['605', 'The Sweyn Forkbeard'], ['219', 'The Tollemache Inn'], ['6788', 'The White Horse'], ['423', 'The Yarborough Hotel'], ['1508', 'Rupert Brooke'], ['2145', 'The Bear and Ragged Staff'], ['263', 'The Benjamin Satchwell'], ['576', 'The Felix Holt'], ['1610', 'The Golden Bee'], ['2201', 'The Thomas Lloyd'], ['904', 'S. Fowler & Co.'], ['5954', 'The Man in the Moon'], ['5452', 'Sandford House'], ['236', 'The College Arms'], ['5362', 'The Drapers Arms'], ['5762', 'The George Hotel'], ['5983', 'The Hippodrome'], ['748', 'The Regal'], ['7140', 'The Swan & Angel'], ['5588', 'The Weeping Ash'], ['1725', 'The Wheatsheaf Inn'], ['2196', 'Sheffield Water Works Company'], ['281', 'The Bankers Draft'], ['721', 'The Benjamin Huntsman'], ['1776', 'The Bluecoat'], ['1757', 'The Church House'], ['6236', 'The Francis Newton'], ['2259', 'The Gate House'], ['2844', 'The Horseshoe'], ['5279', 'The Joseph Bramah'], ['5600', 'The Old Market Hall'], ['6600', 'The Queens Hotel'], ['5261', 'The Rawson Spring'], ['4128', 'The Red Lion'], ['6430', 'The Running Horse'], ['7519', 'The Scarsdale Hundred '], ['5483', 'The Sheaf Island'], ['5593', 'The Silkstone Inn'], ['7188', 'The Steel Foundry'], ['7095', 'The Wagon & Horses'], ['1713', 'The Woodseats Palace'], ['2930', 'Spa Lane Vaults'], ['507', 'The Babington Arms'], ['631', 'The Crown'], ['1017', 'The Observatory'], ['6747', 'The Pillar of Rock'], ['2020', 'The Portland Hotel'], ['1556', 'The Red Lion'], ['1805', 'The Sir Nigel Gresley'], ['6416', 'The Smithy Fold'], ['170', 'The Standing Order'], ['6058', 'The Thomas Leaper'], ['5103', 'Waggon and Horses'], ['6042', 'The Admiral Sir Lucius Curtis'], ['4084', 'The Angel'], ['656', 'The Bright Water Inn'], ['6148', 'The Crown Inn'], ['6256', 'The Denmead Queen'], ['684', 'The First Post'], ['322', 'The Isambard Kingdom Brunel'], ['5731', 'The Ivy House'], ['1526', 'The John Jacques'], ['1345', 'The John Russell Fox'], ['876', 'The Lord Arthur Lee'], ['6405', 'The Lord Palmerston'], ['468', 'The Old Gaolhouse'], ['480', 'The Parchment Makers'], ['532', 'The Prince Arthur'], ['7211', 'The Queen Hotel'], ['6232', 'The Red Lion'], ['7331', 'The Red Lion'], ['2834', 'The Sir Alec Rose'], ['1855', 'The Sir John Baker'], ['6301', 'The Six Bells'], ['202', 'The Standing Order'], ['1373', 'The Star'], ['6240', 'The Tilly Shilling'], ['6147', 'The Wagon Works'], ['6265', 'The Albany Palace'], ['7089', 'The Bath Arms'], ['6689', 'The Bear'], ['6638', 'The Bell'], ['5330', 'The Dockle Farmhouse'], ['4334', 'The Kings Head Inn'], ['247', 'The Savoy'], ['4351', 'The Silk Mercer'], ['5578', 'The Sir Daniel Arms'], ['5649', 'The Albert and The Lion'], ['311', 'The Ash Tree'], ['6165', 'The Boot Inn'], ['6652', 'The Commercial Hotel'], ['6439', 'The Court Leet'], ['4237', 'The Eric Bartholomew'], ['255', 'The Grey Friar'], ['5959', 'The Jolly Tars'], ['5333', 'The Layton Rakes'], ['6279', 'The Leyland Lion'], ['6666', 'The Old Chapel'], ['272', 'The Postal Order'], ['7086', 'The Poulton Elk'], ['6723', 'The Railway Hotel'], ['182', 'The Regal Moon'], ['2038', 'The Sir Henry Tate'], ['1990', 'The Sir Richard Owen'], ['543', 'The Sir Thomas Gerard'], ['5308', 'The Thomas Burke'], ['2218', 'The Thomas Drummond'], ['1883', 'The Trawl Boat Inn'], ['7078', 'The Twelve Tellers'], ['7275', 'The Velvet Coaster'], ['5603', 'The Wallace Hartley'], ['4111', 'The Amber Rooms'], ['2193', 'The Corn Exchange'], ['583', 'The High Cross'], ['5469', 'The Kettleby Cross'], ['790', 'The Lord Keeper of the Great Seal'], ['1727', 'The Monkey Walk'], ['786', 'The Moon & Bell'], ['6901', 'The Shoulder of Mutton'], ['789', 'The Sugar Loaf'], ['6545', 'The White House'], ['424', 'The William Wygston'], ['6246', 'The Angel Hotel'], ['7479', 'The Buck Inn '], ['7206', 'The Crown Inn'], ['1667', 'The Devonshire'], ['6934', 'The Giant Bellflower'], ['7182', 'The Ironstone Miner'], ['383', 'The Lord Rosebery'], ['1587', 'The Plimsoll Line'], ['1845', 'The Postern Gate'], ['2870', 'The Punch Bowl'], ['2121', 'The Ralph Fitz Randal'], ['4265', 'The Resolution'], ['6692', 'The Swatters Carr'], ['5560', 'The Three Tuns'], ['6286', 'The Unicorn Hotel'], ['893', 'The Winter Gardens'], ['6264', 'The Art Picture House'], ['1473', 'The Bishop Blaize'], ['2963', 'The Brocket Arms'], ['6795', 'The Bulls Head Hotel'], ['6738', 'The Gateway'], ['187', 'The Moon Under Water'], ['2710', 'The Robert Shaw'], ['6499', 'The Shay Wake'], ['200', 'The Spinning Mule'], ['395', 'The Up Steps Inn'], ['174', 'The Assembly Rooms'], ['2009', 'The Claude du Vall'], ['520', 'The Edmund Tylney'], ['131', 'The George'], ['194', 'The Herbert Wells'], ['5363', 'The Jack Fairman'], ['557', 'The Jack Phillips'], ['479', 'The Oxted Inn'], ['416', 'The Rodboro Buildings'], ['238', 'The Sun'], ['323', 'The Back of Beyond'], ['6220', 'The Bear'], ['6233', 'The Hatchet Inn'], ['527', 'The Hope Tap'], ['4424', 'The King and Castle'], ['142', 'The Moon and Spoon'], ['65', 'The Old Manor'], ['4309', 'The Windlesora'], ['6209', 'The Bank House'], ['7102', 'The Lord High Constable of England'], ['683', 'The Lord John'], ['778', 'The Moon Under Water'], ['224', 'The Regal'], ['5484', 'The Royal Hop Pole'], ['6491', 'Thorns Farm'], ['6583', 'The Beehive'], ['237', 'The Dolphin & Anchor'], ['5785', 'The Flying Horse'], ['534', 'The George Inn'], ['217', 'The Hatters Inn'], ['206', 'The Jubilee Oak'], ['586', 'The Lynd Cross'], ['2873', 'The Ounce & Ivy Bush'], ['19', 'The Red Lion'], ['6946', 'The Six Gold Martlets'], ['6307', 'The Three Fishes'], ['222', 'The Berkeley'], ['183', 'The Commercial Rooms'], ['6644', 'The Jolly Sailor'], ['609', 'The Kingswood Colliers'], ['2703', 'The Knights Templar'], ['456', 'The Robert Fitzharding'], ['640', 'The Staple Hill Oak'], ['559', 'The Van Dyck Forum'], ['6907', 'The W. G. Grace'], ['2473', 'V-Shed'], ['5326', 'The Bishops Mill'], ['540', 'The Company Row'], ['4197', 'The Five Quarter'], ['6040', 'The Grand Electric Hall'], ['7043', 'The Half Moon Inn'], ['6530', 'The Hat and Feathers'], ['6906', 'The Highland Laddie'], ['6687', 'The Horse Shoe Inn'], ['5268', 'The Stanley Jefferson'], ['302', 'The Tanners Hall'], ['303', 'The Thomas Sheraton'], ['5115', 'The Ward Jackson'], ['1423', 'The Water House'], ['6261', 'The Wicket Gate'], ['4114', 'The William Stead'], ['6476', 'The Blackwater Stream'], ['5254', 'The Christopher Creeke'], ['911', 'The Greyhound'], ['1412', 'The Lord Wimborne'], ['6269', 'The Man in the Wall'], ['6009', 'The Mary Shelley'], ['164', 'The Moon in the Square'], ['825', 'The Nightjar'], ['5570', 'The Parkstone and Heatherlands'], ['5314', 'The Quay'], ['1548', 'The Royal Oak'], ['475', 'The Swan'], ['6016', 'The William Henry'], ['4243', 'The Bransty Arch'], ['6890', 'The Chief Justice of the Common Pleas'], ['6748', 'The Dog Beck'], ['516', 'The Furness Railway'], ['1795', 'The Henry Bessemer'], ['2718', 'The Miles Thompson'], ['4365', 'The William Rufus'], ['470', 'Woodrow Wilson'], ['7295', 'The Bull and Stirrup Hotel'], ['1617', 'The Calverts Court'], ['632', 'The Counting House'], ['4254', 'The Ferry Boat'], ['434', 'The Friar Penketh'], ['7090', 'The George Inn'], ['6862', 'The Kingfisher'], ['6207', 'The Looking Glass'], ['418', 'The Penny Black'], ['1970', 'The Premier'], ['4260', 'The Queens Arms'], ['1635', 'The Society Rooms'], ['4079', 'The Society Rooms'], ['209', 'The Square Bottle'], ['1632', 'The Unicorn'], ['2923', 'The Wheatsheaf'], ['6345', 'The Wilfred Wood'], ['7122', 'The Captain Noel Newton'], ['2367', 'The Catherine Wheel'], ['6612', 'The Company of Weavers'], ['258', 'The Exchange'], ['6019', 'The Four Candles'], ['5779', 'The Narrows'], ['556', 'The Penny Black'], ['6191', 'The Swan & Castle'], ['4469', 'The William Morris'], ['6617', 'The Cooper Rose'], ['1752', 'The Fire Station'], ['6367', 'The Five Swans'], ['6866', 'The Harry Clasper'], ['6777', 'The High Main'], ['2341', 'The Job Bulman'], ['5126', 'The Keel Row'], ['6180', 'The Mile Castle'], ['7134', 'The Ritz'], ['1893', 'The Sir William de Wessyngton'], ['6132', 'The Tilley Stone'], ['6513', 'The Wild Boar'], ['370', 'The William Jameson'], ['319', 'The Wouldhave'], ['646', 'Wetherspoons'], ['6158', 'The Cordwainer'], ['449', 'The Earl of Dalkeith'], ['6484', 'The Railway Inn'], ['334', 'The Red Well'], ['5385', 'The Samuel Lloyd'], ['2890', 'The Saracens Head Inn'], ['5811', 'The Saxon Crown'], ['5509', 'The Crown Rivers'], ['24', 'The Moon Under Water'], ['5499', 'The Dukes Head'], ['1869', 'The Kings Fee'], ['1469', 'The Mail Rooms'], ['2245', 'The Central Bar'], ['2248', 'The Tuesday Bell'], ['2396', 'The Spirit Merchant'], ['7387\\t', 'An Geata Arundel - Opening Feb 2022'], ['7381', "Keavan's Port "], ['7330', 'The Forty Foot'], ['7299', 'The Great Wood  '], ['7278', 'The Old Borough'], ['7380', 'The Silver Penny'], ['7377', 'The South Strand '], ['7329', 'The Three Tun Tavern'], ['7328', 'The Linen Weaver'], ['7390', 'The Tullow Gate'], ['6335', 'An Ruadh-Ghleann'], ['6966', 'The Hay Stook'], ['5801', 'The John Fairweather'], ['7164', 'The Booking Office'], ['6183', 'The Alexander Graham Bell'], ['7248', 'The Caley Picture House'], ['1135', 'The Foot of the Walk'], ['4312', 'The Playfair'], ['6245', 'The Sir Walter Scott'], ['371', 'The Standing Order'], ['6341', 'The White Lady'], ['5428', 'Cross Keys'], ['331', 'The Archibald Simpson'], ['6424', 'The Gordon Highlander'], ['2460', 'The Justice Mill'], ['1233', 'Hunters Hall'], ['6327', 'The Bourtree'], ['6754', 'The Cross Keys'], ['6919', 'Jollys Hotel'], ['358', 'The Counting House'], ['478', 'Sir John Stirling Maxwell'], ['282', 'The Counting House'], ['833', 'The Crystal Palace'], ['1660', 'The Esquire House'],
['1903', 'The Henglers Circus'], ['2663', 'The Kirky Puffer'], ['5520', 'The Lord of the Isles'], ['2151', 'The Sir John Moore'], ['2615', 'The Society Room'], ['4117', 'The Alexander Bain'],
['6411', 'The Great Glen'], 
['1789', 'The Kings Highway'], ['6736', 'The Auld Brig'], ['6902', 'The Paddle Steamer'], ['943', 'The Salt Cot'], 
['6390', 'The Bobbing John'],
['2468', 'The Brandon Works'], ['6502', 'The Carrick Stone'], ['1014', 'The Wishaw Malt'], ['2959', 'The Capital Asset'], ['6732', 'The Fair OBlair'], 
['7057', 'The Captain James Lang'], 
['2496', 'The Carron Works'], ['1044', 'The Corn Exchange'], ['5717', 'The Corryvreckan'], ['6453', 'The Henry Bell'],
['5648', 'The Crossed Peels'], 
['801', 'The Golden Acorn'], ['6198', 'The Guildhall & Linen Exchange'], ['1065', 'The Robert Nairn'], ['625', 'The James Watt'], ['497', 'The Last Post'], 
['797', 'The Muckle Cross'], 
['6266', 'The Newyearfield'], ['6319', 'The Prestwick Pioneer'], ['804', 'The West Kirk'], ['1204', 'The Robert the Bruce'], ['6677', 'The Saltoun Inn'],
['725', 'The Wheatsheaf Inn'],
['6682', 'Pen Cob'], ['1715', 'Tafarn Y Porth'], ['1664', 'The Black Bull Inn'], ['6259', 'The Aneurin Bevan'], ['2042', 'The Central Bar'],
['754', 'The Ernest Willows'],
['1749', 'The Gatekeeper'], ['5361', 'The Great Western'], ['750', 'The Ivor Davies'], ['6428', 'The Mount Stuart'], ['207', 'The Prince of Wales'], 
['749', 'The Bank Statement'],
['6897', 'The Mardy Inn'], ['175', 'The Potters Wheel'], ['6700', 'The Red Lion Inn'], ['709', 'The Bears Head'], ['5574', 'The Sir Samuel Romilly'],
['5345', 'The Bell Hanger'], 
['1742', 'The Coliseum'], ['623', 'The Kings Head'], ['6671', 'The Black Boy'], ['7401', 'The George Hotel'], ['5536', 'The Castle Hotel'], 
['2000', 'The Sussex'], 
['5815', 'The Central Hotel'],
['2422', 'The Gold Cape'],
['6445', 'The Market Cross'],
['729', 'The Lord Caradoc'],
['386', 'The Elihu Yale'],
['2394', 'The North and South Wales Bank'],
['458', 'The Godfrey Morgan'],
['191', 'The John Wallace Linton'], 
['5195', 'The John Fielding'], 
['6372', 'The Malcolm Uphill'], 
['1381', 'The Sirhowy'], 
['1762', 'The Olympia'], 
['680', 'The Picture House'], 
['5468', 'The Pontlottyn'],
['1013', 'The Palladium'],
['807', 'The Picture House'],
['6954', 'The Sawyers Arms'], 
['1087', 'The Wyndham Arms'], 
['2470', 'The Tumble Inn'], 
['2667', 'Yr Ieuan Ap Iago'], 
['5748', 'The William Owen'], 
['465', 'The York Palace'], 
['1721', 'Yr Hen Dderwen'], 
['1258', 'Y Dic Penderyn'],
['1176', 'Yr Hen Orsaf']]


best = main()

for i in range(10):
    print(best[i][0],best[i][1], "ml with a price per unit of £",str(round(best[i][-1], 2)))
