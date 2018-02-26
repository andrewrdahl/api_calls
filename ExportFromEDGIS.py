import arcpy
from arcpy import env
import xml.dom.minidom as DOM
import sys


def make_feature_layers():
	delete_fields = [
			'edgis_MPLS_PARCELS_MUNICNM',
			'edgis_MPLS_PARCELS_ZIPCD',
			'edgis_MPLS_PARCELS_HOUSENUM',
			'edgis_MPLS_PARCELS_FRACHOUSEN',
			'edgis_MPLS_PARCELS_STREETNM',
			'edgis_MPLS_PARCELS_CONDONO',
			'edgis_MPLS_PARCELS_PROPSTATCD',
			'edgis_MPLS_PARCELS_X_CENTROID',
			'edgis_MPLS_PARCELS_Y_CENTROID',
			'edgis_MPLS_PARCELS_LATITUDE',
			'edgis_MPLS_PARCELS_LONGITUDE',
			'edgis_MPLS_PARCELS_WGS_X',
			'edgis_MPLS_PARCELS_WGS_Y',
			'edgis_MPLS_PARCELS_PID'
			]

	env.workspace = 'M:\CPED\Common\GIS\MINS_GIS_Models\CPED_Inventory.gdb'
	arcpy.env.overwriteOutput = True

	inventory = r'M:\CPED\Common\GIS\MINS_GIS_Models\MINS.sde\dataRepository.CPED_Inventory'
	parcels = r'M:\CPED\Common\GIS\MINS_GIS_Models\edgis.sde\MPLS.PARCELS'
	map = r'M:\CPED\Common\GIS\MINS_GIS_Models\CPED_Inventory.gdb\CPED_Inventory.mxd'

	arcpy.MakeTableView_management(inventory,'inventory_view')

	arcpy.MakeFeatureLayer_management(parcels, 'parcels_layer')

	arcpy.AddJoin_management('parcels_layer', 'PID', 'inventory_view', 'PID', 'KEEP_COMMON')

	arcpy.CopyFeatures_management('parcels_layer', 'M:\CPED\Common\GIS\MINS_GIS_Models\CPED_Inventory.gdb\CPED_Inventory')
	
	arcpy.DeleteField_management('M:\CPED\Common\GIS\MINS_GIS_Models\CPED_Inventory.gdb\CPED_Inventory', delete_fields)
	
	field_list = arcpy.ListFields('M:\CPED\Common\GIS\MINS_GIS_Models\CPED_Inventory.gdb\CPED_Inventory')

	field_names = {}

	for field in field_list:
		field_names[str(field.name)] =str(field.name).replace('Mins_dataRepository_CPED_Inventory_','')

	for field in field_list:
		if field.required == False:
			name = str(field_names[str(field.name)])
			arcpy.AlterField_management('M:\CPED\Common\GIS\MINS_GIS_Models\CPED_Inventory.gdb\CPED_Inventory', field.name, name, name)
	
	arcpy.FeatureToPoint_management('M:\CPED\Common\GIS\MINS_GIS_Models\CPED_Inventory.gdb\CPED_Inventory', 'CPED_Inventory_Points')


if __name__ == '__main__':
        print sys.path[0]
