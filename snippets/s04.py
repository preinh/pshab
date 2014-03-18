from oq_input.source_model_converter import nrml2shp, shp2nrml

nrml2shp("s03.xml", "s03.shp")
shp2nrml(["s03"], "s04")

