# -*- coding: utf-8 -*-

from gwmpy.broxml.gld.sourcedocs import *
from gwmpy.broxml.mappings import ns_regreq_map_gld1,ns_regreq_map_gld2,ns_regreq_map_gld3, xsi_regreq_map_gld1, codespace_map_gld1 # mappings
from gwmpy.checks import check_missing_args

from lxml import etree
import os


# =============================================================================
# General info
# =============================================================================

# https://schema.broservices.nl/xsd/isgmw/1.1/isgmw-messages.xsd


#%%

class gld_registration_request():
    
    """
    Class for generating gld registration requests. Check 
    allowed_srcdos for currently available possibilities. 
    """
    
    def __init__(self, srcdoc, **kwargs):
        
        """
        
        Parameters
        ----------
        srcdoc : string
            sourcedoc type (check allowed srcdoc types)
        **kwargs : -
            request-specific attribute data (method-specific)
            sourcedocument-specific attribute data
    
        Returns
        -------
        None, saves generated registration request xml to output directory

        """
        
        # NOTE: IN PROGRESS, MORE SOURCEDOCUMENTS TYPES WILL BE INCLUDED
        
        self.allowed_srcdocs = ['GLD_StartRegistration','GLD_Addition','GLD_Closure']
    
        if srcdoc not in self.allowed_srcdocs:
            raise Exception("Sourcedocument type not allowed")   
        
        self.srcdoc = srcdoc
        self.kwargs = kwargs   
        self.request = None
        
        # Request arguments:
        arglist = {
                   'deliveryAccountableParty':'optional',
                   'broId':'optional',
                   'qualityRegime':'obligated',
                   'requestReference':'obligated',
                   'srcdocdata':'obligated',
                   }
        
        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(self.kwargs, arglist, 'gmw_registration with method initialize')
         
    def generate(self):
               
        # Generate xml document base:
        if self.srcdoc == 'GLD_StartRegistration':
            
            req = etree.Element("registrationRequest",nsmap=ns_regreq_map_gld2,
                attrib={
                'xmlns':ns_regreq_map_gld1['xmlns'],            
                ("{%s}" % ns_regreq_map_gld2['xsi'])+'schemaLocation': xsi_regreq_map_gld1['schemaLocation']
                })
        
        elif self.srcdoc == 'GLD_Addition':
            
            req = etree.Element("registrationRequest",nsmap=ns_regreq_map_gld3,
                attrib={
                'xmlns':ns_regreq_map_gld1['xmlns'],            
                ("{%s}" % ns_regreq_map_gld3['xsi'])+'schemaLocation': xsi_regreq_map_gld1['schemaLocation']
                })        
            
        # Define registration request arguments:
        requestReference=etree.SubElement(req, ("{%s}" % ns_regreq_map_gld2['brocom']) + "requestReference", nsmap=ns_regreq_map_gld2)
        requestReference.text = self.kwargs['requestReference']

        try:
            self.kwargs['deliveryAccountableParty']
            deliveryAccountableParty=etree.SubElement(req, ("{%s}" % ns_regreq_map_gld2['brocom']) + "deliveryAccountableParty", nsmap=ns_regreq_map_gld2)
            deliveryAccountableParty.text = self.kwargs['deliveryAccountableParty']
        except:
            pass

        try:
            self.kwargs['broId']
            broId=etree.SubElement(req, ("{%s}" % ns_regreq_map_gld2['brocom']) + "broId", nsmap=ns_regreq_map_gld2)
            broId.text = self.kwargs['broId']
        except:
            pass

        qualityRegime=etree.SubElement(req, ("{%s}" % ns_regreq_map_gld2['brocom']) + "qualityRegime", nsmap=ns_regreq_map_gld2)
        qualityRegime.text = self.kwargs['qualityRegime']
        
        
        # Create sourcedocument and add to registrationrequest:
        if self.srcdoc == 'GLD_StartRegistration':
            
            if 'broId' in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' not allowed in combination with given sourcedocument")
            else:
                sourceDocument=gen_gld_startregistration(self.kwargs['srcdocdata'], ns_regreq_map_gld2, codespace_map_gld1)
                req.append(sourceDocument)

        elif self.srcdoc == 'GLD_Addition':
            
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gld_addition(self.kwargs['srcdocdata'], ns_regreq_map_gld3, codespace_map_gld1)
                req.append(sourceDocument)
        
        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding='utf8', method='xml')
        #print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_xml(self, filename, output_dir=None):
    
        if output_dir == None:
            self.requesttree.write(filename, pretty_print = True)
        else:
            self.requesttree.write(os.path.join(output_dir,filename), pretty_print=True)

#%% gld replace request


class gld_replace_request():
    
    
    # VRAAG: WAT IS VOOR GLD ADDITION DE EENHEID VAN CORRECTIE? WORDEN DE 
    # GML IDS VAN HET OBSPROC EN OBS VERVANGEN OF NIET?
    
    # AANNAME: BIJ DE ID's van OBSPROC mag de gml id in de replace niet
    # aanwezig zijn in een ander document (gaat hier aannemelijk niet om href,
    # maar echt om de initialisatie). De observation gml id mag ook niet eerder
    # gebruikt zijn (betekend ook niet gml id van oude observatie)
    
    
    """
    Class for generating gld replace requests. Check 
    allowed_srcdos for currently available possibilities. 
    """
    
    def __init__(self, srcdoc, **kwargs):
        
        """
        
        Parameters
        ----------
        srcdoc : string
            sourcedoc type (check allowed srcdoc types)
        **kwargs : -
            request-specific attribute data (method-specific)
            sourcedocument-specific attribute data
    
        Returns
        -------
        None, saves generated replace request xml to output directory

        """
        
        # NOTE: IN PROGRESS, MORE SOURCEDOCUMENTS TYPES WILL BE INCLUDED
        
        self.allowed_srcdocs = ['GLD_Addition']
    
        if srcdoc not in self.allowed_srcdocs:
            raise Exception("Sourcedocument type not allowed")   
        
        self.srcdoc = srcdoc
        self.kwargs = kwargs   
        self.request = None
        
        # Request arguments:
        arglist = {
                   'deliveryAccountableParty':'optional',
                   'broId':'optional',
                   'qualityRegime':'obligated',
                   'requestReference':'obligated',
                   'correctionReason':'obligated',
                   'srcdocdata':'obligated',
                   }
        
        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(self.kwargs, arglist, 'gmw_registration with method initialize')
         
    def generate(self):
               
        # Generate xml document base:       
        if self.srcdoc == 'GLD_Addition':
            
            req = etree.Element("replaceRequest",nsmap=ns_regreq_map_gld3,
                attrib={
                'xmlns':ns_regreq_map_gld1['xmlns'],            
                ("{%s}" % ns_regreq_map_gld3['xsi'])+'schemaLocation': xsi_regreq_map_gld1['schemaLocation']
                })        
            
        # Define registration request arguments:
        requestReference=etree.SubElement(req, ("{%s}" % ns_regreq_map_gld2['brocom']) + "requestReference", nsmap=ns_regreq_map_gld2)
        requestReference.text = self.kwargs['requestReference']

        try:
            self.kwargs['deliveryAccountableParty']
            deliveryAccountableParty=etree.SubElement(req, ("{%s}" % ns_regreq_map_gld2['brocom']) + "deliveryAccountableParty", nsmap=ns_regreq_map_gld2)
            deliveryAccountableParty.text = self.kwargs['deliveryAccountableParty']
        except:
            pass

        try:
            self.kwargs['broId']
            broId=etree.SubElement(req, ("{%s}" % ns_regreq_map_gld2['brocom']) + "broId", nsmap=ns_regreq_map_gld2)
            broId.text = self.kwargs['broId']
        except:
            pass

        qualityRegime=etree.SubElement(req, ("{%s}" % ns_regreq_map_gld2['brocom']) + "qualityRegime", nsmap=ns_regreq_map_gld2)
        qualityRegime.text = self.kwargs['qualityRegime']
        
        correctionReason = etree.SubElement(req, "correctionReason",attrib = {            
                                               'codeSpace':"urn:bro:gld:CorrectionReason"},
                                                nsmap=ns_regreq_map_gld2)
        
        correctionReason.text=self.kwargs['correctionReason']
        
        # Create sourcedocument and add to registrationrequest:
        if self.srcdoc == 'GLD_StartRegistration':
            
            if 'broId' in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' not allowed in combination with given sourcedocument")
            else:
                sourceDocument=gen_gld_startregistration(self.kwargs['srcdocdata'], ns_regreq_map_gld2, codespace_map_gld1)
                req.append(sourceDocument)

        elif self.srcdoc == 'GLD_Addition':
            
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gld_addition(self.kwargs['srcdocdata'], ns_regreq_map_gld3, codespace_map_gld1)
                req.append(sourceDocument)
        
        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding='utf8', method='xml')
        #print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_xml(self, filename, output_dir=None):
    
        if output_dir == None:
            self.requesttree.write(filename, pretty_print = True)
        else:
            self.requesttree.write(os.path.join(output_dir,filename), pretty_print=True)


#%% delete request:

class gld_delete_request():
       
    
    """
    Class for generating gld replace requests. Check 
    allowed_srcdos for currently available possibilities. 
    """
    
    def __init__(self, srcdoc,correctionReason):
        
        """
        
        Parameters
        ----------
        srcdoc : string
            sourcedoc to be deleted (check allowed srcdoc types)
    
        Returns
        -------
        None, saves generated replace request xml to output directory

        """
        self.allowed_srcdocs = ['GLD_Addition']       
        self.srcdoc = etree.fromstring(srcdoc)
        self.correctionReason = correctionReason
        
        check = 'unvalid'
        
        for element in list(self.srcdoc.iter()):
            #print(element.tag)
            for allowed in self.allowed_srcdocs:
                if allowed in element.tag:
                    check='valid'
                
        if check!='valid':
            raise Exception("Sourcedocument type not allowed")   



    def generate(self):        
        
        correctionreason_there = False
        
        for element in list(self.srcdoc.iter()):
            #print(element.tag)
            if 'correctionReason' in element.tag:
                correctionreason_there = True
                correctionreason_el = element
            if 'qualityRegime' in element.tag: 
                qualityRegime_el = element.tag                    
            if 'Request' in element.tag:
                element.tag = 'deleteRequest'
        
        if correctionreason_there == False:
                
            correctionReason = etree.Element("correctionReason",attrib = {            
                                                    'codeSpace':"urn:bro:gld:CorrectionReason"})
            correctionReason.text=self.correctionReason
            qualityRegime_el = self.srcdoc.find(qualityRegime_el)
                
            qualityRegime_el.addnext(correctionReason) 
        
        else:
            correctionreason_el.text = self.correctionReason
        
        self.request = etree.tostring(self.srcdoc)    
        
        self.requesttree = etree.ElementTree(self.srcdoc)
        
    
    def write_xml(self, filename, output_dir=None):
    
        if output_dir == None:
            self.requesttree.write(filename, pretty_print = True)
        else:
            self.requesttree.write(os.path.join(output_dir,filename), pretty_print=True)    
































