import os
import sys


import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')


ROOTFOLDER = r'F:\DonMonteith\Watersheds\ArcGISDesktopWatersheds'


ArcGISFolder = r'ArcGIS'
ArcGISFolder = os.path.join(ROOTFOLDER, ArcGISFolder)
ArcGISFolder = os.path.normpath(ArcGISFolder)


FGDB = r'FGDB01.gdb'
FGDB = os.path.join(ArcGISFolder, FGDB)
FGDB = os.path.normpath(FGDB)
if not arcpy.Exists(FGDB):
    arcpy.CreateFileGDB_management(os.path.split(FGDB)[0], os.path.split(FGDB)[1], 'CURRENT')


# inDTM = r'E:\smw\Workspace\QGIS\srtm\n54_w003_1arc_v3.tif'
# inDTM = r'E:\smw\Workspace\QGIS\ArcGIS\SRTM.gdb\n54_w003_1arc_v3'
inDTM = r'F:\DonMonteith\Watersheds\ArcGISDesktopWatersheds\ArcGIS\SRTM.gdb\n54_w003_1arc_v3'
print('\n\ninDTM:\t{0}\n\n'.format(inDTM))


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


def table_function(table):
    outTable = os.path.join(FGDB, table)
    outTable = os.path.normpath(outTable)
    if arcpy.Exists(outTable):
        print('\tDeleting {0}...'.format(outTable))
        arcpy.Delete_management(outTable)
    return outTable


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
# outCon = Con(outFlowAccumulation, 1, None, 'Value = 415880')
outCon = Con(outFlowAccumulation, 1, None, 'Value = 298450')
print('\tSaving {0}...'.format(fgdbRaster))
outCon.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Watershed')
outWatershed = Watershed(outFlowDirection, outCon, 'Value')
print('\tSaving {0}...'.format(fgdbRaster))
outWatershed.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Slope')
outSlope = Slope(outFill, 'DEGREE', 1.0)
print('\tSaving {0}...'.format(fgdbRaster))
outSlope.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbRaster = raster_function('a' + str(n).zfill(2) + '_Aspect')
outAspect = Aspect(outFill)
print('\tSaving {0}...'.format(fgdbRaster))
outAspect.save(fgdbRaster)


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbTable = table_function('a' + str(n).zfill(2) + '_ZS_Elevation')
outZonalStatistics = ZonalStatisticsAsTable(outWatershed, 'Value', outFill, fgdbTable, 'DATA', 'ALL')
print('\tCreating {0}...'.format(fgdbTable))


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbTable = table_function('a' + str(n).zfill(2) + '_ZS_Slope')
outZonalStatistics = ZonalStatisticsAsTable(outWatershed, 'Value', outSlope, fgdbTable, 'DATA', 'ALL')
print('\tCreating {0}...'.format(fgdbTable))


n += 1
print('{0}'.format(str(n).zfill(2)))
fgdbTable = table_function('a' + str(n).zfill(2) + '_ZS_Aspect')
outZonalStatistics = ZonalStatisticsAsTable(outWatershed, 'Value', outAspect, fgdbTable, 'DATA', 'MEAN')
print('\tCreating {0}...'.format(fgdbTable))
