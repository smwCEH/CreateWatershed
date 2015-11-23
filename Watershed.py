import time


import arcpy


arcpy.env.overwriteOutput = True


# # Generate watersheds using AGOL Watersheds hydrology geoprocessing service
# arcpy.ImportToolbox('http://hydro.arcgis.com/arcgis/services;Tools/Hydrology;<username>;<password>', 'hydro')
# result = arcpy.Watershed_hydro(r'F:\DonMonteith\Watersheds\AWMN.shp',
#                                'FID',
#                                '',
#                                'Meters',
#                                'FINEST',
#                                'False',
#                                'True')
# while result.status < 4:
#     print result.status
#     time.sleep(0.25)
# print "Execution Finished"
# arcpy.CopyFeatures_management(result.getOutput(0),
#                               r'F:\DonMonteith\Watersheds\AWMBWatersheds.shp')
# arcpy.CopyFeatures_management(result.getOutput(1),
#                               r'F:\DonMonteith\Watersheds\AWMBPourPoints.shp')


# Summarise elevation in watersheds usign AGOL SummarizeElevation elevation geoprocessing service
arcpy.ImportToolbox('http://elevation.arcgis.com/arcgis/services;Tools/Elevation;<username>;<password>', 'elev')
result = arcpy.SummarizeElevation_elev(r'F:\DonMonteith\Watersheds\AWMBWatersheds.shp',
                                       'PourPtID',
                                       'FINEST',
                                       'True')
while result.status < 4:
    print result.status
    time.sleep(0.25)
print "Execution Finished"
arcpy.CopyFeatures_management(result.getOutput(0),
                              r'F:\DonMonteith\Watersheds\AWMBSumElev.shp')
