# -*- coding: utf-8 -*-

from gwmpy import check_missing_args

from lxml import etree
import uuid

# =============================================================================
# General info
# =============================================================================

# https://schema.broservices.nl/xsd/isgmw/1.1/isgmw-messages.xsd

#%%

def gen_wellconstructiondate(data, nsmap):
    
    WellConstructionDate = etree.Element(("{%s}" % nsmap['ns']) + 'wellConstructionDate', nsmap=nsmap)
    date = etree.SubElement(WellConstructionDate, ("{%s}" % nsmap['ns1']) + 'date', nsmap=nsmap)
    date.text = data['wellConstructionDate']
    return(WellConstructionDate)

#%%

def gen_deliveredlocation(data, nsmap, codespacemap):
    
    """
    
    Parameters
    ----------
    data : dictionary, with deliveredLocation item.
        The deliveredLocation item itself is also a 
        dictionary containing the following items:
            X: xcoordinate
            Y: ycoordinate
            horizontalPositioningMethod: horizontalPositioningMethod 
    nsmap : dictionary
        namespace mapping 
    codespacemap: dictionary
        codespace mapping

    Returns
    -------
    subelement structure to pass in the deliveredLocation element

    Note: 
    -------
    The coordinate system is restricted to EPSG::28992
    """
    
    arglist = {'X':'obligated',
                'Y':'obligated',
                'horizontalPositioningMethod':'obligated'}
    
    check_missing_args(data['deliveredLocation'], arglist, 'gen_deliveredlocation')

    
    deliveredLocation = etree.Element(("{%s}" % nsmap['ns']) + 'deliveredLocation', nsmap=nsmap)
        
    location  = etree.SubElement(deliveredLocation, ("{%s}" % nsmap['ns2']) + 'location', nsmap = nsmap,
        attrib={
        ("{%s}" % nsmap['ns3']) + 'id':'id-'+str(uuid.uuid4()),
        'srsName':"urn:ogc:def:crs:EPSG::28992"
        })
        
    pos = etree.SubElement(location, ("{%s}" % nsmap['ns3']) + 'pos', nsmap=nsmap)
    
    pos.text = '{X} {Y}'.format(X = str(data['deliveredLocation']['X']),Y = str(data['deliveredLocation']['Y']))
    
    horizontalPositioningMethod = etree.SubElement(deliveredLocation, ("{%s}" % nsmap['ns2']) + 'horizontalPositioningMethod', nsmap = nsmap, codeSpace = codespacemap['horizontalPositioningMethod'])
    horizontalPositioningMethod.text = data['deliveredLocation']['horizontalPositioningMethod']

    
    return(deliveredLocation)

#%%

def gen_deliveredverticalposition(data, nsmap, codespacemap):
      
    arglist = {'localVerticalReferencePoint':'obligated',
                'offset':'obligated',
                'verticalDatum':'obligated',
                'groundLevelPosition':'obligated',
                'groundLevelPositioningMethod':'obligated'
                }
    
    check_missing_args(data['deliveredVerticalPosition'], arglist, 'gen_deliveredverticalposition')

    deliveredVerticalPosition = etree.Element(("{%s}" % nsmap['ns']) + 'deliveredVerticalPosition', nsmap=nsmap)
    localVerticalReferencePoint = etree.SubElement(deliveredVerticalPosition, ("{%s}" % nsmap['ns2']) + 'localVerticalReferencePoint', nsmap = nsmap, codeSpace = codespacemap['localVerticalReferencePoint'])
    localVerticalReferencePoint.text = data['deliveredVerticalPosition']['localVerticalReferencePoint']

    offset = etree.SubElement(deliveredVerticalPosition, ("{%s}" % nsmap['ns2']) + 'offset', nsmap = nsmap, uom = "m")
    offset.text = str(data['deliveredVerticalPosition']['offset'])    

    verticalDatum = etree.SubElement(deliveredVerticalPosition, ("{%s}" % nsmap['ns2']) + 'verticalDatum', nsmap = nsmap, codeSpace = "urn:bro:gmw:VerticalDatum")
    verticalDatum.text = data['deliveredVerticalPosition']['verticalDatum']        

    groundLevelPosition = etree.SubElement(deliveredVerticalPosition, ("{%s}" % nsmap['ns2']) + 'groundLevelPosition', nsmap = nsmap, uom = "m")
    groundLevelPosition.text = str(data['deliveredVerticalPosition']['groundLevelPosition'])        
    
    groundLevelPositioningMethod = etree.SubElement(deliveredVerticalPosition, ("{%s}" % nsmap['ns2']) + 'groundLevelPositioningMethod', nsmap = nsmap, codeSpace = codespacemap['groundLevelPositioningMethod'])
    groundLevelPositioningMethod.text = data['deliveredVerticalPosition']['groundLevelPositioningMethod']        
        
    return(deliveredVerticalPosition)

#%% 

def gen_materialused(data, tube, nsmap, codespacemap):
    arglist = {'tubePackingMaterial':'obligated',
                'tubeMaterial':'obligated',
                'glue':'obligated'}    
    
    check_missing_args(data['monitoringTubes'][tube]['materialUsed'], arglist, 'gen_monitoringtube, tube with index {}, gen_materialused'.format(str(tube)))
    
    materialUsed = etree.Element(("{%s}" % nsmap['ns']) + 'materialUsed', nsmap=nsmap)

    tubePackingMaterial = etree.SubElement(materialUsed, ("{%s}" % nsmap['ns2']) + 'tubePackingMaterial', nsmap = nsmap, codeSpace=codespacemap['tubePackingMaterial'])
    tubePackingMaterial.text = str(data['monitoringTubes'][tube]['materialUsed']['tubePackingMaterial'])
    
    tubeMaterial = etree.SubElement(materialUsed, ("{%s}" % nsmap['ns2']) + 'tubeMaterial', nsmap = nsmap, codeSpace=codespacemap['tubeMaterial'])
    tubeMaterial.text = str(data['monitoringTubes'][tube]['materialUsed']['tubeMaterial'])
    
    glue = etree.SubElement(materialUsed, ("{%s}" % nsmap['ns2']) + 'glue', nsmap = nsmap, codeSpace="urn:bro:gmw:Glue")
    glue.text = str(data['monitoringTubes'][tube]['materialUsed']['glue'])
    
    return(materialUsed)

#%%

def gen_screen(data, tube, nsmap,codespacemap):
    arglist = {'screenLength':'obligated',
                'sockMaterial':'obligated'}    
    
    check_missing_args(data['monitoringTubes'][tube]['screen'], arglist, 'gen_monitoringtube, tube with index {}, gen_screen'.format(str(tube)))
    
    screen = etree.Element(("{%s}" % nsmap['ns']) + 'screen', nsmap=nsmap)

    screenLength = etree.SubElement(screen, ("{%s}" % nsmap['ns']) + 'screenLength', nsmap = nsmap, uom="m")
    screenLength.text = str(data['monitoringTubes'][tube]['screen']['screenLength'])
    
    sockmaterial = etree.SubElement(screen, ("{%s}" % nsmap['ns']) + 'sockMaterial', nsmap = nsmap, codeSpace=codespacemap['sockMaterial'])
    sockmaterial.text = str(data['monitoringTubes'][tube]['screen']['sockMaterial'])

    return(screen)    

#%%

def gen_plaintubepart(data, tube, nsmap):
    arglist = {'plainTubePartLength':'obligated'}    
    
    check_missing_args(data['monitoringTubes'][tube]['plainTubePart'], arglist, 'gen_monitoringtube, tube with index {}, gen_plaintubepart'.format(str(tube)))
    
    plainTubePart = etree.Element(("{%s}" % nsmap['ns']) + 'plainTubePart', nsmap=nsmap)

    plainTubePartLength = etree.SubElement(plainTubePart, ("{%s}" % nsmap['ns2']) + 'plainTubePartLength', nsmap = nsmap, uom="m")
    plainTubePartLength.text = str(data['monitoringTubes'][tube]['plainTubePart']['plainTubePartLength'])
    
    return(plainTubePart)

#%%

def gen_sedimentsump(data, tube, nsmap):
    arglist = {'sedimentSumpLength':'obligated'}    
    
    check_missing_args(data['monitoringTubes'][tube]['sedimentSump'], arglist, 'gen_monitoringtube, tube with index {}, gen_sedimentsump'.format(str(tube)))
    
    sedimentSump = etree.Element(("{%s}" % nsmap['ns']) + 'sedimentSump', nsmap=nsmap)

    sedimentSumpLength = etree.SubElement(sedimentSump, ("{%s}" % nsmap['ns2']) + 'sedimentSumpLength', nsmap = nsmap, uom="m")
    sedimentSumpLength.text = str(data['monitoringTubes'][tube]['sedimentSump']['sedimentSumpLength'])
    
    return(sedimentSump)

#%%
def gen_electrode(data, tube, geoOhmCableId, electrode, nsmap, codespacemap):
    arglist = {'electrodeNumber':'obligated',
               'electrodePackingMaterial':'obligated',               
               'electrodeStatus':'obligated',               
               'electrodePosition':'obligated',                              
               }    
    
    targetdata = data['monitoringTubes'][tube]['geoOhmCables'][geoOhmCableId]['electrodes'][electrode]
    
    check_missing_args(targetdata, arglist, 'gen_monitoringtube, tube with index {}, geoOhmCable with index {}, electrode with index {}'.format(str(tube),str(geoOhmCableId),str(electrode)))
    
    electrode = etree.Element(("{%s}" % nsmap['ns']) + 'electrode', nsmap=nsmap)

    electrodeNumber = etree.SubElement(electrode, ("{%s}" % nsmap['ns2']) + 'electrodeNumber', nsmap = nsmap)
    electrodeNumber.text = str(targetdata['electrodeNumber'])

    electrodePackingMaterial = etree.SubElement(electrode, ("{%s}" % nsmap['ns2']) + 'electrodePackingMaterial', nsmap = nsmap, codeSpace=codespacemap['electrodePackingMaterial'])
    electrodePackingMaterial.text = str(targetdata['electrodePackingMaterial'])

    electrodeStatus = etree.SubElement(electrode, ("{%s}" % nsmap['ns2']) + 'electrodeStatus', nsmap = nsmap, codeSpace=codespacemap['electrodeStatus'])
    electrodeStatus.text = str(targetdata['electrodeStatus'])
    
    electrodePosition = etree.SubElement(electrode, ("{%s}" % nsmap['ns2']) + 'electrodePosition', nsmap = nsmap, uom="m")
    electrodePosition.text = str(targetdata['electrodePosition'])
    
    return(electrode)


#%%

def gen_geoohmcable(data, tube, geoOhmCableId, nsmap,codespacemap):
    arglist = {'cableNumber':'obligated',
               'electrodes':'obligated'}    
    
    check_missing_args(data['monitoringTubes'][tube]['geoOhmCables'][geoOhmCableId], arglist, 'gen_monitoringtube, tube with index {}, gen_geoohmcable, geoOhmCableId {}'.format(str(tube),str(geoOhmCableId)))

    
    if len(data['monitoringTubes'][tube]['geoOhmCables'][geoOhmCableId]['electrodes']) < 2:
        raise Exception("Not enough electrodes provided for geoOhmCable, at least 2 electrodes should be provided")
         
    else:
        geoOhmCable = etree.Element(("{%s}" % nsmap['ns']) + 'geoOhmCable', nsmap=nsmap)
        
        cableNumber = etree.SubElement(geoOhmCable, ("{%s}" % nsmap['ns']) + 'cableNumber', nsmap = nsmap)
        cableNumber.text = str(geoOhmCableId+1)        
    
        electrodes = {}
        for electrode in range(len(data['monitoringTubes'][tube]['geoOhmCables'][geoOhmCableId]['electrodes'])):
            electrodes['electrode{}'.format(str(electrode))] = gen_electrode(data, tube, geoOhmCableId, electrode, nsmap,codespacemap)
            geoOhmCable.append(electrodes['electrode{}'.format(str(electrode))])    
    
        return(geoOhmCable)

#%%

def gen_monitoringtube(data, tube, nsmap,codespacemap):
    """

    Parameters
    ----------
    data : dictionary, with monitoringtubes item.
        The monitoringtubes item consits of a list with dictionaries, 
        in which each dictionary contains the attribute data of a single
        monitoringtube. The required and optional items are listed within
        the arglist in this function.
    tube : int
        monituringtube index in list of available monitoringtubes. A 
        monitoringTube element will be created for the selected 
        monitoringtube.
    nsmap : dictionary
        namespace mapping
    codespacemap: dictionary
        codespace mapping

    Returns
    -------
    subelement structure to pass in the monitoringtube element for the 
    selected monitoringtube

    """
    
    arglist = {'tubeNumber':'obligated',
                'tubeType':'obligated',
                'artesianWellCapPresent':'obligated',
                'sedimentSumpPresent':'obligated',
                'numberOfGeoOhmCables':'obligated',
                'tubeTopDiameter':'obligated',
                'variableDiameter':'obligated',
                'tubeStatus':'obligated', 
                'tubeTopPosition':'obligated',
                'tubeTopPositioningMethod':'obligated',
                'materialUsed':'obligated',
                'screen':'obligated', 
                'plainTubePart':'obligated',
                'sedimentSump':'optional', 
                'geoOhmCables':'optional'}
    
    check_missing_args(data['monitoringTubes'][tube], arglist, 'gen_monitoringtube, tube with index {}'.format(str(tube)))
    
    monitoringTube = etree.Element(("{%s}" % nsmap['ns']) + 'monitoringTube', nsmap=nsmap)
    
    tubeNumber = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'tubeNumber', nsmap = nsmap)
    tubeNumber.text = str(data['monitoringTubes'][tube]['tubeNumber'])
    
    tubeType = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'tubeType', nsmap = nsmap, codeSpace = codespacemap['tubeType'])
    tubeType.text = data['monitoringTubes'][tube]['tubeType']
    
    artesianWellCapPresent = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'artesianWellCapPresent', nsmap = nsmap)
    artesianWellCapPresent.text = data['monitoringTubes'][tube]['artesianWellCapPresent']      
    
    sedimentSumpPresent = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'sedimentSumpPresent', nsmap = nsmap)
    sedimentSumpPresent.text = data['monitoringTubes'][tube]['sedimentSumpPresent']

    numberOfGeoOhmCables = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'numberOfGeoOhmCables', nsmap = nsmap)
    numberOfGeoOhmCables.text = str(data['monitoringTubes'][tube]['numberOfGeoOhmCables'])          

    tubeTopDiameter = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'tubeTopDiameter', nsmap = nsmap, uom = 'mm')
    tubeTopDiameter.text = str(data['monitoringTubes'][tube]['tubeTopDiameter'])              

    variableDiameter = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'variableDiameter', nsmap = nsmap)
    variableDiameter.text = str(data['monitoringTubes'][tube]['variableDiameter'])    

    tubeStatus = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'tubeStatus', nsmap = nsmap, codeSpace=codespacemap['tubeStatus'])
    tubeStatus.text = data['monitoringTubes'][tube]['tubeStatus']
    
    tubeTopPosition = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'tubeTopPosition', nsmap = nsmap, uom = 'm')
    tubeTopPosition.text = str(data['monitoringTubes'][tube]['tubeTopPosition']) 

    tubeTopPositioningMethod = etree.SubElement(monitoringTube, ("{%s}" % nsmap['ns']) + 'tubeTopPositioningMethod', nsmap = nsmap, codeSpace=codespacemap['tubeTopPositioningMethod'])
    tubeTopPositioningMethod.text = str(data['monitoringTubes'][tube]['tubeTopPositioningMethod'])  

    # obligated constructables:
    materialUsed = gen_materialused(data, tube, nsmap,codespacemap)
    monitoringTube.append(materialUsed)
    
    screen = gen_screen(data, tube, nsmap, codespacemap)
    monitoringTube.append(screen)
    
    plainTubePart = gen_plaintubepart(data, tube, nsmap)
    monitoringTube.append(plainTubePart)    
    
    # optional constructables:
    if 'sedimentSump' in list(data['monitoringTubes'][tube].keys()):
        sedimentSump = gen_sedimentsump(data, tube, nsmap)
        monitoringTube.append(sedimentSump)          

    if 'geoOhmCables' in list(data['monitoringTubes'][tube].keys()):
        
        geoOhmCables = {}
        
        for geoOhmCableId in range(len(data['monitoringTubes'][tube]['geoOhmCables'])):
            geoOhmCables['geoOhmCable{}'.format(str(geoOhmCableId))] = gen_geoohmcable(data, tube, geoOhmCableId, nsmap,codespacemap)
            monitoringTube.append(geoOhmCables['geoOhmCable{}'.format(str(geoOhmCableId))])
        
    return(monitoringTube)