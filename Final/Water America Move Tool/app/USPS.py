import urllib.request
import xml.etree.ElementTree as ET


class AddressValidator():
    def __init__(self, Street_Address2, City, State, Zip5):
        self.Street_Address2 = Street_Address2
        self.City = City
        self.State = State
        self.Zip5 = Zip5

    def __repr__(self): 
        return '(%s, %s, %s, %s)' % (self.Address2, self.City, self.State, self.Zip5)

    def __str__(self):
        return '(%s, %s, %s, %s)' % (self.Address2, self.City, self.State, self.Zip5)

    def generate_parse_tree(self):
        Address1 = None
      
        address_list = []
        address_list.append(self.Street_Address2.upper())
        address_list.append(self.City.upper())
        address_list.append(self.State.upper())
        address_list.append(self.Zip5.upper())

        requestXML = '''
        <?xml version="1.0"?>
        <AddressValidateRequest USERID="487RUTGE6377">
            <Revision>1</Revision>
            <Address ID="0">
                <Address1>{}</Address1>
                <Address2>{}</Address2>
                <City>{}</City>
                <State>{}</State>
                <Zip5>{}</Zip5>
            <Zip4/>
            </Address>
        </AddressValidateRequest>
        '''.format(Address1, self.Street_Address2, self.City, self.State, self.Zip5)

         #Prepare.xml.string.doc.for.query.string
        docString = requestXML
        docString = docString.replace('\n','').replace('\t','')
        docString = urllib.parse.quote_plus(docString)
        url="http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=" + docString
        #print(url+"\n\n")

        #API CALL and Check for Errors
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            print("Error making HTTP call:")
            print(response.info())
            exit()

        #If all went well, we get the content of the response and print it out
        contents = response.read()
        #print(contents)
        
        return address_list, ET.fromstring(contents)

    def validate_street_address(self):
        address_list, root = self.generate_parse_tree()
        for address in root.findall('Address'):
            street_address = (address.find("Address2").text)
        return (address_list[0] == street_address)
            
    def validate_city(self):
        address_list, root = self.generate_parse_tree()
        for address in root.findall('Address'):
            city = (address.find("City").text)
        return (address_list[1] == city)

    def validate_state(self):
        address_list, root = self.generate_parse_tree()
        for address in root.findall('Address'):
            state = (address.find("State").text)
        return (address_list[2] == state)

    def validate_zip_code(self):
        address_list, root = self.generate_parse_tree()
        for address in root.findall('Address'):
            zip_code = (address.find("Zip5").text)
        return (address_list[3] == zip_code)
    
    def validate_address(self):
        return self.validate_street_address() and self.validate_city() and self.validate_state() and self.validate_zip_code()

#Calling and Testing the class - expecting False
WrongAddress = AddressValidator("12 Stern Light Drive","Camden","NJ","08054")
WrongAddress.validate_address()

#Calling and Testing the class - expecting True
CorrectAddress = AddressValidator("12 Stern Light Dr","Mount Laurel","NJ","08054")
CorrectAddress.validate_address()

#SIDE NOTE: it has to be DR not Drive to get True !
