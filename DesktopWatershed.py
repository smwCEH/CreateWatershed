import os
import sys


import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')


ROOTFOLDER = r'E:\smw\Workspace\QGIS'


ArcGISFolder = r'ArcGIS'
ArcGISFolder = os.path.join(ROOTFOLDER, ArcGISFolder)
ArcGISFolder = os.path.normpath(ArcGISFolder)


FGDB = r'FGDB01.gdb'
FGDB = os.path.join(ArcGISFolder, FGDB)
FGDB = os.path.normpath(FGDB)
if not arcpy.Exists(FGDB):
    arcpy.CreateFileGDB_management(os.path.split(FGDB)[0], os.path.split(FGDB)[1], 'CURRENT')


inDTM = r'E:\smw\Workspace\QGIS\srtm\n54_w003_1arc_v3.tif'


env.workspace = FGDB
env.cellSize = inDTM
env.mask = inDTM
env.snapRaster = inDTM
env.extent = inDTM
env.outputCoordinateSystem = inDTM
# env.overwriteOutput = True


def raster_function(raster):
    outRaster = os.path.join(FGDB, raster)
    outRaster = os.path.normpath(outRaster)
    if arcpy.Exists(outRaster):
        print('\tDeleting {0}...'.format(outRaster))
        arcpy.Delete_management(outRaster)
    return outRaster


n = 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_FlowDir')
outFlowDirection = FlowDirection(inDTM)
print('\tSaving {0}...'.format(fgdbRaster))
outFlowDirection.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Sink')
outSink = Sink(outFlowDirection)
print('\tSaving {0}...'.format(fgdbRaster))
outSink.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Fill')
outFill = Fill(inDTM)
print('\tSaving {0}...'.format(fgdbRaster))
outFill.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Sink')
outSink = Sink(outFill)
print('\tSaving {0}...'.format(fgdbRaster))
outSink.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Fill')
outFill = Fill(outFill)
print('\tSaving {0}...'.format(fgdbRaster))
outFill.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Sink')
outSink = Sink(outFill)
print('\tSaving {0}...'.format(fgdbRaster))
outSink.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_FlowDir')
outFlowDirection = FlowDirection(outFill)
print('\tSaving {0}...'.format(fgdbRaster))
outFlowDirection.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_FlowAcc')
outFlowAccumulation = FlowAccumulation(outFlowDirection, '#', 'INTEGER')
print('\tSaving {0}...'.format(fgdbRaster))
outFlowAccumulation.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Con')
outCon = Con(outFlowAccumulation, 1, None, 'Value = 415880')
print('\tSaving {0}...'.format(fgdbRaster))
outCon.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Watershed')
outWatershed = Watershed(outFlowDirection, outCon, 'Value')
print('\tSaving {0}...'.format(fgdbRaster))
outWatershed.save(fgdbRaster)
